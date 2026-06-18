"""
News Report - 데이터 수집기 (슬림 버전)
- BetaList (신규 서비스 발견)
- Indie Hackers (수익화 아이디어)
- Hacker News Show HN (개발자 프로젝트)
- Product Hunt (도구 + AI)
"""

import feedparser
from datetime import datetime, timedelta, timezone
from dateutil import parser as dtparser


# RSS 소스 정의
SOURCES = {
    "betalist": {
        "name": "BetaList",
        "url": "https://betalist.com/feed",
        "category": "betalist",
        "icon": "🚀",
    },
    "indie_hackers": {
        "name": "Indie Hackers",
        "url": "https://www.indiehackers.com/feed.xml",
        "category": "monetize",
        "icon": "💰",
    },
    "show_hn": {
        "name": "Hacker News - Show HN",
        "url": "https://hnrss.org/show",
        "category": "monetize",
        "icon": "🔨",
    },
    "product_hunt": {
        "name": "Product Hunt",
        "url": "https://www.producthunt.com/feed",
        "category": "monetize",
        "icon": "⚡",
    },
}


def fetch_source(source_key, hours=48):
    """단일 RSS 소스에서 기사 수집
    
    Args:
        source_key: SOURCES의 키
        hours: 최근 N시간 이내 (기본 48시간 = 2일)
    """
    source = SOURCES.get(source_key)
    if not source:
        return []
    
    url = source["url"]
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    items = []
    
    try:
        d = feedparser.parse(url)
        for e in d.entries[:20]:  # 소스당 최대 20건
            # 발행일 파싱
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
            
            # 너무 오래된 기사 제외
            if pub and pub < cutoff:
                continue
            
            items.append({
                "source": source["name"],
                "source_key": source_key,
                "category": source["category"],
                "icon": source["icon"],
                "title": (e.get("title") or "").strip(),
                "link": e.get("link", ""),
                "summary": (e.get("summary") or "").strip(),
                "published": pub,
            })
        
        print(f"  {source['name']}: {len(items)}건 수집")
    except Exception as ex:
        print(f"[WARN] {source['name']} 수집 실패: {ex}")
    
    return items


def fetch_all():
    """모든 소스에서 수집"""
    print("📰 RSS 수집 시작...")
    
    all_items = []
    for source_key in SOURCES.keys():
        items = fetch_source(source_key)
        all_items.extend(items)
    
    print(f"✅ 총 {len(all_items)}건 수집")
    return all_items
