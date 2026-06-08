from bs4 import BeautifulSoup
from difflib import SequenceMatcher

def clean_html(text: str, limit: int = 180) -> str:
    soup = BeautifulSoup(text or "", "html.parser")
    txt = soup.get_text(" ", strip=True)
    return (txt[:limit] + "…") if len(txt) > limit else txt

def similar(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

def dedupe(items, threshold: float = 0.65):
    """제목 유사도 기반 중복 제거 (더 엄격)"""
    kept = []
    for it in items:
        if any(similar(it["title"], k["title"]) >= threshold for k in kept):
            continue
        kept.append(it)
    return kept

def score(item, keywords):
    s = 0
    title = item["title"]
    summary = item.get("summary") or ""
    for kw in keywords:
        if kw in title:
            s += 3
        elif kw in summary:
            s += 1
    if item.get("published"):
        s += 1
    # 본문이 충실하면 가산점
    if len(summary) > 200:
        s += 2
    return s

def is_blocked(item, block_keywords, spam_phrases):
    """부정 키워드 + 광고성 키워드 차단"""
    title = item["title"]
    summary = item.get("summary") or ""
    # 부정 키워드
    if any(kw in title for kw in block_keywords):
        return True
    if any(kw in summary[:100] for kw in block_keywords):
        return True
    # 광고성 (제목)
    if any(phrase in title for phrase in spam_phrases):
        return True
    return False

def is_too_short(item, min_length):
    """본문이 너무 짧은 기사 제외"""
    summary = (item.get("summary") or "").strip()
    return len(summary) < min_length

def curate_by_category(items, keywords, block_keywords, spam_phrases, 
                       min_length, dedupe_threshold, quota):
    # 1. 부정 키워드 + 광고성 차단
    items = [it for it in items if not is_blocked(it, block_keywords, spam_phrases)]
    
    # 2. 너무 짧은 기사 제외
    items = [it for it in items if not is_too_short(it, min_length)]
    
    # 3. 정제 + 점수 계산
    for it in items:
        it["summary"] = clean_html(it.get("summary", ""))
        it["_score"] = score(it, keywords)
    
    # 4. 카테고리별 분리
    by_cat = {cat: [] for cat in quota.keys()}
    for it in items:
        cat = it.get("category")
        if cat in by_cat:
            by_cat[cat].append(it)
    
    # 5. 각 카테고리에서 점수순 정렬 + 중복 제거 + 쿼터만큼 선택
    result = {}
    for cat, cat_items in by_cat.items():
        cat_items.sort(key=lambda x: (x["_score"], x.get("published") or 0), reverse=True)
        cat_items = dedupe(cat_items, dedupe_threshold)
        result[cat] = cat_items[:quota[cat]]
    
    return result
