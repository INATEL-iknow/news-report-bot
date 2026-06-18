"""
Threads V3 콘텐츠 생성기 (V3 정의서 완전 반영)
- V3 정의서 14개 메타데이터 모두 활용
- 4단 구조 (본문 + 댓글 1/2/3)
- 카톡 친구 톤 (Level 3)
- 브랜드명 비공개 + 키워드 매그넷
- 영문 + 한글 동시 생성
- 이모지 절대 금지
"""

import json
import time
from anthropic import Anthropic

from threads_v3_topics import get_topic_config, get_post_type_info


PROMPT_TEMPLATE = """You are a Korean local writing Threads posts for foreign travelers visiting Korea.

[TOPIC METADATA]
Keyword: {keyword}
Category: {category_name}
Target Traveler: {target_traveler}

What they already know: {what_foreigners_already_know}
What they don't know: {what_foreigners_do_not_know}

Main Hook: {main_hook}
Post Type: {post_type_name} - {post_type_description}

[CONTENT BLUEPRINT]
Comment 1 answer: {comment_1_answer}
Comment 2 real tip: {comment_2_real_tip}
Comment 3 Pglemaps benefit: {comment_3_pglemaps_benefit}

[FORBIDDEN CLAIMS - DO NOT WRITE]
{forbidden_claims}

[YOUR TASK]
Create a complete Threads post (main + 3 comments) following the V3 structure.
Use the blueprint above but write in YOUR voice, not copy-paste it.

[TONE - CRITICAL]
Write like you're texting a friend who's planning a Korea trip.
- Casual, conversational, slightly humorous
- Short choppy sentences
- Use "you" directly (never "tourists" or "foreigners")
- Natural expressions: "Okay so", "Here's the deal", "It's a whole thing", "Btw", "Drop", "Like", "Actually"
- Light humor or mild sass when fitting
- No emojis at all
- No formal phrases like "It is important to note that..."

[STRUCTURE - V3 RULES]

MAIN POST:
- Strong hook that breaks expectations or creates curiosity
- DO NOT reveal the answer in main post
- Make people NEED to read comment 1
- 5-8 short lines, choppy rhythm
- End with something that triggers "wait what?" or "ugh I'm doing this"
- Add [Topic: Korea Travel] at the end
- Reader should feel: "Why?", "I'm doing this", "I almost did this", "I need to see comments"

COMMENT 1:
- Resolve the curiosity from main post
- Explain WHY using the comment_1_answer blueprint
- Make reader think "ah, that's why"
- 5-7 lines, still casual
- End in a way that leads to comment 2

COMMENT 2:
- Practical advice with SAVE VALUE
- Use the comment_2_real_tip blueprint
- Could be a cheat sheet, comparison, or actionable tip
- Format as list/bullets if helpful (use dashes, NOT emojis)
- Make reader want to bookmark this
- End with: "Save this", "Trust me", "You'll thank me later" or similar

COMMENT 3 (CRITICAL RULES):
- Connect to the problem from main/comment 1/2
- Frame manual solution as annoying (random screenshots, switching apps, scattered lists)
- Introduce Pglemaps benefit WITHOUT mentioning the brand name
- Use phrases like:
  * "There's this free Korea trip planner"
  * "There's a free website that lets you..."
  * "There's a free map-based planner for Korea travelers"
- Use the comment_3_pglemaps_benefit blueprint
- End with: 'Drop "{keyword}" below and I'll send it' OR similar variant
  (Other variants: 'Comment "{keyword}" and I\\'ll DM you', 'Drop "{keyword}" - link in DM')

[ABSOLUTE FORBIDDEN]
- DO NOT mention "Pglemaps", "Pgle Maps", "pglemaps.com" anywhere
- DO NOT use ANY emojis (no exceptions)
- DO NOT use "tourists" or "foreigners" - use "you", "everyone", "people"
- DO NOT use fake statistics or made-up numbers
- DO NOT say "no signup needed" (signup IS required)
- DO NOT make claims listed in [FORBIDDEN CLAIMS] above
- DO NOT use formal/blog-style writing

[KOREAN TRANSLATION]
Provide Korean translation in casual conversational tone:
- Use "~예요/이에요" not "~합니다"
- Short choppy sentences like Korean group chat
- Natural fillers: "자", "이거", "진짜", "제발", "참", "솔직히", "근데"
- No emojis
- Match the casual energy of English version

[OUTPUT - VALID JSON ONLY]
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
    
    # forbidden_claims 리스트를 줄바꿈 텍스트로
    forbidden_list = config.get("forbidden_claims", [])
    forbidden_text = "\n".join(f"- {claim}" for claim in forbidden_list)
    if not forbidden_text:
        forbidden_text = "- (none specific)"
    
    prompt = PROMPT_TEMPLATE.format(
        keyword=keyword,
        category_name=config.get("category_name", ""),
        target_traveler=config.get("target_traveler", ""),
        what_foreigners_already_know=config.get("what_foreigners_already_know", ""),
        what_foreigners_do_not_know=config.get("what_foreigners_do_not_know", ""),
        main_hook=config.get("main_hook", ""),
        post_type_name=post_type_info.get("name_kr", post_type),
        post_type_description=post_type_info.get("description", ""),
        comment_1_answer=config.get("comment_1_answer", ""),
        comment_2_real_tip=config.get("comment_2_real_tip", ""),
        comment_3_pglemaps_benefit=config.get("comment_3_pglemaps_benefit", ""),
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
        
        # 메타데이터 추가
        content["keyword"] = keyword
        content["category_name"] = config.get("category_name", "")
        content["post_type"] = post_type
        content["post_type_kr"] = post_type_info.get("name_kr", "")
        
        # 브랜드명 노출 검증 (안전장치)
        all_text = " ".join([
            content.get("main_post_en", ""),
            content.get("comment_1_en", ""),
            content.get("comment_2_en", ""),
            content.get("comment_3_en", ""),
        ]).lower()
        
        forbidden_brands = ["pglemaps", "pgle maps", "pgle map", "pglemaps.com"]
        for brand in forbidden_brands:
            if brand in all_text:
                content["brand_leak_warning"] = f"⚠️ '{brand}' 노출됨 - 검토 필요"
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
        time.sleep(0.5)  # Rate limit 방지
    
    return contents
