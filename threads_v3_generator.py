"""
Threads V3 콘텐츠 생성기 (피드백 반영 V2)
- 톤 일관성 강제 (본문/댓글 모두 같은 친구 톤)
- 필러 단어 금지 ("자", "Cute", "Love that for you" 등)
- 기승전결 구조 강제
- 피글맵 진짜 기능만 사용
- 영문 + 한글 동시 생성
"""

import json
import time
from anthropic import Anthropic

from threads_v3_topics import get_topic_config, get_post_type_info, PGLEMAPS_REAL_FEATURES


PROMPT_TEMPLATE = """You are a Korean local writing Threads posts for foreign travelers visiting Korea.

[TOPIC METADATA]
Keyword: {keyword}
Category: {category_name}
Target: {target_traveler}

What they already know: {what_already_know}
What they don't know: {what_dont_know}

Main Hook: {main_hook}
Post Type: {post_type_name} - {post_type_description}

[CONTENT BLUEPRINT - use as guide, write in your own voice]
Comment 1 answer: {comment_1_answer}
Comment 2 real tip: {comment_2_real_tip}
Comment 3 Pglemaps benefit: {comment_3_real_feature}

[PGLEMAPS REAL FEATURES - ONLY USE THESE]
{real_features}

[ABSOLUTELY FORBIDDEN CLAIMS - DO NOT WRITE THESE]
{forbidden_claims}

============================================================
TONE REQUIREMENTS (CRITICAL)
============================================================

Write like you're texting a friend who's planning a Korea trip.
The SAME tone must run through main post and ALL 3 comments.

DO use:
- Conversational casual English
- Short choppy sentences
- "you" directly
- Light natural humor when fitting
- Phrases like "Here's the deal", "Btw", "Honestly", "The thing is"
- "Trust me", "Save this", "You'll thank me later"

DO NOT use:
- "Cute. Love that for you." - sounds mocking, NEVER use this
- "Spoiler:" - filler word, never use
- "자," - meaningless Korean filler
- "Sorry not sorry" - cliché
- Any condescending tone
- Sarcastic put-downs
- Emojis (zero, ever)
- Formal phrases like "It is important to note"
- "tourists" or "foreigners" - use "you" or "everyone"
- Sudden tone shifts between main post and comments
- Buzzwords like "literally", "actually" used as fillers

CONSISTENCY CHECK:
After writing, the main post and all 3 comments should sound like
the same person continuing one conversation. Not like they were
written by 4 different people.

============================================================
STRUCTURE REQUIREMENTS
============================================================

MAIN POST (must follow 기승전결 / setup-build-twist-hook):
1. SETUP (1-2 lines): State the situation directly
2. BUILD (2-3 lines): Add context, raise the stakes
3. TWIST (1-2 lines): Reveal there's a hidden problem
4. HOOK (1 line): Make them HAVE to read comment 1

Example structure (for HOTEL topic):
"Booking Myeongdong for your Seoul trip?           [SETUP]
Most people do. It's central, it's popular,
travel guides love it.                              [BUILD]
But popular and 'right for your trip' aren't       [TWIST]
the same thing.
Here's why this matters more than you think."       [HOOK]

End with: [Topic: Korea Travel]

COMMENT 1 (resolve curiosity):
- Open with continuity from main post
- Explain the actual WHY using the comment_1_answer blueprint
- 5-7 lines, same casual tone as main post
- End in a way that leads to comment 2

COMMENT 2 (save-worthy info):
- Open with practical pivot ("Here's what works:", "The fix:", "Try this:")
- Format as clean bullet list using dashes (-), never emojis
- Use comment_2_real_tip blueprint
- End with: "Save this", "Trust me", "You'll thank me later"

COMMENT 3 (Pglemaps + magnet):
- Open by acknowledging the problem from main/comment 1/2
- Frame manual solution as annoying (random screenshots, scattered lists, etc.)
- Introduce Pglemaps benefit WITHOUT brand name
- Use phrases like:
  * "There's a free Korea trip planner that lets you..."
  * "There's a free website where you can..."
  * "There's a free map-based planner for Korea travelers..."
- Use the comment_3_real_feature blueprint
- End with magnet: 'Drop "{keyword}" below and I\\'ll send it'

============================================================
KOREAN TRANSLATION (구어체)
============================================================

- Use "~예요/이에요" not "~합니다"
- Short choppy sentences like Korean group chat
- Natural fillers OK: "솔직히", "근데", "이거", "진짜", "참"
- NEVER use "자," at the start of sentences (sounds weird)
- NEVER use Korean equivalents of "Cute" or "Love that for you"
- No emojis
- Match the casual energy of English

============================================================
OUTPUT - VALID JSON ONLY
============================================================

{{
  "main_post_en": "main post in English with [Topic: Korea Travel] at end",
  "comment_1_en": "comment 1 in English",
  "comment_2_en": "comment 2 in English",
  "comment_3_en": "comment 3 in English with keyword magnet at end",
  "main_post_kr": "본문 한글 (구어체)",
  "comment_1_kr": "댓글 1 한글",
  "comment_2_kr": "댓글 2 한글",
  "comment_3_kr": "댓글 3 한글"
}}
"""


