"""
News Report - 데이터 수집기 (7개 카테고리)
- BetaList, 수익화, 방한외국인, 정부정책, 관광업계, 어필리에이트, 외국인비즈니스
"""

import feedparser
from urllib.parse import quote
from datetime import datetime, timedelta, timezone
from dateutil import parser as dtparser


# RSS 소스 정의
SOURCES = {
    # 1. BetaList
    "betalist": {
        "name": "BetaList",
        "url": "https://betalist.com/feed",
        "category": "betalist",
        "type": "rss",
    },
    
    # 2. 수익화 아이디어
    "indie_hackers": {
        "name": "Indie Hackers",
        "url": "https://www.indiehackers.com/feed.xml",
        "category": "monetize",
        "type": "rss",
    },
    "show_hn": {
        "name": "Hacker News - Show HN",
        "url": "https://hnrss.org/show",
        "category": "monetize",
        "type": "rss",
    },
    "product_hunt": {
        "name": "Product Hunt",
        "url": "https://www.producthunt.com/feed",
        "category": "monetize",
        "type": "rss",
    },
}


# Google News 검색 키워드 (카테고리별)
GOOGLE_NEWS_QUERIES = {
    "inbound_tourism": {
        "category": "inbound_tourism",
        "queries_ko": [
            "방한 외국인 관광객",
            "외국인 한국 여행 트렌드",
            "K관광 통계",
            "외국인 한국 방문",
            "인바운드 관광",
        ],
        "queries_en": [
            "South Korea tourism statistics",
            "foreigners visiting Korea trend",
            "Korea inbound tourism 2026",
        ],
    },
    
    "gov_policy": {
        "category": "gov_policy",
        "queries_ko": [
            "K-Startup 외국인 지원",
            "관광 스타트업 지원금",
            "중소벤처기업부 외국인 관광",
            "한국관광공사 지원사업",
            "외국인 대상 정부 지원",
        ],
        "queries_en": [],
    },
    
    "tourism_industry": {
        "category": "tourism_industry",
        "queries_ko": [
            "한국 관광 업계 동향",
            "한국 여행 플랫폼 트렌드",
            "Klook Korea",
            "Trip.com 한국",
            "관광 스타트업 한국",
        ],
        "queries_en": [
            "Korea travel industry trend",
            "Klook Trip.com Korea",
        ],
    },
    
    "affiliate": {
        "category": "affiliate",
        "queries_ko": [
            "어필리에이트 마케팅 한국",
            "제휴 마케팅 성공 사례",
            "한국 어필리에이트 플랫폼",
            "쿠팡 파트너스 사례",
        ],
        "queries_en": [
            "affiliate marketing case study",
            "travel affiliate Korea",
        ],
    },
    
    "foreigner_business": {
        "category": "foreigner_business",
        "queries_ko": [
            "외국인 대상 한국 마케팅",
            "K뷰티 외국인 마케팅",
            "한국 외국인 타겟 비즈니스",
            "외국인 한국 쇼핑 트렌드",
        ],
        "queries_en": [
            "Korean brand foreigner marketing",
            "K-beauty foreigner tourists",
        ],
    },
}


def is_korean(text):
    """한국어 키워드 판별"""
    for char in text:
        if '\uac00' <= char <= '\ud7a3':
            return True
    return False


def build_gnews_url(query):
    """Google News RSS URL"""
    if is_korean(query):
        return f"https://news.google.com/rss/search?q={quote(query)}&hl=ko&gl=KR&ceid=KR:ko"
    else:
        return f"https://news.google.com/rss/search?q={quote(query)}&hl=en-US&gl=US&ceid=US:en"


def parse_item(entry, source_name, category):
    """RSS 엔트리 파싱"""
    # 발행일 파싱
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
        "source": source_name,
        "category": category,
        "title": (entry.get("title") or "").strip(),
        "link": entry.get("link", ""),
        "summary": (entry.get("summary") or "").strip(),
        "published": pub,
    }


def fetch_rss_source(source_key, hours=48):
    """단일 RSS 소스 수집"""
    source = SOURCES.get(source_key)
    if not source:
        return []
    
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    items = []
    
    try:
        d = feedparser.parse(source["url"])
        for e in d.entries[:20]:
            item = parse_item(e, source["name"], source["category"])
            
            # 오래된 거 제외
            if item["published"] and item["published"] < cutoff:
                continue
            
            items.append(item)
        
        print(f"  {source['name']}: {len(items)}건")
    except Exception as ex:
        print(f"[WARN] {source['name']} 실패: {ex}")
    
    return items


def fetch_gnews_category(category_key, hours=72):
    """Google News 카테고리별 수집"""
    config = GOOGLE_NEWS_QUERIES.get(category_key)
    if not config:
        return []
    
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    items = []
    
    all_queries = config.get("queries_ko", []) + config.get("queries_en", [])
    
    for query in all_queries:
        try:
            url = build_gnews_url(query)
            d = feedparser.parse(url)
            for e in d.entries[:5]:  # 키워드당 5건
                item = parse_item(e, f"Google News ({query[:20]})", config["category"])
                
                if item["published"] and item["published"] < cutoff:
                    continue
                
                items.append(item)
        except Exception as ex:
            print(f"[WARN] '{query}' 실패: {ex}")
    
    print(f"  {category_key}: {len(items)}건 수집")
    return items


def fetch_all():
    """모든 소스에서 수집"""
    print("📰 RSS + Google News 수집 시작...")
    
    all_items = []
    
    # 1. RSS 소스 (BetaList, 수익화 3개 소스)
    print("\n[RSS 소스]")
    for source_key in SOURCES.keys():
        items = fetch_rss_source(source_key)
        all_items.extend(items)
    
    # 2. Google News 카테고리별 검색
    print("\n[Google News 카테고리별]")
    for category_key in GOOGLE_NEWS_QUERIES.keys():
        items = fetch_gnews_category(category_key)
        all_items.extend(items)
    
    print(f"\n✅ 총 {len(all_items)}건 수집")
    return all_items
