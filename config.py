import os

# 이메일 설정
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")
MAIL_FROM = os.environ.get("SMTP_USER", "")
MAIL_TO   = [os.environ.get("MAIL_TO", "")]

# Claude API 키
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# Google 뉴스 RSS 빌더
def gnews(query, lang="ko"):
    from urllib.parse import quote
    if lang == "ko":
        return f"https://news.google.com/rss/search?q={quote(query)}&hl=ko&gl=KR&ceid=KR:ko"
    else:
        return f"https://news.google.com/rss/search?q={quote(query)}&hl=en-US&gl=US&ceid=US:en"

# RSS 소스
FEEDS = {
    "창업·아이디어": [
        gnews("스타트업 창업"),
        gnews("신규 비즈니스"),
        gnews("AI 서비스 출시"),
        gnews("1인 창업"),
        gnews("사이드 프로젝트"),
        gnews("노코드 창업"),
        gnews("바이브 코딩"),
        gnews("SaaS 출시"),
        gnews("D2C 브랜드"),
        gnews("구독 서비스"),
        "https://platum.kr/feed",
        "https://www.venturesquare.net/feed",
    ],
    "방한외국인": [
        gnews("외국인 관광객 한국"),
        gnews("방한 관광객"),
        gnews("K-콘텐츠 인기"),
        gnews("한류 트렌드"),
        gnews("인바운드 관광"),
        gnews("외국인 서울 여행"),
        gnews("외국인 한복 체험"),
        gnews("K-뷰티 외국인"),
        gnews("Korea travel trend", lang="en"),
        gnews("Seoul tourism foreigners", lang="en"),
        gnews("visit Korea experience", lang="en"),
    ],
    "사회·경제": [
        gnews("정부 지원금 창업"),
        gnews("관광 산업 정책"),
        gnews("스타트업 지원"),
        gnews("관광공사"),
        "https://www.yna.co.kr/rss/economy.xml",
    ],
}

# 카테고리별 개수
CATEGORY_QUOTA = {
    "창업·아이디어": 10,
    "방한외국인": 5,
    "사회·경제": 5,
}

# 70/20/10 비율
INNOVATION_RATIO = {
    "Core": 0.7,           # 즉시 실행 (바이브 코딩 1주 이내)
    "Adjacent": 0.2,       # 1~3개월 확장
    "Transformative": 0.1, # 6개월+ 큰 베팅
}

# 피글맵스 컨텍스트 (AI에게 전달할 사업 정보)
PIGLEMAPS_CONTEXT = """
피글맵스(pglemaps.com)는 방한 외국인 관광객 대상 서비스입니다.

현재 수익 모델:
- 한복 체험, K-뷰티 시술, 각종 액티비티의 어필리에이트 커미션
- 외국인이 체험 예약 시 수수료 수익

핵심 기능 (무료):
- 가고 싶은 장소를 담으면 최적 동선 자동 생성
- 외국인 친화적 UX (다국어, 결제 등)

축적되는 데이터 자산:
- 외국인 관광객의 선호 동선
- 카테고리별 인기 액티비티
- 지역별 방문 트렌드
- 다국적 사용자 행동 패턴

확장 가능성:
- 동선 데이터를 활용한 신규 수익 모델 개발 가능
- B2B (관광 사업자 대상) 데이터/광고 모델
- 추천 알고리즘 고도화
- 콘텐츠/커뮤니티 확장
"""

KEYWORDS_BOOST = [
    # 창업·바이브 코딩
    "AI", "생성형", "노코드", "바이브 코딩", "사이드 프로젝트",
    "1인", "솔로", "창업", "스타트업", "런칭", "출시", "MVP",
    "구독", "SaaS", "D2C", "이커머스", "리테일",
    # 방한 외국인
    "외국인", "방한", "관광객", "인바운드", "한류", "K-",
    "한복", "K-뷰티", "액티비티", "체험", "서울", "여행",
    "Seoul", "Korea", "Korean", "tourism", "tourist",
    # 정부·관광산업
    "지원금", "정책", "관광공사", "문화체육관광부",
]

KEYWORDS_BLOCK = [
    "프로야구", "축구", "농구", "배구", "올림픽",
    "연예", "드라마 개봉", "영화 개봉", "아이돌 컴백",
    "사망", "별세", "부고",
]

MAX_ITEMS = 20
