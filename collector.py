import feedparser
from datetime import datetime, timedelta, timezone
from dateutil import parser as dtparser

def fetch_all(feeds: dict, hours: int = 24):
    """최근 N시간 이내 기사만 수집"""
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