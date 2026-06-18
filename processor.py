"""
데이터 처리기 - 카테고리별 그룹화 + 중복 제거
"""

from difflib import SequenceMatcher


def similar(a, b):
    """제목 유사도 (0~1)"""
    return SequenceMatcher(None, a, b).ratio()


def dedupe(items, threshold=0.7):
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


def group_by_category(items):
    """카테고리별 그룹화"""
    groups = {
        "betalist": [],
        "monetize": [],
    }
    
    for item in items:
        cat = item.get("category", "")
        if cat in groups:
            groups[cat].append(item)
    
    return groups


def process(items):
    """전체 처리 흐름"""
    print("🔧 데이터 처리 중...")
    
    # 중복 제거
    items = dedupe(items, threshold=0.7)
    print(f"  중복 제거 후: {len(items)}건")
    
    # 카테고리별 그룹화
    grouped = group_by_category(items)
    
    for cat, cat_items in grouped.items():
        print(f"  {cat}: {len(cat_items)}건")
    
    return grouped
