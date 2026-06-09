import feedparser
import urllib.request
import json
from datetime import datetime, timedelta, timezone
from dateutil import parser as dtparser

USER_AGENT = "Mozilla/5.0 (compatible; NewsBot/1.0)"

def fetch_all(feeds: dict, hours: int = 24):
    """RSS 피드에서 최근 N시간 이내 기사만 수집"""
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    items = []
    for category, urls in feeds.items():
        for url in urls:
            try:
                d = feedparser.parse(url)
                for e in d.entries:
                    pub = None
                    for key in ("published", "updated"):
                        if e.get(key):
                            try:
                                pub = dtparser.parse(e[key])
                                if pub.tzinfo is None:
                                    pub = pub.replace(tzinfo=timezone.utc)
                                break
                            except Exception:
                                pass
                    if pub and pub < cutoff:
                        continue
                    items.append({
                        "category": category,
                        "title": (e.get("title") or "").strip(),
                        "link": e.get("link", ""),
                        "summary": (e.get("summary") or "").strip(),
                        "published": pub,
                        "source": d.feed.get("title", url),
                    })
            except Exception as ex:
                print(f"[WARN] {url}: {ex}")
    return items

def fetch_reddit_posts(subreddits, top_per_sub=4, question_limit=10):
    """Reddit 서브레딧에서 인기 글 + 질문 글 수집"""
    items = []
    
    # 1. 각 서브레딧에서 24시간 인기 글
    for sub in subreddits:
        try:
            url = f"https://www.reddit.com/r/{sub}/top.json?t=day&limit={top_per_sub}"
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode("utf-8"))
            
            for post in data.get("data", {}).get("children", []):
                p = post["data"]
                # NSFW나 광고 제외
                if p.get("over_18") or p.get("stickied"):
                    continue
                
                items.append({
                    "category": "Reddit인사이트",
                    "subcategory": "인기",
                    "title": p.get("title", "").strip(),
                    "link": f"https://reddit.com{p.get('permalink', '')}",
                    "summary": (p.get("selftext", "") or "")[:500].strip(),
                    "published": datetime.fromtimestamp(p.get("created_utc", 0), tz=timezone.utc),
                    "source": f"r/{sub}",
                    "score": p.get("score", 0),
                    "num_comments": p.get("num_comments", 0),
                })
        except Exception as e:
            print(f"[WARN] r/{sub} 실패: {e}")
    
    # 2. 질문 글 (search API로 한국 관련 질문 찾기)
    question_keywords = [
        "korea+travel+how", 
        "seoul+where+to",
        "korea+tips",
        "visiting+seoul"
    ]
    
    for keyword in question_keywords[:2]:  # API 부하 줄이려고 2개만
        try:
            url = f"https://www.reddit.com/search.json?q={keyword}&sort=new&t=week&limit=5"
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode("utf-8"))
            
            for post in data.get("data", {}).get("children", []):
                p = post["data"]
                if p.get("over_18") or p.get("stickied"):
                    continue
                
                title = p.get("title", "").strip()
                # 질문 형식인지 체크
                is_question = (
                    "?" in title or
                    any(w in title.lower() for w in ["how ", "where ", "what ", "is it", "can i", "should i"])
                )
                if not is_question:
                    continue
                
                items.append({
                    "category": "Reddit인사이트",
                    "subcategory": "질문",
                    "title": title,
                    "link": f"https://reddit.com{p.get('permalink', '')}",
                    "summary": (p.get("selftext", "") or "")[:500].strip(),
                    "published": datetime.fromtimestamp(p.get("created_utc", 0), tz=timezone.utc),
                    "source": f"r/{p.get('subreddit', 'unknown')}",
                    "score": p.get("score", 0),
                    "num_comments": p.get("num_comments", 0),
                })
        except Exception as e:
            print(f"[WARN] Reddit 검색 {keyword} 실패: {e}")
    
    print(f"  Reddit: {len(items)}건 수집")
    return items
