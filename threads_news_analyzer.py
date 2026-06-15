"""
Threads 콘텐츠 소재용 뉴스 분석기
- 각 기사에 대해 Claude가 어그로 점수 평가
- 본인 콘텐츠 공식에 어떻게 활용할지 자동 분석
- 어그로 점수 낮은 기사는 자동 제외
"""

import json
import time
from anthropic import Anthropic


PROMPT_TEMPLATE = """You are evaluating news articles for a Korea travel Threads marketing strategy.

[CONTEXT]
We post on Threads daily targeting English-speaking foreign travelers to Korea.
Our content formula: provocative hook → tease in body → reveal in comments → Pglemaps pitch.
We want articles that work as material for THESE kinds of provocative posts:
- Price shock (Korea X is 1/5 of US price)
- Tourist traps / scams to avoid
- Insider info Koreans don't tell foreigners
- Things foreigners regret doing in Korea
- Limited-time deals/promotions for foreigners

[TODAY'S TOPIC]
Topic: {topic}
This article is about: {topic} category in Korea travel.

[ARTICLE]
Title: {title}
Summary: {summary}
Source: {source}
Language: {lang}

[YOUR TASK]
Evaluate this article on a scale of 1-5 for Threads content potential:

5 = Perfect material. Contains specific shocking info (price, scam, hidden tip, regret story, limited offer)
4 = Strong material. Has some provocative angle for foreigners
3 = Decent material. General info but could be reframed
2 = Weak. Generic promotional content
1 = Useless. Pure PR/advertorial, no provocative angle

Return ONLY valid JSON (no markdown):
{{
  "agro_score": 1-5,
  "agro_type": "Price Shock | Tourist Trap | Insider Info | Regret Story | Limited Offer | Other",
  "key_hook": "one-line provocative hook this article could be turned into",
  "content_idea": "one-line Threads post idea using our formula",
  "use_recommendation": "Use Today | Use This Week | Save for Later | Skip"
}}

IMPORTANT:
- Be brutally honest. Most articles will score 1-2.
- Score 4-5 only when article has SPECIFIC numbers, names, or shocking info
- Score 1 for typical PR/government promotion language
"""


def get_client(api_key):
    return Anthropic(api_key=api_key)


def analyze_article(client, topic, article):
    """단일 기사의 어그로 점수 평가"""
    prompt = PROMPT_TEMPLATE.format(
        topic=topic,
        title=article.get("title", ""),
        summary=article.get("summary", "")[:400],
        source=article.get("source", ""),
        lang=article.get("lang", "en"),
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
        print(f"[WARN] 분석 실패: {article.get('title','')[:30]} - {e}")
        return None


def analyze_articles(client, topic, articles, min_score=3):
    """여러 기사 분석 + 점수 낮은 기사 필터링
    
    Args:
        articles: 수집된 기사 리스트
        min_score: 이 점수 이상만 통과 (기본 3)
    """
    print(f"🤖 {len(articles)}건 분석 중...")
    
    analyzed = []
    for i, article in enumerate(articles, 1):
        if i % 5 == 0:
            print(f"  진행: {i}/{len(articles)}")
        
        analysis = analyze_article(client, topic, article)
        if analysis:
            article["analysis"] = analysis
            score = analysis.get("agro_score", 0)
            if score >= min_score:
                analyzed.append(article)
        
        time.sleep(0.3)  # Rate limit 방지
    
    # 점수 높은 순으로 정렬
    analyzed.sort(
        key=lambda x: x.get("analysis", {}).get("agro_score", 0),
        reverse=True,
    )
    
    print(f"✅ {len(analyzed)}건이 점수 {min_score}+ 통과")
    return analyzed


def enrich_with_analysis(api_key, topic, articles, min_score=3):
    """수집된 기사를 Claude로 분석 + 필터링"""
    if not api_key:
        print("[WARN] ANTHROPIC_API_KEY 없음 - 분석 건너뜀")
        return articles
    
    client = get_client(api_key)
    return analyze_articles(client, topic, articles, min_score)
