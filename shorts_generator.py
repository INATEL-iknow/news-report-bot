"""
유튜브 쇼츠 대본 생성기 (2단계 파이프라인)
- Step 1: Claude Haiku로 화제성 평가 + 상위 3개 선정
- Step 2: Claude Opus로 심층 대본 생성 (자극적 + 공감 + 분쟁 CTA)
"""

import json
import time
from anthropic import Anthropic


# Step 1: 화제성 평가 프롬프트 (Haiku - 빠르고 저렴)
EVALUATION_PROMPT = """You are evaluating entertainment news for YouTube Shorts virality.

[ARTICLE]
Title: {title}
Source: {source}
Category: {category}
Summary: {summary}

[YOUR TASK]
Score this article on YouTube Shorts virality potential.

Return ONLY valid JSON:
{{
  "virality_score": 1-10,
  "category": "domestic" or "global",
  "subcategory": "breakup/wedding/scandal/comeback/collab/controversy/other",
  "hook_potential": "one sentence in Korean about what makes it viral",
  "target_audience": "who would click this shorts (Korean)",
  "reason_kr": "왜 이 화제성 점수인지 한국어로 1문장"
}}

RULES:
- score 10 = 초대박 이슈 (모든 매체가 다룸, 논란/충격/화제 폭발)
- score 8-9 = 대형 이슈 (특정 팬층 폭발적 반응)
- score 6-7 = 중형 이슈 (일반 관심)
- score 4-5 = 소형 이슈 (팬층만 관심)
- score 1-3 = 무관/광고성/재탕
- 이미 매우 오래된 이슈는 감점
- 단순 홍보성은 감점
- 논란/스캔들/충격 요소는 가점
"""


# Step 2: 대본 생성 프롬프트 (Opus - 고품질 콘텐츠)
SCRIPT_GENERATION_PROMPT = """You are writing a viral YouTube Shorts script for a Korean entertainment news channel.

[ISSUE INFO]
Title: {title}
Source: {source}
Category: {category}
Subcategory: {subcategory}
Hook Potential: {hook_potential}
Original Summary: {summary}
Link: {link}

============================================================
YOUR TASK: Write a complete 60-second YouTube Shorts script
============================================================

[TONE REQUIREMENTS]
- 자극적이면서도 정보 전달
- 시청자 공감 포인트 중간중간 삽입
- CTA는 분쟁/의견대립 유도 질문 (예/아니오로 나뉘는)
- TTS 자연 발화용 (자연스러운 문장 흐름)
- 카톡 친구 톤 아님, 뉴스 나레이터 톤 (하지만 딱딱하지 않게)

[STRUCTURE - MUST FOLLOW]
Total: 약 60초 (한국어 280-310자)

1. 후킹 (3초, 약 15-25자):
   - 공감 유도 시작 ("다들 ~하죠?", "이거 상상 되세요?", "다들 놀란 표정 지으셨죠?")
   - 또는 강력한 팩트 (충격/의외성)
   
2. 본문 (40초, 약 180-210자):
   - 이슈 상세 설명
   - 중간중간 공감 포인트 삽입 ("이거 그대로 믿기엔 뭔가 이상하죠?", "다들 그냥 지나쳤는데")
   - 구체적 인용 or 세부사항 필수
   - 인물 이름, 날짜, 장소 등 팩트 강화
   
3. 반전/포인트 (10초, 약 45-55자):
   - 놀라운 추가 정보 or 의혹 제기
   - "근데 ~", "사실은 ~" 시작
   
4. CTA (7초, 약 30-40자):
   - 반드시 분쟁 유도 질문 (예/아니오 나뉘는)
   - 예시: "~ 진짜일까요, 아니면 ~일까요?"
   - 예시: "~해도 될까요?"
   - 예시: "~에 동의하시나요?"
   - 끝: "댓글로 여러분 생각 남겨주세요"

[FORBIDDEN]
- 이모지 사용 금지
- "자," 같은 필러 금지
- 너무 정중한 표현 금지
- 확인 안 된 팩트 지어내기 금지
- "쓸데없는" 홍보 문구 금지

[ENGLISH SUBTITLES]
Also generate English subtitles for the video (10-11 cuts).
Format: "TIME  SUBTITLE" (each under 8 words, punchy)
Time format: MM:SS

[SUMMARY]
Also write a 5-6 line factual summary in Korean of the actual article.

[OUTPUT - VALID JSON ONLY]
{{
  "issue_info": {{
    "category_kr": "국내 or 해외",
    "subcategory_kr": "카테고리 한국어",
    "virality_stars": "⭐⭐⭐⭐⭐ (1-5개)",
    "hook_summary": "한국어 1문장으로 어떤 훅인지"
  }},
  "article_summary_kr": [
    "5-6줄 팩트 요약, 각 줄은 한 문장",
    "구체적 인물명, 날짜, 인용 포함",
    "..."
  ],
  "script_kr": {{
    "hook": "후킹 부분 (0:00-0:04)",
    "body": "본문 부분 (0:04-0:43)",
    "twist": "반전 부분 (0:43-0:53)",
    "cta": "CTA 부분 (0:53-1:00)"
  }},
  "english_subtitles": [
    "0:00  first subtitle",
    "0:04  second subtitle",
    "..."
  ],
  "char_count": 총_한국어_문자수
}}
"""


