"""
검증된 뉴스 → Threads 어그로 아이디어 생성기
- 진짜 뉴스 기사 기반으로 어그로 아이디어 작성
- 영문 + 한글 동시 출력
- 본인 콘텐츠 공식 적용 (어그로 + Open Loop)
"""

import json
import time
from anthropic import Anthropic


PROMPT_TEMPLATE = """You are a content strategist for a Threads account targeting foreign travelers to Korea.

You are given a REAL news article. Create a provocative Threads post idea based ONLY on facts in this article.

[ARTICLE]
Title: {title}
Summary: {summary}
Key Fact: {key_fact}
Source: {source}

[CONTENT FORMULA]
Our Threads posts follow this structure:
- Hook: address foreign travelers directly
- Tease provocative info from the article
- End with Open Loop (incomplete ending)
- The actual "answer" is in comments later

[YOUR TASK]
Generate ONE provocative idea based on this article.
The idea should be a single English sentence (10-20 words) that:
1. Uses SPECIFIC facts from the article (numbers, names, places)
2. Creates curiosity/shock for foreign travelers
3. Avoids generic statements

Then translate to Korean.

[STYLE EXAMPLES]
- "Korea is giving 8,000 foreign travelers a hidden bus discount - but only this month."
- "Why Incheon airport taxis charge foreigners 4x more than locals (and how to avoid it)."
- "The Korean government just made eSIM free for foreign tourists - no one's talking about it."

[OUTPUT]
Return ONLY valid JSON:
{{
  "idea_en": "1 provocative English sentence based on REAL facts from this article",
  "idea_kr": "한국어 번역 (자연스럽게)",
  "facts_used": "specific facts from the article you used (1 sentence)"
}}

IMPORTANT:
- ONLY use facts that are explicitly in the article
- DO NOT make up numbers or details
- If article has no specific shocking facts, write a more general but accurate hook
"""


def generate_idea_from_news(client, news_item):
    """단일 뉴스로부터 어그로 아이디어 생성"""
    evaluation = news_item.get("evaluation", {})
    key_fact = evaluation.get("key_fact", "")
    
    prompt = PROMPT_TEMPLATE.format(
        title=news_item.get("title", ""),
        summary=news_item.get("summary", "")[:500],
        key_fact=key_fact,
        source=news_item.get("source", ""),
    )
    
    try:
        msg = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=600,
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
        print(f"[WARN] 아이디어 생성 실패: {e}")
        return None


def generate_ideas_from_news_pool(api_key, news_by_category):
    """카테고리별 뉴스에서 아이디어 생성
    
    Args:
        news_by_category: {"price_shock": [news1, news2], "scams": [...], ...}
    """
    if not api_key:
        return news_by_category
    
    client = Anthropic(api_key=api_key)
    
    print(f"💡 검증된 뉴스로 어그로 아이디어 생성 중...")
    
    total_ideas = 0
    for category, news_list in news_by_category.items():
        print(f"  {category}: {len(news_list)}건")
        for news in news_list:
            idea = generate_idea_from_news(client, news)
            if idea:
                news["idea"] = idea
                total_ideas += 1
            time.sleep(0.3)
    
    print(f"✅ {total_ideas}개 아이디어 생성 완료")
    return news_by_category
