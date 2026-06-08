import json
import time
from anthropic import Anthropic

def get_client(api_key):
    return Anthropic(api_key=api_key)

PROMPT_TEMPLATES = {
    "바이브코딩": """다음 뉴스를 보고, 1인 개발자가 바이브 코딩(노코드/AI 활용 빠른 개발)으로 만들 수 있는 구체적인 아이디어 1개를 제안해주세요.

기사 제목: {title}
기사 요약: {summary}

다음 JSON 형식으로만 답하세요:
{{
  "innovation_level": "Core|Adjacent|Transformative 중 하나",
  "idea": "한 문장 아이디어",
  "target_user": "타겟 고객 (구체적으로)",
  "monetization": "수익화 방법 - 다음 중에서만 선택: '어필리에이트 커미션', '광고 수익', '데이터/리포트 판매(B2B)', '거래 수수료(마켓플레이스)', '컨설팅/강의/교육', '일회성 결제(One-time purchase)' 중 하나와 구체적 설명",
  "revenue_estimate": "현실적인 월 수익 추정 (예: 50~200만원)",
  "build_difficulty": "쉬움|보통|어려움",
  "key_tech": "필요한 핵심 기술/도구"
}}

⚠️ 중요:
- '월 구독료' 모델은 절대 제안하지 말 것
- 1인 개발자가 6개월 이내에 실제로 수익을 낼 수 있는 모델만
- 추상적이면 안 됨, 구체적인 수익 구조 명시""",

    "외국인마케팅성공사례": """다음 뉴스는 외국인 대상 마케팅 사례입니다. 핵심 성공 요인을 분석하고, 피글맵스(방한 외국인 대상 서비스)에 어떻게 적용할 수 있는지 제안해주세요.

[피글맵스 정보]
{context}

[기사]
제목: {title}
요약: {summary}

다음 JSON 형식으로만 답하세요:
{{
  "success_factor": "이 캠페인/사례의 핵심 성공 요인 (1줄)",
  "key_metric": "주목할 만한 수치/성과 (있다면)",
  "piglemaps_application": "피글맵스에 어떻게 적용할 수 있는지 (구체적으로)",
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
  "revenue_model": "수익 모델 (어필리에이트/광고/B2B 등)",
  "priority": "높음|중간|낮음"
}}""",

    "정부지원금": """다음은 정부 지원사업/지원금 관련 뉴스입니다. 창업자/관광사업자가 활용할 수 있는 정보를 정리해주세요.

기사 제목: {title}
기사 요약: {summary}

다음 JSON 형식으로만 답하세요:
{{
  "program_name": "지원사업명 (기사에서 추출, 없으면 '정보 부족')",
  "target": "지원 대상 (예: 관광 스타트업, 청년 창업가 등)",
  "support_amount": "지원 금액/규모 (기사에 있으면, 없으면 '확인 필요')",
  "deadline": "신청 마감일 또는 일정 (있으면)",
  "fit_for_piglemaps": "피글맵스 신청 적합도 - 매우높음|높음|보통|낮음",
  "action": "지금 해야 할 행동 (1줄, 예: '내일 공고 확인 후 신청서 작성')"
}}"""
}

def analyze_item(client, category, item, context=""):
    template = PROMPT_TEMPLATES.get(category)
    if not template:
        return None
    
    prompt = template.format(
        title=item.get("title", ""),
        summary=item.get("summary", "")[:400],
        context=context,
    )
    
    try:
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=500,
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