def get_client(api_key):
    return Anthropic(api_key=api_key)


def evaluate_articles(client, items):
    """Step 1: 각 기사 화제성 평가 (Haiku 사용)"""
    print(f"🤖 Step 1: {len(items)}건 화제성 평가 중...")
    
    evaluated = []
    for i, item in enumerate(items, 1):
        if i % 20 == 0:
            print(f"  진행: {i}/{len(items)}")
        
        prompt = EVALUATION_PROMPT.format(
            title=item.get("title", ""),
            source=item.get("source", ""),
            category=item.get("category", ""),
            summary=item.get("summary", "")[:400],
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
            if start != -1 and end != -1:
                text = text[start:end+1]
            
            evaluation = json.loads(text)
            item["evaluation"] = evaluation
            evaluated.append(item)
        
        except Exception as e:
            print(f"[WARN] 평가 실패: {item.get('title','')[:30]} - {e}")
        
        time.sleep(0.1)  # Rate limit 방지
    
    return evaluated


def select_top_3(evaluated_items):
    """Step 1.5: 상위 3개 선정 (화제성 순, 국내/해외 균형)"""
    print("\n🎯 상위 3개 선정 중...")
    
    # 점수순 정렬
    evaluated_items.sort(
        key=lambda x: x.get("evaluation", {}).get("virality_score", 0),
        reverse=True,
    )
    
    # 국내/해외 분리
    domestic = [i for i in evaluated_items 
                if i.get("evaluation", {}).get("category") == "domestic"]
    global_items = [i for i in evaluated_items 
                    if i.get("evaluation", {}).get("category") == "global"]
    
    # 균형 있게 3개 선정
    # 기본: 화제성 순으로 상위 3개
    # 다만 국내/해외 모두 있으면 최소 각 1개씩 포함
    top_3 = []
    
    # 가장 화제성 높은 것 1개 무조건
    if evaluated_items:
        top_3.append(evaluated_items[0])
    
    # 국내/해외 균형
    domestic_added = 1 if top_3 and top_3[0] in domestic else 0
    global_added = 1 if top_3 and top_3[0] in global_items else 0
    
    for item in evaluated_items[1:]:
        if len(top_3) >= 3:
            break
        if item in top_3:
            continue
        
        is_domestic = item in domestic
        
        # 국내/해외 균형 체크
        if is_domestic and domestic_added >= 2:
            continue
        if not is_domestic and global_added >= 2:
            continue
        
        top_3.append(item)
        if is_domestic:
            domestic_added += 1
        else:
            global_added += 1
    
    # 3개 안 채워지면 화제성 순으로 채움
    for item in evaluated_items:
        if len(top_3) >= 3:
            break
        if item not in top_3:
            top_3.append(item)
    
    print(f"✅ 선정 완료:")
    for i, item in enumerate(top_3, 1):
        eval_data = item.get("evaluation", {})
        print(f"  {i}. [{eval_data.get('category', '?')}] "
              f"화제성 {eval_data.get('virality_score', 0)}/10 - "
              f"{item.get('title', '')[:40]}")
    
    return top_3


def generate_script(client, item):
    """Step 2: 단일 이슈에 대한 심층 대본 생성 (Opus 사용)"""
    evaluation = item.get("evaluation", {})
    
    prompt = SCRIPT_GENERATION_PROMPT.format(
        title=item.get("title", ""),
        source=item.get("source", ""),
        category=evaluation.get("category", ""),
        subcategory=evaluation.get("subcategory", ""),
        hook_potential=evaluation.get("hook_potential", ""),
        summary=item.get("summary", "")[:800],
        link=item.get("link", ""),
    )
    
    try:
        msg = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=2500,
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
        if start != -1 and end != -1:
            text = text[start:end+1]
        
        script = json.loads(text)
        
        # 원본 기사 정보 추가
        script["original_title"] = item.get("title", "")
        script["original_link"] = item.get("link", "")
        script["original_source"] = item.get("source", "")
        script["evaluation"] = evaluation
        
        return script
    
    except Exception as e:
        print(f"[ERROR] 대본 생성 실패: {item.get('title','')[:30]} - {e}")
        return None


def generate_all_scripts(api_key, items):
    """전체 파이프라인: 평가 → 선정 → 대본 생성"""
    if not api_key:
        print("[WARN] API 키 없음")
        return []
    
    client = get_client(api_key)
    
    # Step 1: 화제성 평가
    evaluated = evaluate_articles(client, items)
    
    if not evaluated:
        print("❌ 평가된 항목 없음")
        return []
    
    # Step 1.5: 상위 3개 선정
    top_3 = select_top_3(evaluated)
    
    # Step 2: 대본 생성
    print(f"\n🎬 Step 2: {len(top_3)}개 대본 생성 중...")
    
    scripts = []
    for i, item in enumerate(top_3, 1):
        print(f"  {i}/{len(top_3)} 생성 중: {item.get('title','')[:40]}")
        script = generate_script(client, item)
        if script:
            scripts.append(script)
        time.sleep(0.5)
    
    print(f"✅ 총 {len(scripts)}개 대본 완성")
    return scripts