def get_client(api_key):
    return Anthropic(api_key=api_key)


def generate_content(client, keyword):
    """단일 키워드에 대한 V3 콘텐츠 생성"""
    config = get_topic_config(keyword)
    
    if not config:
        print(f"[WARN] '{keyword}' 설정 없음")
        return None
    
    post_type = config.get("post_type", "controversial")
    post_type_info = get_post_type_info(post_type)
    
    forbidden_list = config.get("forbidden_claims", [])
    forbidden_text = "\n".join(f"- {claim}" for claim in forbidden_list)
    if not forbidden_text:
        forbidden_text = "- (none specific)"
    
    prompt = PROMPT_TEMPLATE.format(
        keyword=keyword,
        category_name=config.get("category_name", ""),
        target_traveler=config.get("target_traveler", ""),
        what_already_know=config.get("what_already_know", ""),
        what_dont_know=config.get("what_dont_know", ""),
        main_hook=config.get("main_hook", ""),
        post_type_name=post_type_info.get("name_kr", post_type),
        post_type_description=post_type_info.get("description", ""),
        comment_1_answer=config.get("comment_1_answer", ""),
        comment_2_real_tip=config.get("comment_2_real_tip", ""),
        comment_3_real_feature=config.get("comment_3_real_feature", ""),
        real_features=PGLEMAPS_REAL_FEATURES,
        forbidden_claims=forbidden_text,
    )
    
    try:
        msg = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=3000,
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
        
        content = json.loads(text)
        
        content["keyword"] = keyword
        content["category_name"] = config.get("category_name", "")
        content["post_type"] = post_type
        content["post_type_kr"] = post_type_info.get("name_kr", "")
        
        # 브랜드명 노출 검증
        all_text = " ".join([
            content.get("main_post_en", ""),
            content.get("comment_1_en", ""),
            content.get("comment_2_en", ""),
            content.get("comment_3_en", ""),
        ]).lower()
        
        forbidden_brands = ["pglemaps", "pgle maps", "pgle map", "pglemaps.com"]
        for brand in forbidden_brands:
            if brand in all_text:
                content["brand_leak_warning"] = f"'{brand}' 노출됨"
                break
        
        # 필러 단어 검증 (피드백 반영)
        forbidden_phrases = [
            "cute. love that for you",
            "love that for you",
            "spoiler:",
            "sorry not sorry",
        ]
        for phrase in forbidden_phrases:
            if phrase in all_text:
                content["filler_warning"] = f"필러 단어 '{phrase}' 감지됨"
                break
        
        return content
    
    except Exception as e:
        print(f"[ERROR] '{keyword}' 콘텐츠 생성 실패: {e}")
        return None


def generate_multiple_contents(client, keywords):
    """여러 키워드에 대한 콘텐츠 일괄 생성"""
    contents = []
    
    for i, keyword in enumerate(keywords, 1):
        print(f"  {i}/{len(keywords)} 생성 중: {keyword}")
        content = generate_content(client, keyword)
        if content:
            contents.append(content)
        time.sleep(0.5)
    
    return contents
