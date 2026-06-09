import json
import time
from anthropic import Anthropic

def get_client(api_key):
    return Anthropic(api_key=api_key)

PROMPT_TEMPLATES = {
    "오늘의출시도구": """다음은 오늘 새로 출시되거나 GitHub에서 트렌딩 중인 도구/서비스입니다. 이걸 보고 본인이 1~2주 안에 만들 수 있는 "한국 시장 적용 버전"을 제안해주세요.

[피글맵스 정보]
{context}

[도구 정보]
이름: {title}
설명: {summary}
링크: {link}

다음 JSON 형식으로만 답하세요:
{{
  "what_it_does": "이 도구가 정확히 뭘 하는지 (1줄)",
  "korean_market_idea": "한국 시장 또는 피글맵스에 맞춰 응용/변형할 아이디어 (구체적으로)",
  "target_user": "구체적 타겟",
  "monetization": "수익화 방법 - '어필리에이트', '광고', '데이터 판매 B2B', '거래 수수료', '컨설팅/강의', '일회성 결제' 중 하나 + 설명",
  "revenue_estimate": "현실적 월 수익 추정 (예: 30~150만원)",
  "build_time": "예상 개발 시간",
  "key_tech": "핵심 기술 스택",
  "first_step": "당장 내일 30분 안에 할 첫 액션"
}}

⚠️ 월 구독료 모델 금지. 매우 구체적으로.""",

    "사이드프로젝트": """다음은 개인 개발자가 만든 사이드 프로젝트나 1인 비즈니스 사례입니다. 여기서 영감을 얻어 본인이 만들 수 있는 아이디어를 1개 제안해주세요.

[피글맵스 정보]
{context}

[사이드 프로젝트]
제목: {title}
설명: {summary}

다음 JSON 형식으로만 답하세요:
{{
  "what_they_built": "그들이 만든 것 (1줄)",
  "their_insight": "이 프로젝트에서 배울 점 / 영감 포인트",
  "my_version_idea": "본인 도메인(관광/외국인/피글맵스)에 맞춘 버전 아이디어",
  "target_user": "구체적 타겟",
  "monetization": "수익화 방법 (구독료 제외)",
  "revenue_estimate": "현실적 월 수익 추정",
  "execution_difficulty": "쉬움|보통|어려움",
  "first_step": "내일 30분 안에 할 첫 액션"
}}""",

    "외국인마케팅성공사례": """다음 뉴스는 외국인 대상 마케팅 사례입니다. 핵심 성공 요인을 분석하고, 피글맵스에 어떻게 적용할 수 있는지 제안해주세요.

[피글맵스 정보]
{context}

[기사]
제목: {title}
요약: {summary}

다음 JSON 형식으로만 답하세요:
{{
  "success_factor": "핵심 성공 요인 (1줄)",
  "key_metric": "주목할 만한 수치/성과 (있다면)",
  "piglemaps_application": "피글맵스에 어떻게 적용할 수 있는지",
  "execution_difficulty": "즉시 적용 가능|1-3개월|6개월+",
  "priority": "높음|중간|낮음"
}}""",

    "방한외국인": """다음 뉴스를 보고, 피글맵스와 어떻게 연결해 수익화/상품화할 수 있을지 제안해주세요.

[피글맵스 정보]
{context}

[기사]
제목: {title}
요약: {summary}

다음 JSON 형식으로만 답하세요:
{{
  "innovation_level": "Core|Adjacent|Transformative 중 하나",
  "connection": "이 뉴스가 피글맵스와 어떻게 연결되는지",
  "product_idea": "구체적인 상품/기능 제안",
  "revenue_model": "수익 모델",
  "priority": "높음|중간|낮음"
}}""",

    "정부지원금": """다음은 정부 지원사업/지원금 관련 뉴스입니다. 창업자/관광사업자가 활용할 수 있는 정보를 정리해주세요.

기사 제목: {title}
기사 요약: {summary}

다음 JSON 형식으로만 답하세요:
{{
  "program_name": "지원사업명 (기사에서 추출)",
  "target": "지원 대상",
  "support_amount": "지원 금액/규모",
  "deadline": "신청 마감일 또는 일정",
  "fit_for_piglemaps": "피글맵스 신청 적합도 - 매우높음|높음|보통|낮음",
  "action": "지금 해야 할 행동 (1줄)"
}}""",

    "Reddit인사이트": """다음은 외국인이 Reddit에 작성한 한국 관련 글입니다. 영어를 한국어로 번역하고, 피글맵스 입장에서 어떤 인사이트를 얻을 수 있는지 분석해주세요.

[피글맵스 정보]
{context}

[Reddit 글]
제목 (영어): {title}
본문 (영어): {summary}
서브레딧: {source}

다음 JSON 형식으로만 답하세요:
{{
  "title_kr": "제목 한국어 번역 (자연스럽게)",
  "summary_kr": "본문 핵심 한국어 요약 (2~3문장, 본문 없으면 '본문 없음')",
  "user_intent": "이 사람이 진짜 원하는 것 / 페인포인트 (1줄)",
  "piglemaps_opportunity": "피글맵스가 이 사람에게 어떤 가치를 줄 수 있는지 (구체적으로)",
  "content_idea": "이 글을 보고 만들 수 있는 콘텐츠/마케팅 아이디어 (예: '○○ 관련 가이드 영상 제작')",
  "priority": "높음|중간|낮음 (이 인사이트의 활용 우선순위)"
}}

⚠️ 매우 구체적으로. 추상적 답변 금지."""
}

def analyze_item(client, category, item, context=""):
    template = PROMPT_TEMPLATES.get(category)
    if not template:
        return None
    
    prompt = template.format(
        title=item.get("title", ""),
        summary=item.get("summary", "")[:500],
        link=item.get("link", ""),
        source=item.get("source", ""),
        context=context,
    )
    
    try:
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=700,
            messages=[{"role": "user", "content": prompt}],
        )
        text = msg.content[0].text.strip()
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()
        return json.loads(text)
    except Exception as e:
        print(f"[WARN] AI 분석 실패: {item.get('title','')[:30]} - {e}")
        return None

def enrich_items(items_by_cat, api_key, context):
    client = get_client(api_key)
    
    for cat, items in items_by_cat.items():
        print(f"  AI 분석 중: {cat} ({len(items)}건)")
        for item in items:
            insight = analyze_item(client, cat, item, context)
            item["insight"] = insight
            time.sleep(0.3)
    
    return items_by_cat
