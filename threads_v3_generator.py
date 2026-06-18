"""
Threads V3 콘텐츠 생성기
- V3 정의서 4단 구조 (본문 + 댓글 1/2/3)
- 카톡 친구 톤 (Level 3 가벼움)
- 브랜드명 비공개 + 키워드 매그넷
- 영문 + 한글 번역
- 이모지 사용 안 함
"""

import json
import time
from anthropic import Anthropic

from threads_v3_topics import get_topic_config


PROMPT_TEMPLATE = """You are a Korean local writing Threads posts for foreign travelers visiting Korea.

[TOPIC TODAY]
Keyword: {keyword}
Topic: {topic}
Post Type: {post_type}
Main Problem: {main_problem}
Core Insight: {core_insight}
Pglemaps Benefit (for comment 3): {pglemaps_benefit}

[YOUR TASK]
Create a complete Threads post (main + 3 comments) following the V3 structure.

[TONE - CRITICAL]
Write like you're texting a friend who's planning a Korea trip.
- Casual, conversational, slightly humorous
- Short choppy sentences
- Use "you" directly
- Natural expressions like "Okay so", "Here's the deal", "It's a whole thing", "Btw", "Drop"
- No emojis at all
- No formal phrases like "It is important to note that..."
- No "tourists" or "foreigners" - use "you" or "everyone"

[STRUCTURE - V3 RULES]

MAIN POST:
- Strong hook that breaks expectations or creates curiosity
- Don't reveal the answer
- Make people NEED to read comment 1
- 5-8 short lines, choppy rhythm
- End with something that triggers "wait what?" feeling
- Add [Topic: Korea Travel] at the end

COMMENT 1:
- Resolve the curiosity from main post
- Explain WHY the problem exists
- Make reader think "ah, that's why"
- 5-7 lines, still casual

COMMENT 2:
- Practical advice with SAVE value
- Could be a quick cheat sheet, comparison, or actionable tip
- Make reader want to bookmark this
- End with something like "Save this", "Trust me", "You'll thank me"

COMMENT 3 (CRITICAL RULES):
- Connect to the problem from main/comment 1/2
- Frame manual solution as annoying ("don't trust some random list", "stop switching between apps")
- Introduce Pglemaps benefit WITHOUT mentioning the brand name
- Use phrases like:
  * "There's this free Korea trip planner"
  * "There's a free website that lets you..."
  * "There's a free planner for Korea travelers"
- End with: "Drop "{keyword}" below and I'll send it" OR similar variant

[FORBIDDEN]
- DO NOT mention "Pglemaps", "Pgle Maps", or "pglemaps.com" anywhere in any post or comment
- DO NOT use emojis
- DO NOT use formal phrases
- DO NOT use fake statistics or made-up numbers
- DO NOT say "no signup needed" (signup IS required)
- DO NOT use "tourists" or "foreigners" - use "you" or "everyone"

[KOREAN TRANSLATION]
Also provide Korean translation in casual conversational tone:
- Use "~예요/이에요" not "~합니다"
- Short choppy sentences like Korean group chat
- Natural expressions like "자", "이거", "진짜", "제발", "참"
- No emojis
- Match the casual energy of English version

[OUTPUT - VALID JSON ONLY]
{{
  "main_post_en": "main post in English",
  "comment_1_en": "comment 1 in English",
  "comment_2_en": "comment 2 in English",
  "comment_3_en": "comment 3 in English with keyword magnet",
  "main_post_kr": "본문 한글",
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
    
    prompt = PROMPT_TEMPLATE.format(
        keyword=keyword,
        topic=config.get("topic", ""),
        post_type=config.get("post_type", ""),
        main_problem=config.get("main_problem", ""),
        core_insight=config.get("core_insight", ""),
        pglemaps_benefit=config.get("pglemaps_benefit", ""),
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
        content["topic"] = config.get("topic", "")
        content["post_type"] = config.get("post_type", "")
        
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
