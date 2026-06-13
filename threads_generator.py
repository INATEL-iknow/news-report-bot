"""
Threads 콘텐츠 생성기 (Claude API)
- 본인이 정한 구조: 본문 + 댓글 3개
- 본문은 Open Loop (미완성 결말)
- 댓글 3은 Pglemaps 대세감 + DM 매그넷
"""

import json
from anthropic import Anthropic


PGLEMAPS_CONTEXT = """
[About Pglemaps]
Pglemaps (pglemaps.com/en) is a free Korea trip planner built for foreign travelers visiting Korea.
It's becoming a must-have tool that many foreign travelers in Korea already rely on.

What it does:
- Travelers save the places they want to visit (restaurants, K-Beauty clinics, Hanbok rental, etc.)
- Pglemaps auto-generates the most efficient route
- 100% free to use

Categories available on Pglemaps:
- Transportation (Airport Taxi, Car Rental, Shuttle, KTX)
- Beauty (Hair Salon, Dermatology, Color Analysis, Nail & Makeup)
- Snap & Experience (Hanbok, K-Pop Class, Cooking Class, Street Snap)
- Food & Drink (Restaurant, Wine Bar, Café)
- Tours (Museum, Theme Park, Guided Tour)
- Travel Essentials (Luggage Storage, SIM, Currency Exchange, Medical Translation)

Business model:
- Affiliate commissions from partner businesses when foreigners book through Pglemaps
"""


PROMPT_TEMPLATE = """You are a Korean local sharing real insider knowledge with foreign travelers on Threads.

[CONTEXT]
{pglemaps_context}

[TODAY'S TOPIC]
Category: {category}
Topic: {topic}

[YOUR TASK]
Generate a Threads post following this EXACT structure:

1. **MAIN POST** (body)
   - Hook: address foreign travelers directly ("Going to Seoul soon?" / "Planning a Korea trip?")
   - Mention what most foreign travelers usually do (the obvious choice)
   - Tease that there's a hidden/better option Koreans actually love
   - Briefly describe the appeal of this hidden option (2-3 specific benefits)
   - End with "The name of this place is —" or similar incomplete ending
   - DO NOT reveal the actual name in the body
   - DO NOT ask for comments explicitly
   - Length: 8-12 lines max
   - Tone: confident, direct, friendly

2. **COMMENT 1** (reveal the answer)
   - Reveal the actual place/spot name (in Korean + English)
   - Give 3-4 quick practical info bullets (location, best time, tips)
   - Length: 5-7 lines max

3. **COMMENT 2** (additional value)
   - Add 2-3 more underrated alternatives in the same category
   - Each with one-line description
   - Length: 5-7 lines max

4. **COMMENT 3** (Pglemaps social proof + DM magnet)
   - Start by addressing the real pain point (planning Korea trip is hard/messy)
   - List 3-4 specific pain points as bullet points
     (which neighborhood to stay, how to connect spots, transport options, booking order)
   - Frame Pglemaps as a must-have tool that many foreign travelers in Korea already use
   - Mention it's 100% free
   - DO NOT mention "no signup" or "no account needed" (signup IS required, don't lie)
   - End with: "Comment 'Pglemaps' below and I'll DM you the link 🗺️"
   - Length: 8-10 lines max

[STYLE RULES]
- Write in English (for English-speaking foreign travelers)
- Use emojis sparingly (1-2 per section max)
- NO fake statistics or made-up numbers (no "90% of travelers", "200+ users", etc.)
- NO buzzwords like "amazing", "incredible", "must-see"
- Direct, confident, Korean-style marketing tone
- Real specific names, locations, prices (when known)
- Brand name is ALWAYS "Pglemaps" (NOT "Piglemaps", NOT "PigleMaps")
- DO NOT claim "no signup required" - signup IS required on Pglemaps
- Frame Pglemaps as a must-have tool many foreign travelers in Korea already rely on

[OUTPUT FORMAT]
Return ONLY valid JSON in this exact format (no markdown, no extra text):
{{
  "main_post": "the main post body text",
  "comment_1": "comment 1 text",
  "comment_2": "comment 2 text",
  "comment_3": "comment 3 text",
  "topic_tag": "Korea Travel"
}}

IMPORTANT: The "topic_tag" should be ONE relevant Threads topic (e.g., "Korea Travel", "Seoul", "K-Beauty", "Korean Food").
"""


def get_client(api_key):
    return Anthropic(api_key=api_key)


def generate_threads_content(client, category, topic):
    """Claude API로 Threads 본문 + 댓글 3개 생성"""
    prompt = PROMPT_TEMPLATE.format(
        pglemaps_context=PGLEMAPS_CONTEXT,
        category=category,
        topic=topic,
    )
    
    try:
        msg = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}],
        )
        text = msg.content[0].text.strip()
        
        # 1차: ``` 코드 블록 제거
        if "```" in text:
            parts = text.split("```")
            if len(parts) >= 2:
                text = parts[1]
                if text.startswith("json"):
                    text = text[4:]
                text = text.strip()
        
        # 2차: JSON 추출 (첫 { 부터 마지막 } 까지)
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            text = text[start:end+1]
        
        return json.loads(text)
    
    except Exception as e:
        print(f"[ERROR] Threads 콘텐츠 생성 실패: {e}")
        return None
