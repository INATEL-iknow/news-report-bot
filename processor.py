"""
데이터 처리기 - 7개 카테고리 그룹화 + 중복 제거
"""

from difflib import SequenceMatcher


# 7개 카테고리 정의
CATEGORIES = [
    "betalist",            # BetaList 신규 서비스
    "monetize",            # 수익화 아이디어
    "inbound_tourism",     # 방한 외국인 트렌드
    "gov_policy",          # 정부 정책/지원금
    "tourism_industry",    # 한국 관광 업계 동향
    "affiliate",           # 어필리에이트 사례
    "foreigner_business",  # 외국인 대상 한국 비즈니스
]


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
    groups = {cat: [] for cat in CATEGORIES}
    
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
    
    print(f"\n[카테고리별 수집 결과]")
    for cat in CATEGORIES:
        count = len(grouped.get(cat, []))
        print(f"  {cat}: {count}건")
    
    return grouped
