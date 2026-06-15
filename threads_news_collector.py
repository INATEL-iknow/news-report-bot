"""
Threads 콘텐츠 소재용 뉴스 수집기
- 23개 토픽 × 7개 키워드 = 약 161개 검색
- Google News RSS 활용 (무료, 인증 없음)
- 한국어 + 영어 동시 수집
- 중복 제거
"""

import feedparser
from urllib.parse import quote
from datetime import datetime, timedelta, timezone
from dateutil import parser as dtparser
from difflib import SequenceMatcher

from threads_news_topics import TOPICS


def is_korean(text):
    """한국어 키워드인지 판별"""
    for char in text:
        if '\uac00' <= char <= '\ud7a3':  # 한글 유니코드 범위
            return True
    return False


def build_gnews_url(query):
    """Google News RSS URL 생성 (한/영 자동 판별)"""
    if is_korean(query):
        return f"https://news.google.com/rss/search?q={quote(query)}&hl=ko&gl=KR&ceid=KR:ko"
    else:
        return f"https://news.google.com/rss/search?q={quote(query)}&hl=en-US&gl=US&ceid=US:en"


def fetch_topic_news(topic, hours=72):
    """특정 토픽의 모든 키워드로 뉴스 수집
    
    Args:
        topic: 토픽 이름 (예: "Airport Taxi")
        hours: 몇 시간 이내 기사만 수집 (기본 72시간 = 3일)
    """
    config = TOPICS.get(topic, {})
    keywords = config.get("keywords", [])
    
    if not keywords:
        print(f"[WARN] '{topic}' 키워드 없음")
        return []
    
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    items = []
    
    for keyword in keywords:
        url = build_gnews_url(keyword)
        try:
            d = feedparser.parse(url)
            for e in d.entries[:10]:  # 키워드당 최대 10건
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
                    "topic": topic,
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
    
    print(f"  {topic}: {len(items)}건 수집")
    return items


def similar(a, b):
    """두 문자열 유사도 (0~1)"""
    return SequenceMatcher(None, a, b).ratio()


def dedupe_news(items, threshold=0.7):
    """중복 기사 제거 (제목 유사도 기준)"""
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


def fetch_today_topic_news(topic):
    """오늘의 토픽 뉴스 수집 + 중복 제거"""
    print(f"📰 '{topic}' 뉴스 수집 시작...")
    
    items = fetch_topic_news(topic, hours=72)
    print(f"  중복 제거 전: {len(items)}건")
    
    items = dedupe_news(items, threshold=0.7)
    print(f"  중복 제거 후: {len(items)}건")
    
    # 최신순 정렬
    items.sort(
        key=lambda x: x.get("published") or datetime.min.replace(tzinfo=timezone.utc),
        reverse=True,
    )
    
    return items
