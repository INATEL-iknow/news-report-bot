"""
유튜브 쇼츠 자동화 - 연예 뉴스 수집기
- 국내 연예인 이슈 (한국어)
- 해외 월드 스타 이슈 (영어)
- 매일 최근 24-48시간 뉴스만 수집
"""

import feedparser
from urllib.parse import quote
from datetime import datetime, timedelta, timezone
from dateutil import parser as dtparser


# 국내 연예 뉴스 검색 키워드
KOREAN_ENTERTAINMENT_QUERIES = [
    "연예인 이슈",
    "아이돌 논란",
    "배우 열애",
    "결혼 발표",
    "결별 소식",
    "K-POP 컴백",
    "스캔들",
    "예능 화제",
    "드라마 화제",
    "BTS",
    "블랙핑크",
    "뉴진스",
    "아이유",
    "손흥민",
]


# 해외 월드 스타 검색 키워드
GLOBAL_CELEBRITY_QUERIES = [
    "celebrity breaking news",
    "hollywood scandal",
    "celebrity wedding",
    "celebrity breakup",
    "taylor swift",
    "beyonce jay-z",
    "kim kardashian",
    "kanye west",
    "kpop world star",
    "netflix show controversy",
    "grammy nominations",
    "oscar buzz",
    "billboard hot 100",
]


def build_gnews_url(query, is_korean=True):
    """Google News RSS URL 생성"""
    encoded = quote(query)
    if is_korean:
        return f"https://news.google.com/rss/search?q={encoded}&hl=ko&gl=KR&ceid=KR:ko"
    else:
        return f"https://news.google.com/rss/search?q={encoded}&hl=en-US&gl=US&ceid=US:en"


def parse_item(entry, source, category):
    """RSS 엔트리 파싱"""
    pub = None
    for key in ("published", "updated"):
        if entry.get(key):
            try:
                pub = dtparser.parse(entry[key])
                if pub.tzinfo is None:
                    pub = pub.replace(tzinfo=timezone.utc)
                break
            except Exception:
                pass
    
    return {
        "source": source,
        "category": category,
        "title": (entry.get("title") or "").strip(),
        "link": entry.get("link", ""),
        "summary": (entry.get("summary") or "").strip(),
        "published": pub,
    }


def fetch_google_news(queries, is_korean=True, hours=48):
    """Google News에서 여러 키워드로 뉴스 수집"""
    category = "korean" if is_korean else "global"
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    items = []
    
    for query in queries:
        try:
            url = build_gnews_url(query, is_korean)
            d = feedparser.parse(url)
            
            for e in d.entries[:5]:  # 키워드당 5건
                item = parse_item(e, f"Google News ({query[:15]})", category)
                
                # 오래된 기사 제외
                if item["published"] and item["published"] < cutoff:
                    continue
                
                items.append(item)
        except Exception as ex:
            print(f"[WARN] '{query}' 실패: {ex}")
    
    return items


def dedupe_by_title(items, threshold=0.75):
    """제목 유사도로 중복 제거"""
    from difflib import SequenceMatcher
    
    kept = []
    for item in items:
        title = item["title"]
        is_dup = False
        for k in kept:
            if SequenceMatcher(None, title, k["title"]).ratio() >= threshold:
                is_dup = True
                break
        if not is_dup:
            kept.append(item)
    return kept


def fetch_all():
    """국내 + 해외 연예 뉴스 전체 수집"""
    print("🎬 연예 뉴스 수집 시작...")
    
    all_items = []
    
    # 국내 연예
    print("\n[국내 연예]")
    korean_items = fetch_google_news(KOREAN_ENTERTAINMENT_QUERIES, is_korean=True)
    print(f"  수집: {len(korean_items)}건")
    all_items.extend(korean_items)
    
    # 해외 월드 스타
    print("\n[해외 월드 스타]")
    global_items = fetch_google_news(GLOBAL_CELEBRITY_QUERIES, is_korean=False)
    print(f"  수집: {len(global_items)}건")
    all_items.extend(global_items)
    
    # 중복 제거
    print(f"\n[중복 제거 전] {len(all_items)}건")
    all_items = dedupe_by_title(all_items, threshold=0.75)
    print(f"[중복 제거 후] {len(all_items)}건")
    
    # 카테고리별 통계
    korean_count = sum(1 for i in all_items if i["category"] == "korean")
    global_count = sum(1 for i in all_items if i["category"] == "global")
    print(f"\n✅ 최종: 국내 {korean_count}건 + 해외 {global_count}건 = 총 {len(all_items)}건")
    
    return all_items
