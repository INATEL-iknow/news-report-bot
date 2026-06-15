"""
외국인 시점 어그로 가능한 뉴스 검색 키워드 풀
- 5개 카테고리 (가격충격/사기/인사이더/후회/혜택)에 매핑되는 키워드
- 영어 + 한국어 혼합
- Google News에서 진짜 검증 가능한 정보 잡기 위한 키워드
"""

KEYWORDS = {
    # 💰 가격/비용 충격
    "price_shock": [
        # 영어
        "Korea botox price foreigner",
        "Korea LASIK cost cheaper",
        "Korea medical tourism price",
        "Korea cosmetic surgery cost comparison",
        "Korea dental implant price foreigner",
        # 한국어
        "외국인 한국 의료관광 가격",
        "한국 의료비 외국 비교",
        "외국인 K-뷰티 가격 시술",
    ],
    
    # ⚠️ 사기/바가지/함정
    "scams": [
        # 영어
        "Korea tourist scam",
        "Seoul taxi rip off",
        "Korea overcharge foreigner",
        "Myeongdong tourist trap",
        "Korea fake product foreigner",
        # 한국어
        "외국인 관광객 바가지",
        "외국인 사기 한국",
        "외국인 택시 바가지 공항",
    ],
    
    # 🤫 한국인만 아는 정보
    "insider": [
        # 영어
        "Korean local restaurant Seoul hidden",
        "Korea where locals go",
        "Seoul beyond tourist spots",
        "Korean only place foreigner",
        "Seoul authentic Korean experience",
        # 한국어 - 보도자료/리뷰 잡기 좋은 키워드
        "한국인 외국인 추천 맛집",
        "외국인 모르는 한국 명소",
        "한국인이 가는 카페 외국인",
    ],
    
    # 😅 외국인 후회/실수
    "regrets": [
        # 영어
        "Korea travel mistake foreigner",
        "Seoul tourist regret",
        "Korea wish I knew",
        "Korea travel tips first time",
        "Korea culture shock foreigner",
        # 한국어
        "외국인 한국 여행 후회",
        "외국인 한국 실수",
        "외국인 첫 한국 방문 어려움",
    ],
    
    # 🎁 시간 한정 혜택/특별
    "deals": [
        # 영어
        "Korea tourism discount 2026",
        "Korea foreigner free service",
        "Visit Korea promotion",
        "Korea Tourism Organization deal",
        "KTO foreigner benefit",
        # 한국어 - 정부 정책 잡기 좋은 키워드 (제일 강함!)
        "외국인 관광객 할인 정부",
        "한국관광공사 외국인 프로모션",
        "외국인 한정 무료 한국",
        "방한 외국인 혜택",
        "외국인 무료 K-체험",
    ],
}


def get_all_keywords():
    """모든 키워드 + 카테고리 정보 반환"""
    result = []
    for category, kw_list in KEYWORDS.items():
        for kw in kw_list:
            result.append({
                "category": category,
                "keyword": kw,
            })
    return result


def get_keywords_by_category(category):
    """특정 카테고리 키워드만"""
    return KEYWORDS.get(category, [])
