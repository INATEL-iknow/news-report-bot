import feedparser
from datetime import datetime, timedelta, timezone
from dateutil import parser as dtparser

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

def fetch_github_trending(language="", since="daily", limit=15):
    """GitHub Trending 페이지 스크래핑"""
    url = f"https://github.com/trending"
    if language:
        url += f"/{language}"
    url += f"?since={since}"
    
    items = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode("utf-8")
        
        soup = BeautifulSoup(html, "html.parser")
        repos = soup.select("article.Box-row")[:limit]
        
        for repo in repos:
            try:
                title_tag = repo.select_one("h2.h3 a")
                if not title_tag:
                    continue
                repo_path = title_tag.get("href", "").strip("/")
                title = repo_path
                link = f"https://github.com/{repo_path}"
                
                desc_tag = repo.select_one("p")
                description = desc_tag.text.strip() if desc_tag else ""
                
                lang_tag = repo.select_one('[itemprop="programmingLanguage"]')
                language_name = lang_tag.text.strip() if lang_tag else ""
                
                star_tag = repo.select_one(".float-sm-right")
                stars_today = star_tag.text.strip() if star_tag else ""
                
                summary = f"{description}"
                if language_name:
                    summary += f" [언어: {language_name}]"
                if stars_today:
                    summary += f" [{stars_today}]"
                
                items.append({
                    "category": "오늘의출시도구",
                    "title": title,
                    "link": link,
                    "summary": summary,
                    "published": datetime.now(timezone.utc),
                    "source": "GitHub Trending",
                })
            except Exception:
                continue
        print(f"  GitHub Trending: {len(items)}건 수집")
    except Exception as e:
        print(f"[WARN] GitHub Trending 실패: {e}")
    
    return items
