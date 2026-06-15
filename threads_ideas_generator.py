"""
Threads 콘텐츠 아이디어 생성기
- 매일 Claude가 5개 카테고리 × 각 2개 = 10개 새 주제 생성
- 방한 외국인이 흥미로워할 토픽 위주
"""

import json
from anthropic import Anthropic


PROMPT = """You are a Korea travel content strategist for English-speaking foreign travelers.

Generate 10 NEW provocative Threads post ideas for today.
Each idea should be something foreign travelers visiting Korea would find genuinely intriguing.

[CATEGORIES - generate 2 ideas per category]

1. 💰 Price/Cost Shock
   - Things shockingly cheap or expensive in Korea
   - Korea vs US/Europe price comparisons
   - Hidden cost discoveries
   - Examples: "Korea botox is 1/5 of US price", "Why glasses in Korea are so cheap"

2. ⚠️ Scams/Tourist Traps
   - Things foreigners get ripped off on
   - Hidden fees, tourist-only pricing
   - Common scam patterns
   - Examples: "Airport taxi scam in Korea", "Myeongdong tourist traps"

3. 🤫 Insider Info (Things Koreans Don't Tell Foreigners)
   - Local secrets, hidden spots
   - Where Koreans actually go vs tourist spots
   - Insider tricks
   - Examples: "Where Koreans get K-beauty", "Real BBQ spots Koreans love"

4. 😅 Regrets/Mistakes
   - What foreigners regret doing in Korea
   - Common first-day mistakes
   - Things foreigners wish they knew
   - Examples: "Why foreigners regret Myeongdong day 1", "K-beauty products foreigners wrongly buy"

5. 🎁 Limited-Time Deals/Special Offers
   - Foreigner-only discounts and free services
   - Government promotions for tourists
   - Seasonal special deals
   - Examples: "Foreigner-only free Hanbok service", "KTX pass only foreigners can buy"

[RULES]
- Each idea must be SPECIFIC and intriguing (not generic)
- Use NUMBERS, SPECIFIC PLACES, REAL TRENDS when possible
- Each idea: ONE provocative sentence in English
- Make foreigners think "Wait, really?" or "I need to know this"
- Avoid clichés like "Top 10 things in Seoul"
- NO fake statistics - use real Korean culture/business knowledge

[OUTPUT FORMAT]
Return ONLY valid JSON (no markdown, no extra text):
{
  "price_shock": [
    "idea 1 (one provocative sentence)",
    "idea 2"
  ],
  "scams": [
    "idea 1",
    "idea 2"
  ],
  "insider": [
    "idea 1",
    "idea 2"
  ],
  "regrets": [
    "idea 1",
    "idea 2"
  ],
  "deals": [
    "idea 1",
    "idea 2"
  ]
}
"""


def get_client(api_key):
    return Anthropic(api_key=api_key)


def generate_ideas(client):
    """매일 새 10개 주제 생성"""
    try:
        msg = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=2000,
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
