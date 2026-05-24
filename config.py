import os

# 이메일 설정 (환경변수에서 읽기 - 안전)
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")
MAIL_FROM = os.environ.get("SMTP_USER", "")
MAIL_TO   = [os.environ.get("MAIL_TO", "")]

# Google 뉴스 RSS 빌더
def gnews(query, lang="ko"):
    from urllib.parse import quote
    if lang == "ko":
        return f"https://news.google.com/rss/search?q={quote(query)}&hl=ko&gl=KR&ceid=KR:ko"
    else:
        return f"https://news.google.com/rss/search?q={quote(query)}&hl=en-US&gl=US&ceid=US:en"

# RSS 소스
FEEDS = {
    "마케팅": [
        gnews("마케팅 트렌드"),
        gnews("브랜드 캠페인"),
        gnews("광고 사례"),
        gnews("디지털 마케팅"),
        gnews("콘텐츠 마케팅"),
        gnews("소비자 트렌드"),
        "https://www.madtimes.org/rss/allArticle.xml",
        "https://www.the-pr.co.kr/rss/allArticle.xml",
    ],
    "스타트업·아이디어": [
        gnews("스타트업 창업"),
        gnews("신규 비즈니스"),
        gnews("AI 서비스 출시"),
        gnews("1인 창업"),
        gnews("사이드 프로젝트"),
        "https://platum.kr/feed",
        "https://www.venturesquare.net/feed",
    ],
    "인바운드·한국트렌드": [
        gnews("외국인 관광객 한국"),
        gnews("방한 관광객"),
        gnews("K-콘텐츠 인기"),
        gnews("한류 트렌드"),
        gnews("인바운드 관광"),
        gnews("외국인 서울 여행"),
        gnews("Korea travel trend", lang="en"),
        gnews("Seoul tourism foreigners", lang="en"),
        gnews("K-culture popular", lang="en"),
        gnews("visit Korea", lang="en"),
    ],
    "경제·사회": [
        "https://www.yna.co.kr/rss/economy.xml",
        "https://www.yna.co.kr/rss/society.xml",
    ],
}

CATEGORY_QUOTA = {
    "마케팅": 8,
    "스타트업·아이디어": 4,
    "인바운드·한국트렌드": 5,
    "경제·사회": 3,
}

KEYWORDS_BOOST = [
    "트렌드", "인사이트", "캠페인", "광고", "브랜드", "마케팅",
    "전략", "콘텐츠", "소비자", "Z세대", "MZ",
    "AI", "생성형", "노코드", "바이브 코딩", "사이드 프로젝트",
    "1인", "솔로", "창업", "스타트업", "런칭", "출시", "MVP",
    "구독", "SaaS", "D2C", "이커머스", "리테일",
    "외국인", "방한", "관광객", "인바운드", "한류", "K-",
    "서울", "여행", "Seoul", "Korea", "Korean",
    "tourism", "tourist", "visit", "travel", "trend",
]

KEYWORDS_BLOCK = [
    "프로야구", "축구", "농구", "배구", "올림픽",
    "연예", "드라마 개봉", "영화 개봉", "아이돌 컴백",
    "사망", "별세", "부고",
]

MAX_ITEMS = 20
