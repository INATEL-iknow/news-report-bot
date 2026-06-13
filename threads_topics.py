"""
Threads 콘텐츠 주제 관리
- 요일별 카테고리 결정
- 주제 풀에서 오늘 주제 선택
"""

from datetime import datetime

# 요일별 카테고리 (0=월, 1=화, ..., 6=일)
WEEKDAY_CATEGORIES = {
    0: "Transportation",      # 월
    1: "Beauty & Aesthetics", # 화
    2: "Snap & Experience",   # 수
    3: "Food & Drink",        # 목
    4: "Tours & Tickets",     # 금
    5: "Travel Essentials",   # 토
    6: "Weekly Best",         # 일
}

# 카테고리별 주제 풀
TOPIC_POOL = {
    "Transportation": [
        "인천공항에서 서울 호텔까지, 외국인이 모르는 가장 똑똑한 이동 방법",
        "KTX vs SRT, 외국인이 골라야 할 진짜 이유",
        "한국에서 차 렌트할 때 외국인이 항상 놓치는 것",
        "공항 셔틀 vs 택시 vs 지하철, 진짜 가성비 비교",
        "카카오T 외국인 모드로 택시 5분 안에 잡는 법",
    ],
    "Beauty & Aesthetics": [
        "한국 피부과, 압구정 말고 한국 여자들이 진짜 가는 동네",
        "퍼스널 컬러 분석, 외국인이 받을 수 있는 진짜 좋은 곳",
        "성수동 헤어샵 vs 청담동 헤어샵, 외국인에게 진짜 맞는 곳",
        "네일아트, 인스타용이 아닌 한국 트렌드용 진짜 핫한 곳",
        "한국 안과(아이웨어)가 외국보다 5배 싼 진짜 이유",
        "한방 디톡스, 외국인이 받을 수 있는 진짜 효과 좋은 곳",
    ],
    "Snap & Experience": [
        "한복, 경복궁 앞 말고 사진이 진짜 예쁘게 나오는 곳",
        "K-Pop 댄스 클래스, 외국인 전용 vs 한국인 섞인 곳 진짜 추천",
        "스트리트 스냅, 인스타 외국인 인플루언서가 진짜 가는 동네",
        "한식 쿠킹 클래스, 진짜 한국 시어머니 손맛 배우는 곳",
        "한국 영화 촬영지 투어, 진짜 가볼만한 곳",
    ],
    "Food & Drink": [
        "명동 길거리 음식 말고, 한국인 회식 가는 진짜 노포 거리",
        "한국 와인바, 외국인이 모르는 진짜 핫한 곳",
        "한식당 가이드북 1순위 말고, 한국 직장인이 매일 가는 곳",
        "스타벅스 말고, 한국 카페가 진짜 다른 이유 보여주는 곳",
        "갈비집, 가이드북에 없지만 진짜 맛있는 동네",
        "한국 24시 콩나물국밥, 술 마신 다음날 한국인이 가는 곳",
    ],
    "Tours & Tickets": [
        "박물관 가이드 투어, 한국인 친구가 데려가는 곳",
        "에버랜드 vs 롯데월드, 외국인 입장에서 진짜 추천",
        "DMZ 투어, 진짜 좋은 가이드 회사 고르는 법",
        "서울 야경 투어, 남산 말고 진짜 인생샷 나오는 곳",
        "한옥마을 가이드 투어, 북촌 말고 진짜 한옥 골목",
    ],
    "Travel Essentials": [
        "한국 도착하자마자 사야 할 SIM 카드, 외국인이 항상 잘못 사는 것",
        "환전, 공항 환전소 말고 한국에서 진짜 좋은 환율",
        "짐 보관, 코인락커 말고 더 편한 방법",
        "한국 병원, 외국인이 받을 수 있는 의료 통역 서비스",
        "면세점에서 외국인 모르는 5% 할인 받는 법",
    ],
    "Weekly Best": [
        "이번 주 피글맵스에 가장 많이 저장된 장소 TOP 3",
        "오늘 한국 도착하는 외국인들이 가장 많이 찾는 것",
        "이번 달 가장 후회한 한국 여행 실수 TOP 3",
        "한국 여행 첫날 외국인이 가장 많이 잘못하는 실수",
        "한국 여행 일정 짤 때 외국인이 가장 많이 놓치는 것",
    ],
}


def get_today_category():
    """오늘의 카테고리 반환"""
    weekday = datetime.now().weekday()
    return WEEKDAY_CATEGORIES[weekday]


def get_today_topic(category, used_topics=None):
    """카테고리에서 오늘의 주제 1개 선택 (랜덤)"""
    import random
    
    topics = TOPIC_POOL.get(category, [])
    if not topics:
        return None
    
    # 사용한 주제 제외
    if used_topics:
        available = [t for t in topics if t not in used_topics]
        if not available:
            available = topics  # 다 썼으면 풀에서 재선택
    else:
        available = topics
    
    return random.choice(available)
