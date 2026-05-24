from bs4 import BeautifulSoup
from difflib import SequenceMatcher

def clean_html(text: str, limit: int = 160) -> str:
    soup = BeautifulSoup(text or "", "html.parser")
    txt = soup.get_text(" ", strip=True)
    return (txt[:limit] + "…") if len(txt) > limit else txt

def similar(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

def dedupe(items, threshold: float = 0.75):
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
            s += 3  # 제목에 있으면 3점
        elif kw in summary:
            s += 1
    if item.get("published"):
        s += 1
    return s

def is_blocked(item, block_keywords):
    title = item["title"]
    return any(kw in title for kw in block_keywords)

def curate_by_category(items, keywords, block_keywords, quota):
    # 1. 부정 키워드 차단
    items = [it for it in items if not is_blocked(it, block_keywords)]
    
    # 2. 정제 + 점수 계산
    for it in items:
        it["summary"] = clean_html(it.get("summary", ""))
        it["_score"] = score(it, keywords)
    
    # 3. 카테고리별로 분리
    by_cat = {cat: [] for cat in quota.keys()}
    for it in items:
        cat = it.get("category")
        if cat in by_cat:
            by_cat[cat].append(it)
    
    # 4. 각 카테고리에서 점수순 정렬 + 중복 제거 + 쿼터만큼 선택
    result = {}
    for cat, cat_items in by_cat.items():
        cat_items.sort(key=lambda x: (x["_score"], x.get("published") or 0), reverse=True)
        cat_items = dedupe(cat_items)
        result[cat] = cat_items[:quota[cat]]
    
    return result