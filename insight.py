"""
Claude로 카테고리별 인사이트 분석
- 7개 카테고리 각자 다른 평가 기준
- 한국어 번역 필수
- 카테고리당 상위 3건 선별
"""

import json
import time
from anthropic import Anthropic


# 카테고리별 Claude 프롬프트
PROMPTS = {
    "betalist": """You are evaluating a new startup from BetaList for a Korean entrepreneur.

The entrepreneur runs Pglemaps (pglemaps.com/en), a Korea trip route planner for foreign travelers.
Business model: affiliate commissions from Korean experiences (Hanbok, K-beauty, food tours).

[STARTUP]
Title: {title}
Source: {source}
Summary: {summary}

[YOUR TASK]
Return ONLY valid JSON:
{{
  "title_kr": "한국어로 자연스럽게 번역된 제목",
  "summary_kr": "한국어로 2-3줄 요약 (무엇을 하는 서비스인지)",
  "score": 1-5,
  "insight_kr": "본인 사업에 적용 가능한 포인트 1문장 (관련 낮으면 '본인 사업과 관련성 낮음')"
}}

RULES:
- score 5 = Pglemaps 직접 경쟁/협력 가능
- score 4 = 본인 사업에 응용 가능
- score 3 = 트렌드 참고용
- score 1-2 = 관련성 낮음
""",

    "monetize": """You are evaluating a side project for a Korean entrepreneur exploring "vibe coding" monetization.

[PROJECT]
Title: {title}
Source: {source}
Summary: {summary}

[YOUR TASK]
Return ONLY valid JSON:
{{
  "title_kr": "한국어로 자연스럽게 번역된 제목",
  "summary_kr": "한국어로 2-3줄 요약 (무엇을 만들었고 어떻게 돈 버는지)",
  "score": 1-5,
  "insight_kr": "본인이 따라할 만한 핵심 액션 1문장 한국어 (가치 낮으면 '단순 출시 소식')"
}}

RULES:
- score 5 = 명확한 수익 모델 + 따라할만함 (MRR/매출 공개)
- score 4 = 좋은 아이디어 + 실행 가능
- score 3 = 참고용
- score 1-2 = 단순 출시 소식, 가치 낮음
""",

    "inbound_tourism": """You are evaluating Korea inbound tourism news for a Korean entrepreneur in the travel/affiliate business.

[ARTICLE]
Title: {title}
Source: {source}
Summary: {summary}

[YOUR TASK]
Return ONLY valid JSON:
{{
  "title_kr": "한국어로 자연스럽게 번역된 제목 (이미 한국어면 그대로)",
  "summary_kr": "한국어로 2-3줄 핵심 요약",
  "score": 1-5,
  "insight_kr": "방한 외국인 사업에 활용할 수 있는 포인트 1문장 (관련 낮으면 '일반 보도')"
}}

RULES:
- score 5 = 명확한 통계/정책/시장 변화 (수치 포함)
- score 4 = 의미있는 트렌드 정보
- score 3 = 일반 산업 뉴스
- score 1-2 = 단순 홍보/광고
""",

    "gov_policy": """You are evaluating Korean government policy news for an entrepreneur running an inbound tourism business.

[ARTICLE]
Title: {title}
Source: {source}
Summary: {summary}

[YOUR TASK]
Return ONLY valid JSON:
{{
  "title_kr": "한국어로 번역된 제목 (이미 한국어면 그대로)",
  "summary_kr": "한국어로 2-3줄 핵심 요약 (어떤 지원/정책인지)",
  "score": 1-5,
  "insight_kr": "본인이 신청 가능하거나 활용 가능한 포인트 1문장 (관련 낮으면 '직접 적용 어려움')"
}}

RULES:
- score 5 = 본인 직접 신청 가능한 지원금/제도
- score 4 = 관광/외국인 사업 관련 정책
- score 3 = 일반 스타트업 지원
- score 1-2 = 무관한 정부 발표
""",

    "tourism_industry": """You are evaluating Korean tourism industry news for an entrepreneur competing with Klook/Trip.com type platforms.

[ARTICLE]
Title: {title}
Source: {source}
Summary: {summary}

[YOUR TASK]
Return ONLY valid JSON:
{{
  "title_kr": "한국어로 번역된 제목 (이미 한국어면 그대로)",
  "summary_kr": "한국어로 2-3줄 요약",
  "score": 1-5,
  "insight_kr": "본인 사업에 활용/대응할 포인트 1문장 (관련 낮으면 '단순 산업 뉴스')"
}}

RULES:
- score 5 = 경쟁사 동향/신규 모델/시장 변화
- score 4 = 관광 플랫폼 트렌드
- score 3 = 일반 관광 뉴스
- score 1-2 = 단순 홍보
""",

    "affiliate": """You are evaluating affiliate marketing case studies for an entrepreneur using affiliate revenue model.

[ARTICLE]
Title: {title}
Source: {source}
Summary: {summary}

[YOUR TASK]
Return ONLY valid JSON:
{{
  "title_kr": "한국어로 번역된 제목 (이미 한국어면 그대로)",
  "summary_kr": "한국어로 2-3줄 요약",
  "score": 1-5,
  "insight_kr": "본인 어필리에이트 전략에 적용할 포인트 1문장 (관련 낮으면 '실용 가치 낮음')"
}}

RULES:
- score 5 = 구체적 성공 사례 + 따라할만한 전략
- score 4 = 어필리에이트 트렌드/팁
- score 3 = 마케팅 일반론
- score 1-2 = 추상적/무관
""",

    "foreigner_business": """You are evaluating news about businesses targeting foreigners in Korea (K-beauty, K-food, K-fashion for tourists).

[ARTICLE]
Title: {title}
Source: {source}
Summary: {summary}

[YOUR TASK]
Return ONLY valid JSON:
{{
  "title_kr": "한국어로 번역된 제목 (이미 한국어면 그대로)",
  "summary_kr": "한국어로 2-3줄 요약",
  "score": 1-5,
  "insight_kr": "본인 사업에 활용할 포인트 1문장 (관련 낮으면 '일반 보도')"
}}

RULES:
- score 5 = 외국인 대상 마케팅 성공 사례
- score 4 = 외국인 시장 트렌드
- score 3 = 일반 K-콘텐츠 뉴스
- score 1-2 = 무관
""",
}


