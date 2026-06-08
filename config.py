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

def gnews(query, lang="ko"):
    from urllib.parse import quote
    if lang == "ko":
        return f"https://news.google.com/rss/search?q={quote(query)}&hl=ko&gl=KR&ceid=KR:ko"
    else:
        return f"https://news.google.com/rss/search?q={quote(query)}&hl=en-US&gl=US&ceid=US:en"

# RSS 소스
FEEDS = {
    "오늘의출시도구": [
        "https://www.producthunt.com/feed",
    ],
    "사이드프로젝트": [
        "https://hnrss.org/show",
        "https://www.indiehackers.com/feed.xml",
    ],
    "외국인마케팅성공사례": [
        gnews("외국인 마케팅 성공"),
        gnews("인바운드 마케팅 사례"),
        gnews("관광 마케팅 캠페인"),
        gnews("K-마케팅 해외"),
        gnews("외국인 고객 유치 성공"),
        gnews("inbound tourism marketing success", lang="en"),
        gnews("Korea brand marketing case", lang="en"),
        gnews("Seoul tourism campaign", lang="en"),
    ],
    "방한외국인": [
        gnews("외국인 관광객 한국"),
        gnews("방한 관광객 증가"),
        gnews("외국인 한복 체험"),
        gnews("K-뷰티 외국인 인기"),
        gnews("외국인 서울 핫플레이스"),
        gnews("한국 여행 트렌드"),
        gnews("Korea travel trend foreigners", lang="en"),
        gnews("Seoul tourism foreigners", lang="en"),
        gnews("visit Korea experience", lang="en"),
    ],
    "정부지원금": [
        gnews("관광 스타트업 지원금"),
        gnews("창업 지원사업 모집"),
        gnews("관광공사 지원사업"),
        gnews("중기부 지원사업"),
        gnews("문체부 관광 지원"),
        gnews("청년 창업 지원금"),
        gnews("외국인 관광 지원사업"),
        gnews("K-스타트업 지원"),
    ],
}

# 카테고리별 개수 (총 25건)
CATEGORY_QUOTA = {
    "오늘의출시도구": 5,
    "사이드프로젝트": 5,
    "외국인마케팅성공사례": 5,
    "방한외국인": 5,
    "정부지원금": 5,
}

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
    "AI", "GPT", "Claude", "automation", "tool", "app",
    "launched", "build", "side project", "indie", "MVP",
    "성공", "캠페인", "사례", "마케팅", "브랜딩", "전환율",
    "고객 유치", "바이럴", "성과",
    "외국인", "방한", "관광객", "인바운드", "한류", "K-",
    "한복", "K-뷰티", "체험", "서울 여행", "Korea", "Seoul",
    "지원금", "지원사업", "모집", "공고", "선정", "보조금",
    "관광공사", "중기부", "문체부", "창업지원",
]

KEYWORDS_BLOCK = [
    "프로야구", "축구", "농구", "배구", "올림픽", "월드컵",
    "KBO", "K리그", "MLB", "NBA",
    "연예", "드라마 개봉", "영화 개봉", "아이돌 컴백", "OST",
    "결혼", "이혼", "열애",
    "사망", "별세", "부고", "유언", "추모", "장례",
    "여당", "야당", "당대표", "대선", "총선", "탄핵",
    "[광고]", "[홍보]",
    "아파트 분양", "오피스텔", "재개발",
]

SPAM_PHRASES = [
    "[광고]", "[홍보]", "PR", "협찬",
    "스폰서드", "AD)",
]

MAX_ITEMS = 25
MIN_SUMMARY_LENGTH = 30
DEDUPE_THRESHOLD = 0.65
