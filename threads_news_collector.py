"""
Threads 콘텐츠용 뉴스 수집기 (개선 버전)
- threads_news_keywords의 키워드 풀로 매일 자동 수집
- Google News RSS 활용 (무료, 인증 없음)
- 한국어 + 영어 동시 수집
- 중복 제거
"""

import feedparser
from urllib.parse import quote
from datetime import datetime, timedelta, timezone
from dateutil import parser as dtparser
from difflib import SequenceMatcher

from threads_news_keywords import get_all_keywords


def is_korean(text):
    """한국어 키워드 판별"""
    for char in text:
        if '\uac00' <= char <= '\ud7a3':
            return True
    return False


def build_gnews_url(query):
    """Google News RSS URL 생성"""
    if is_korean(query):
        return f"https://news.google.com/rss/search?q={quote(query)}&hl=ko&gl=KR&ceid=KR:ko"
    else:
        return f"https://news.google.com/rss/search?q={quote(query)}&hl=en-US&gl=US&ceid=US:en"


def fetch_news_for_keyword(keyword, category, hours=168):
    """단일 키워드로 뉴스 수집
    
    Args:
        keyword: 검색어
        category: price_shock / scams / insider / regrets / deals
        hours: 몇 시간 이내 기사 (168시간 = 7일)
    """
    url = build_gnews_url(keyword)
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    items = []
    
    try:
        d = feedparser.parse(url)
        for e in d.entries[:8]:  # 키워드당 최대 8건
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
                "category": category,
                "keyword": keyword,
                "title": (e.get("title") or "").strip(),
                "link": e.get("link", ""),
                "summary": (e.get("summary") or "").strip(),
                "published": pub,
                "source": d.feed.get("title", ""),
                "lang": "ko" if is_korean(keyword) else "en",
            })
    except Exception as ex:
        print(f"[WARN] '{keyword}' 수집 실패: {ex}")
    
    return items


def similar(a, b):
    """제목 유사도 (0~1)"""
    return SequenceMatcher(None, a, b).ratio()


def dedupe_news(items, threshold=0.7):
    """중복 기사 제거"""
    kept = []
    for item in items:
        is_dup = False
        for k in kept:
            if similar(item["title"], k["title"]) >= threshold:
                is_dup = True
                break
        if not is_dup:
            kept.append(item)
    return kept


def fetch_all_news():
    """모든 키워드로 뉴스 수집 + 중복 제거"""
    print(f"📰 뉴스 수집 시작...")
    
    all_keywords = get_all_keywords()
    print(f"  총 {len(all_keywords)}개 키워드")
    
    all_items = []
    for kw_data in all_keywords:
        items = fetch_news_for_keyword(
            kw_data["keyword"],
            kw_data["category"],
        )
        all_items.extend(items)
    
    print(f"  수집 결과: {len(all_items)}건")
    
    # 중복 제거
    deduped = dedupe_news(all_items, threshold=0.7)
    print(f"  중복 제거 후: {len(deduped)}건")
    
    # 최신순 정렬
    deduped.sort(
        key=lambda x: x.get("published") or datetime.min.replace(tzinfo=timezone.utc),
        reverse=True,
    )
    
    return deduped