def get_client(api_key):
    return Anthropic(api_key=api_key)


def analyze_item(client, item, category):
    """단일 항목 분석"""
    prompt_template = PROMPTS.get(category)
    if not prompt_template:
        return None
    
    prompt = prompt_template.format(
        title=item.get("title", ""),
        source=item.get("source", ""),
        summary=item.get("summary", "")[:500],
    )
    
    try:
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )
        text = msg.content[0].text.strip()
        
        # JSON 추출
        if "```" in text:
            parts = text.split("```")
            if len(parts) >= 2:
                text = parts[1]
                if text.startswith("json"):
                    text = text[4:]
                text = text.strip()
        
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            text = text[start:end+1]
        
        return json.loads(text)
    
    except Exception as e:
        print(f"[WARN] 분석 실패: {item.get('title','')[:30]} - {e}")
        return None


def enrich_items(api_key, grouped_items):
    """카테고리별 분석 + 상위 3건 선별"""
    if not api_key:
        print("[WARN] API 키 없음")
        return grouped_items
    
    client = get_client(api_key)
    result = {}
    
    for category, items in grouped_items.items():
        if not items:
            result[category] = []
            continue
        
        print(f"🤖 {category} {len(items)}건 분석 중...")
        
        analyzed = []
        for i, item in enumerate(items, 1):
            if i % 5 == 0:
                print(f"  진행: {i}/{len(items)}")
            
            analysis = analyze_item(client, item, category)
            if analysis:
                item["analysis"] = analysis
                analyzed.append(item)
            
            time.sleep(0.2)
        
        # 점수 기준 정렬
        analyzed.sort(
            key=lambda x: x.get("analysis", {}).get("score", 0),
            reverse=True,
        )
        
        # 상위 3건만
        result[category] = analyzed[:3]
        print(f"✅ {category}: 상위 {len(result[category])}건 선별")
    
    return result
