"""
뉴스 필터링기 - Claude로 어그로 점수 평가
- 수집된 뉴스 중 진짜 외국인이 흥미로워할 것만 선별
- 점수 4~5점만 통과
- 평범한 보도자료/홍보 기사 제외
"""

import json
import time
from anthropic import Anthropic


PROMPT_TEMPLATE = """You are filtering Korean news articles for a Threads marketing strategy.

Target audience: English-speaking foreign travelers visiting Korea.
We want articles that contain SPECIFIC, PROVOCATIVE information they'd find genuinely intriguing.

[ARTICLE]
Category: {category}
Title: {title}
Summary: {summary}
Source: {source}
Language: {lang}

[CATEGORY DEFINITION]
{category_def}

[YOUR TASK]
Score this article 1-5 for Threads content potential:

5 = Excellent. Contains SPECIFIC shocking info (real prices, real scam details, real insider tips, real benefits)
4 = Strong. Has clear provocative angle with some specifics
3 = Decent. Could be reframed but lacks specifics
2 = Weak. Generic promotional content
1 = Useless. Pure PR or unrelated

[STRICT SCORING RULES]
- Score 1-2 for typical government/company PR with no shocking specifics
- Score 1-2 for general K-beauty/tourism trend articles
- Score 4-5 ONLY if article has REAL numbers, names, or surprising facts
- Be brutally honest. Most articles deserve 1-3.

[OUTPUT]
Return ONLY valid JSON:
{{
  "score": 1-5,
  "reason": "1 sentence in Korean explaining the score",
  "key_fact": "If score 4-5, the most provocative specific fact from this article (1 sentence). Otherwise empty."
}}
"""


CATEGORY_DEFINITIONS = {
    "price_shock": "Articles about specific Korean prices that would shock foreigners (botox, surgery, dental, glasses) compared to other countries.",
    "scams": "Articles about specific scams, rip-offs, hidden fees targeting foreign tourists in Korea.",
    "insider": "Articles revealing places/info known to Koreans but unknown to foreign tourists (real local spots, hidden tips).",
    "regrets": "Articles about specific mistakes foreigners make in Korea or things they wish they knew.",
    "deals": "Articles about specific foreigner-only discounts, free services, government promotions for tourists.",
}


def filter_news_with_claude(api_key, news_items, min_score=4):
    """Claude로 뉴스 필터링
    
    Args:
        news_items: collector에서 수집한 뉴스 리스트
        min_score: 이 점수 이상만 통과 (기본 4)
    """
    if not api_key:
        print("[WARN] API 키 없음")
        return []
    
    if not news_items:
        return []
    
    client = Anthropic(api_key=api_key)
    
    print(f"🔍 Claude로 {len(news_items)}건 필터링 중...")
    
    filtered = []
    for i, item in enumerate(news_items, 1):
        if i % 10 == 0:
            print(f"  진행: {i}/{len(news_items)}")
        
        category = item.get("category", "")
        prompt = PROMPT_TEMPLATE.format(
            category=category,
            title=item.get("title", ""),
            summary=item.get("summary", "")[:400],
            source=item.get("source", ""),
            lang=item.get("lang", "en"),
            category_def=CATEGORY_DEFINITIONS.get(category, ""),
        )
        
        try:
            msg = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=400,
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
            
            evaluation = json.loads(text)
            score = evaluation.get("score", 0)
            
            item["evaluation"] = evaluation
            
            # 점수 통과만 저장
            if score >= min_score:
                filtered.append(item)
        
        except Exception as e:
            print(f"[WARN] 평가 실패: {e}")
        
        time.sleep(0.2)
    
    # 점수 높은 순 정렬
    filtered.sort(
        key=lambda x: x.get("evaluation", {}).get("score", 0),
        reverse=True,
    )
    
    print(f"✅ 점수 {min_score}+ 통과: {len(filtered)}건")
    return filtered


def filter_by_category(filtered_items):
    """필터링된 뉴스를 카테고리별로 그룹화 + 각 카테고리 최대 2건"""
    by_category = {
        "price_shock": [],
        "scams": [],
        "insider": [],
        "regrets": [],
        "deals": [],
    }
    
    for item in filtered_items:
        cat = item.get("category", "")
        if cat in by_category and len(by_category[cat]) < 2:
            by_category[cat].append(item)
    
    return by_category
