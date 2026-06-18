"""
Claude로 본인 사업 맞춤 인사이트 생성
- 한국어 번역
- 본인 사업 적용 가능성 평가
- 카테고리당 5건만 선별
"""

import json
import time
from anthropic import Anthropic


BETALIST_PROMPT = """You are evaluating new startups from BetaList for a Korean entrepreneur.

The entrepreneur runs Pglemaps (pglemaps.com/en), a Korea trip route planner for foreign travelers.
Business model: affiliate commissions from Korean experiences (Hanbok, K-beauty, food tours, etc.)

[STARTUP]
Title: {title}
Source: {source}
Summary: {summary}

[YOUR TASK]
Provide concise analysis in Korean:

Return ONLY valid JSON:
{{
  "title_kr": "한국어로 번역된 제목 (자연스럽게)",
  "summary_kr": "한국어로 2-3줄 요약",
  "relevance_score": 1-5,
  "insight_kr": "본인 사업에 적용 가능한 포인트 1문장 한국어 (없으면 '본인 사업과 직접 관련성 낮음')"
}}

RULES:
- relevance_score: 5=직접 적용 가능, 3=참고용, 1=관련성 낮음
- summary_kr: 무엇을 하는 서비스인지 핵심만 (홍보 톤 X)
- insight_kr: 진짜 본인 사업에 도움될지 솔직하게
"""


MONETIZE_PROMPT = """You are evaluating side projects/indie hacker stories for a Korean entrepreneur.

The entrepreneur is exploring monetization ideas through "vibe coding" - small AI-powered projects, 
side projects, automation tools, micro-SaaS, etc.

[PROJECT]
Title: {title}
Source: {source}
Summary: {summary}

[YOUR TASK]
Evaluate if this is a real monetization opportunity worth following:

Return ONLY valid JSON:
{{
  "title_kr": "한국어로 번역된 제목 (자연스럽게)",
  "summary_kr": "한국어로 2-3줄 요약",
  "monetization_score": 1-5,
  "actionable_kr": "본인이 따라할 만한 핵심 1문장 한국어 (없으면 '단순 출시 소식, 따라할 모델 X')"
}}

RULES:
- monetization_score: 5=명확한 수익 모델 + 따라할 만함, 3=참고만, 1=가치 낮음
- summary_kr: 무엇을 만들었고 어떻게 돈 버는지
- actionable_kr: 본인이 실제로 시도 가능한 액션 (없으면 솔직히)
- Hacker News Show HN의 단순 출시 소식은 1-2점
- 실제 수익 보고 (MRR, revenue 공개)는 4-5점
"""


def get_client(api_key):
    return Anthropic(api_key=api_key)


def analyze_item(client, item, category):
    """단일 항목 분석"""
    if category == "betalist":
        prompt_template = BETALIST_PROMPT
    elif category == "monetize":
        prompt_template = MONETIZE_PROMPT
    else:
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
    """카테고리별 항목 분석 + 점수 높은 5건 선별
    
    Args:
        grouped_items: {"betalist": [...], "monetize": [...]}
    """
    if not api_key:
        print("[WARN] API 키 없음")
        return grouped_items
    
    client = get_client(api_key)
    
    result = {}
    
    for category, items in grouped_items.items():
        print(f"🤖 {category} 카테고리 {len(items)}건 분석 중...")
        
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
        score_key = "relevance_score" if category == "betalist" else "monetization_score"
        analyzed.sort(
            key=lambda x: x.get("analysis", {}).get(score_key, 0),
            reverse=True,
        )
        
        # 상위 5건만 선별
        result[category] = analyzed[:5]
        print(f"✅ {category}: 상위 5건 선별 완료")
    
    return result
