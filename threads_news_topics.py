"""
Threads 콘텐츠 소재용 뉴스 수집 - 23개 아이템별 어그로 키워드
- 평일 23일에 1:1 매칭
- Food & Drink 카테고리 제외
- 영어 70% + 한국어 30%
"""

TOPICS = {
    # 🚗 Transportation
    "Airport Taxi": {
        "icon": "🚕",
        "color": "#3b82f6",
        "category": "Transportation",
        "keywords": [
            "Korea airport taxi scam",
            "Incheon airport taxi rip off",
            "Seoul airport transfer cost",
            "Korea airport taxi vs subway",
            "Korea airport taxi cheap alternative",
            "한국 공항 택시 바가지",
            "인천공항 택시 사기",
        ],
    },
    "Car Rental": {
        "icon": "🚗",
        "color": "#3b82f6",
        "category": "Transportation",
        "keywords": [
            "Korea car rental scam",
            "Seoul rental car hidden fee",
            "Korea car rental foreigner license",
            "Korea car rental tips warning",
            "Korea driving foreigner regret",
            "한국 렌터카 외국인 바가지",
            "한국 렌터카 함정",
        ],
    },
    "Shuttle Bus": {
        "icon": "🚌",
        "color": "#3b82f6",
        "category": "Transportation",
        "keywords": [
            "Korea shuttle bus foreigner discount",
            "Seoul shuttle bus secret",
            "Korea airport bus tips",
            "Korea express bus tourist deal",
            "Korea bus pass foreigner",
            "외국인 한정 버스 할인",
            "한국 시외버스 외국인 혜택",
        ],
    },
    "KTX Train": {
        "icon": "🚄",
        "color": "#3b82f6",
        "category": "Transportation",
        "keywords": [
            "KTX foreigner pass discount",
            "KTX vs SRT price difference",
            "Korea Rail Pass scam",
            "KTX tourist mistake",
            "KTX cheaper than flight Korea",
            "외국인 KTX 패스 할인",
            "한국 기차 외국인 혜택",
        ],
    },
    
    # 💄 Eyewear & Beauty
    "Eyewear": {
        "icon": "👓",
        "color": "#ec4899",
        "category": "Eyewear & Beauty",
        "keywords": [
            "Korea glasses cheap foreigner",
            "Seoul eyewear price shock",
            "Korea contact lens foreigner",
            "Korean glasses vs US price",
            "Seoul optical shop foreigner",
            "한국 안경 외국 가격 차이",
            "외국인 한국 안경 후기",
        ],
    },
    "Hair Salon": {
        "icon": "💇",
        "color": "#ec4899",
        "category": "Eyewear & Beauty",
        "keywords": [
            "Korean hair salon foreigner experience",
            "Seoul hair salon rip off",
            "Korea hair perm foreigner price",
            "Seoul hair stylist English",
            "Korea hair coloring tourist",
            "한국 미용실 외국인 바가지",
            "외국인 한국 헤어샵 후기",
        ],
    },
    "Aesthetics": {
        "icon": "✨",
        "color": "#ec4899",
        "category": "Eyewear & Beauty",
        "keywords": [
            "Korea aesthetics clinic price",
            "Seoul skin treatment vs US cost",
            "Korea facial foreigner shock",
            "Seoul anti aging clinic",
            "Korea beauty clinic regret",
            "한국 피부관리실 가격 충격",
            "외국인 한국 에스테틱",
        ],
    },
    "Nail & Makeup": {
        "icon": "💅",
        "color": "#ec4899",
        "category": "Eyewear & Beauty",
        "keywords": [
            "Korea nail art foreigner",
            "Seoul makeup studio price",
            "Korea wedding makeup tourist",
            "Korean nail shop English",
            "Seoul makeup trend foreigner",
            "한국 네일 외국인 인기",
            "외국인 한국 메이크업 샵",
        ],
    },
    "Dermatology": {
        "icon": "🧴",
        "color": "#ec4899",
        "category": "Eyewear & Beauty",
        "keywords": [
            "Korean dermatology price shock",
            "Seoul botox half price foreigner",
            "Korea skin clinic vs US cost",
            "Seoul dermatologist tourist scam",
            "Korea laser treatment foreigner",
            "한국 피부과 외국인 가격",
            "한국 보톡스 외국인 후기",
        ],
    },
    "Color Analysis": {
        "icon": "🎨",
        "color": "#ec4899",
        "category": "Eyewear & Beauty",
        "keywords": [
            "Personal color analysis Seoul foreigner",
            "Korea color consulting English",
            "Seoul personal color experience",
            "Korea color analysis worth it",
            "Personal color Korea regret",
            "외국인 퍼스널 컬러 진단",
            "한국 퍼스널 컬러 외국인 후기",
        ],
    },
    
    # 📸 Snap & Experience
    "Street Snap": {
        "icon": "📷",
        "color": "#8b5cf6",
        "category": "Snap & Experience",
        "keywords": [
            "Seoul street snap photographer",
            "Korea snap photo tourist trap",
            "Seoul photo studio foreigner",
            "Korea wedding snap location",
            "Seoul Instagram spot regret",
            "외국인 한국 스냅 사진",
            "한국 스냅 촬영 외국인",
        ],
    },
    "Hanbok Rental": {
        "icon": "👘",
        "color": "#8b5cf6",
        "category": "Snap & Experience",
        "keywords": [
            "Hanbok rental scam foreigner",
            "Seoul Hanbok rental hidden fee",
            "Gyeongbokgung Hanbok rip off",
            "Bukchon Hanbok rental tips",
            "Hanbok rental regret",
            "외국인 한복 대여 바가지",
            "경복궁 한복 외국인 후기",
        ],
    },
    "K-Pop Class": {
        "icon": "🎤",
        "color": "#8b5cf6",
        "category": "Snap & Experience",
        "keywords": [
            "K-pop dance class Seoul scam",
            "Seoul K-pop class beginner regret",
            "Korea K-pop training foreigner",
            "K-pop class worth it tourist",
            "Seoul dance studio tourist trap",
            "외국인 K-Pop 댄스 클래스",
            "K-Pop 클래스 외국인 후기",
        ],
    },
    "Cooking Class": {
        "icon": "🍳",
        "color": "#8b5cf6",
        "category": "Snap & Experience",
        "keywords": [
            "Korean cooking class foreigner regret",
            "Seoul cooking class tourist trap",
            "Korean kimchi class authentic",
            "Korea cooking class English worth",
            "Seoul food class foreigner price",
            "외국인 한식 쿠킹 클래스",
            "한국 요리 클래스 외국인",
        ],
    },
    
    "Museum": {
        "icon": "🏛️",
        "color": "#10b981",
        "category": "Tours & Tickets",
        "keywords": [
            "Seoul museum free foreigner",
            "Korea museum hidden gem",
            "Seoul museum English guide",
            "Korea museum tourist mistake",
            "Korea National Museum foreigner",
            "외국인 한국 박물관 무료",
            "한국 박물관 외국인 추천",
        ],
    },
    "Theme Park": {
        "icon": "🎢",
        "color": "#10b981",
        "category": "Tours & Tickets",
        "keywords": [
            "Everland vs Lotte World foreigner",
            "Korea theme park discount tourist",
            "Seoul theme park rip off",
            "Korea amusement park foreigner price",
            "Everland tourist mistake",
            "외국인 에버랜드 할인",
            "외국인 롯데월드 가격",
        ],
    },
    "Guided Tour": {
        "icon": "🗺️",
        "color": "#10b981",
        "category": "Tours & Tickets",
        "keywords": [
            "Korea private tour guide scam",
            "Seoul tour guide rip off",
            "DMZ tour comparison foreigner",
            "Korea guided tour worth it",
            "Seoul walking tour regret",
            "한국 가이드 투어 외국인 바가지",
            "외국인 한국 가이드 투어 후기",
        ],
    },
    
    # 🧳 Travel Essentials
    "Luggage Storage": {
        "icon": "🧳",
        "color": "#6366f1",
        "category": "Travel Essentials",
        "keywords": [
            "Korea luggage storage cheap",
            "Seoul station luggage locker",
            "Korea baggage storage foreigner",
            "Seoul luggage delivery service",
            "Korea airport luggage storage",
            "외국인 한국 짐 보관",
            "한국 코인락커 외국인",
        ],
    },
    "SIM / eSIM": {
        "icon": "📱",
        "color": "#6366f1",
        "category": "Travel Essentials",
        "keywords": [
            "Korea SIM card scam foreigner",
            "Korea eSIM vs SIM cheaper",
            "Seoul SIM card airport rip off",
            "Korea data plan tourist regret",
            "Korea SIM card free deal",
            "외국인 한국 SIM 바가지",
            "한국 eSIM 외국인 후기",
        ],
    },
    "Currency Exchange": {
        "icon": "💱",
        "color": "#6366f1",
        "category": "Travel Essentials",
        "keywords": [
            "Korea currency exchange best rate",
            "Seoul Myeongdong exchange scam",
            "Korea airport exchange rate rip off",
            "Korea ATM foreigner fee",
            "Korea money exchange tips",
            "외국인 한국 환전 바가지",
            "한국 환전 최저가",
        ],
    },
    "Medical Translation": {
        "icon": "🏥",
        "color": "#6366f1",
        "category": "Travel Essentials",
        "keywords": [
            "Korea hospital English service",
            "Seoul medical translation foreigner",
            "Korea emergency room tourist",
            "Korea medical tourism scam",
            "Seoul international clinic price",
            "외국인 한국 병원 통역",
            "한국 의료 통역 외국인",
        ],
    },
    "Oriental Clinic": {
        "icon": "🌿",
        "color": "#6366f1",
        "category": "Travel Essentials",
        "keywords": [
            "Korea oriental medicine foreigner",
            "Seoul Korean medicine clinic English",
            "Korea acupuncture tourist worth it",
            "Korean herbal medicine foreigner regret",
            "Seoul hanbang clinic price",
            "외국인 한방 진료",
            "한국 한의원 외국인",
        ],
    },
}


def get_all_topics():
    """모든 23개 토픽 이름 반환"""
    return list(TOPICS.keys())


def get_topic_config(topic):
    """토픽 정보 반환 (아이콘, 색, 키워드 등)"""
    return TOPICS.get(topic, {})


def get_topic_keywords(topic):
    """토픽의 모든 키워드 반환"""
    config = TOPICS.get(topic, {})
    return config.get("keywords", [])


def get_today_topic():
    """오늘의 토픽 결정 - 평일 23일 1:1 매칭"""
    from datetime import datetime
    
    # 오늘이 평일이 아니면 None (주말 발송 안 함)
    weekday = datetime.now().weekday()
    if weekday >= 5:  # 토(5), 일(6)
        return None
    
    # 월의 N번째 평일 계산
    day = datetime.now().day
    # 간단한 매핑: 일자 % 23으로 순환
    topics = get_all_topics()
    topic_index = (day - 1) % len(topics)
    return topics[topic_index]
