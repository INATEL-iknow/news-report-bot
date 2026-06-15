"""
Threads 콘텐츠 아이디어 생성기
- 매일 Claude가 5개 카테고리 × 각 2개 = 10개 새 주제 생성
- 각 아이디어마다 검색용 키워드도 함께 생성 (검증용)
"""

import json
from anthropic import Anthropic


PROMPT = """You are a Korea travel content strategist for English-speaking foreign travelers.

Generate 10 NEW provocative Threads post ideas for today.
Each idea should be something foreign travelers visiting Korea would find genuinely intriguing.

[CATEGORIES - generate 2 ideas per category]

1. 💰 Price/Cost Shock
   Examples: "Korea botox is 1/5 of US price", "Why glasses in Korea are so cheap"

2. ⚠️ Scams/Tourist Traps
   Examples: "Airport taxi scam in Korea", "Myeongdong tourist traps"

3. 🤫 Insider Info (Things Koreans Don't Tell Foreigners)
   Examples: "Where Koreans get K-beauty", "Real BBQ spots Koreans love"

4. 😅 Regrets/Mistakes
   Examples: "Why foreigners regret Myeongdong day 1", "K-beauty products foreigners wrongly buy"

5. 🎁 Limited-Time Deals/Special Offers
   Examples: "Foreigner-only free Hanbok service", "KTX pass only foreigners can buy"

[FOR EACH IDEA, PROVIDE]
1. The provocative idea (1 English sentence)
2. The Korean translation (1 Korean sentence)
3. 2-3 search keywords to verify this fact (mix of English and Korean)

[RULES]
- Each idea must be SPECIFIC (mention numbers, places, brands)
- Make foreigners think "Wait, really?"
- Avoid clichés
- NO obviously fake statistics
- Search keywords should target REAL articles that could verify the claim

[OUTPUT FORMAT]
Return ONLY valid JSON (no markdown, no extra text):
{
  "price_shock": [
    {
      "idea_en": "English idea sentence",
      "idea_kr": "한국어 번역",
      "search_keywords": ["keyword 1", "keyword 2"]
    },
    {
      "idea_en": "...",
      "idea_kr": "...",
      "search_keywords": ["...", "..."]
    }
  ],
  "scams": [...],
  "insider": [...],
  "regrets": [...],
  "deals": [...]
}
"""


def get_client(api_key):
    return Anthropic(api_key=api_key)


def generate_ideas(client):
    """매일 새 10개 주제 + 검색 키워드 생성"""
    try:
        msg = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=3500,
            messages=[{"role": "user", "content": PROMPT}],
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
        print(f"[ERROR] 아이디어 생성 실패: {e}")
        return None
