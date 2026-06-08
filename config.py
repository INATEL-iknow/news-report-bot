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
    "바이브코딩": [
        gnews("AI 도구 출시"),
        gnews("노코드 서비스"),
        gnews("바이브 코딩"),
        gnews("1인 개발자 수익"),
        gnews("AI 사이드 프로젝트"),
        gnews("AI 자동화 도구"),
        gnews("indie hacker", lang="en"),
        gnews("solo founder AI tool", lang="en"),
    ],
    "외국인마케팅성공사례": [
        gnews("외국인 마케팅 성공"),
        gnews("인바운드 마케팅 사례"),
        gnews("관광 마케팅 캠페인"),
        gnews("K-마케팅 해외"),
        gnews("외국인 고객 유치 성공"),
        gnews("글로벌 브랜딩 한국"),
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

# 카테고리별 개수 (총 20개)
CATEGORY_QUOTA = {
    "바이브코딩": 5,
    "외국인마케팅성공사례": 5,
    "방한외국인": 5,
    "정부지원금": 5,
}

# 피글맵스 컨텍스트
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

# 가산점 키워드 (제목/요약에 있으면 점수 ↑)
KEYWORDS_BOOST = [
    # 바이브 코딩
    "AI", "생성형", "노코드", "바이브 코딩", "1인 개발자", "솔로",
    "사이드 프로젝트", "indie", "MVP", "출시", "런칭",
    # 마케팅 성공사례
    "성공", "캠페인", "사례", "마케팅", "브랜딩", "전환율",
    "고객 유치", "바이럴", "성과",
    # 방한 외국인
    "외국인", "방한", "관광객", "인바운드", "한류", "K-",
    "한복", "K-뷰티", "체험", "서울 여행", "Korea", "Seoul",
    # 정부지원금
    "지원금", "지원사업", "모집", "공고", "선정", "보조금",
    "관광공사", "중기부", "문체부", "창업지원",
]

# 부정 키워드 (제외) - 강화됨
KEYWORDS_BLOCK = [
    # 스포츠
    "프로야구", "축구", "농구", "배구", "올림픽", "월드컵",
    "KBO", "K리그", "MLB", "NBA",
    # 연예
    "연예", "드라마 개봉", "영화 개봉", "아이돌 컴백", "OST",
    "결혼", "이혼", "열애",
    # 부고/사고
    "사망", "별세", "부고", "유언", "추모", "장례",
    # 정치 (창업·관광과 무관한)
    "여당", "야당", "당대표", "대선", "총선", "탄핵",
    # 광고성·저품질
    "이벤트 안내", "할인 행사", "프로모션 진행",
    "기자회견", "보도자료",
    # 부동산 (관련 없음)
    "아파트 분양", "오피스텔", "재개발",
]

# 광고성 기사 차단 키워드 (제목에 있으면 100% 제외)
SPAM_PHRASES = [
    "[광고]", "[홍보]", "PR", "협찬",
    "스폰서드", "AD)",
]

MAX_ITEMS = 20

# 최소 기사 본문 길이 (이보다 짧으면 제외)
MIN_SUMMARY_LENGTH = 50

# 중복 판단 기준 (제목 유사도, 낮을수록 더 엄격하게 제거)
DEDUPE_THRESHOLD = 0.65
