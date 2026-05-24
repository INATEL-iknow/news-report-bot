import json
import time
from anthropic import Anthropic

def get_client(api_key):
    return Anthropic(api_key=api_key)

PROMPT_TEMPLATES = {
    "창업·아이디어": """다음 뉴스 기사를 보고, 바이브 코딩(노코드/AI 활용 빠른 개발)으로 1~2주 안에 만들 수 있는 구체적인 아이디어를 1개 제안해주세요.

기사 제목: {title}
기사 요약: {summary}

다음 JSON 형식으로만 답하세요 (다른 텍스트 X):
{{
  "innovation_level": "Core|Adjacent|Transformative 중 하나",
  "idea": "한 문장 아이디어 (예: 'X를 자동화하는 Y 도구')",
  "monetization": "수익화 방법 (1줄)",
  "build_difficulty": "쉬움|보통|어려움",
  "key_tech": "필요한 핵심 기술/도구 (예: 'Claude API + Streamlit')"
}}

판단 기준:
- Core: 검증된 시장, 1주 안에 MVP 가능, 명확한 페인포인트
- Adjacent: 1~3개월 빌드, 기존 모델 응용
- Transformative: 6개월+, 신규 카테고리 창출""",

    "방한외국인": """다음 뉴스를 보고, 피글맵스(방한 외국인 대상 서비스)와 어떻게 연결해 수익화/상품화할 수 있을지 제안해주세요.

[피글맵스 정보]
{context}

[기사]
제목: {title}
요약: {summary}

다음 JSON 형식으로만 답하세요:
{{
  "innovation_level": "Core|Adjacent|Transformative 중 하나",
  "connection": "이 뉴스가 피글맵스와 어떻게 연결되는지 (1줄)",
  "product_idea": "구체적인 상품/기능 제안 (1~2줄)",
  "revenue_model": "수익 모델 (어필리에이트/구독/광고/B2B 등)",
  "priority": "높음|중간|낮음"
}}

판단 기준:
- Core: 현재 어필리에이트 모델에 바로 붙일 수 있음
- Adjacent: 동선 데이터 활용한 신규 기능
- Transformative: B2B/플랫폼 확장 등 큰 베팅""",

    "사회·경제": """다음 뉴스의 핵심을 요약하고, 창업·관광 사업자 관점에서 활용 포인트를 알려주세요.

기사 제목: {title}
기사 요약: {summary}

다음 JSON 형식으로만 답하세요:
{{
  "summary": "핵심 내용 1~2줄 요약",
  "actionable": "창업자/관광 사업자가 활용할 만한 포인트 (1줄)",
  "category_tag": "지원금|정책|시장동향|기타 중 하나"
}}"""
}

def analyze_item(client, category, item, context=""):
    """단일 기사를 Claude로 분석"""
    template = PROMPT_TEMPLATES.get(category)
    if not template:
        return None
    
    prompt = template.format(
        title=item.get("title", ""),
        summary=item.get("summary", "")[:300],
        context=context,
    )
    
    try:
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",  # 빠르고 저렴
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}],
        )
        text = msg.content[0].text.strip()
        # JSON 추출 (앞뒤 ``` 등 제거)
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
    """카테고리별로 아이템에 AI 인사이트 추가"""
    client = get_client(api_key)
    
    for cat, items in items_by_cat.items():
        print(f"  AI 분석 중: {cat} ({len(items)}건)")
        for item in items:
            insight = analyze_item(client, cat, item, context)
            item["insight"] = insight
            time.sleep(0.3)  # API 부하 방지
    
    return items_by_cat
