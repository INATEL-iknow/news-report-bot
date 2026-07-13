"""
유튜브 쇼츠 후킹 자동화 (Haiku 전용)
- Step 1: 화제성 평가 + key_subjects/issue_id 추출
- Step 1.5: 국내 8 + 해외 2 고정 (중복 방지 + 유연 대체)
- Step 2: 각 이슈마다 후킹 3개 옵션 + 요약 생성
"""

import json
import time
from anthropic import Anthropic


# ============================================================
# Step 1: 화제성 평가 프롬프트
# ============================================================
EVALUATION_PROMPT = """You are evaluating entertainment news for YouTube Shorts virality.

[ARTICLE]
Title: {title}
Source: {source}
Category: {category}
Summary: {summary}

[YOUR TASK]
Score this article on YouTube Shorts virality potential.
Also identify the CORE subjects and issue ID for duplicate detection.

Return ONLY valid JSON:
{{
  "virality_score": 1-10,
  "category": "domestic" or "global",
  "subcategory": "breakup/wedding/scandal/comeback/collab/controversy/other",
  "key_subjects": ["주요 인물 이름1", "주요 인물 이름2"],
  "issue_id": "core-issue-slug-YYYY",
  "hook_potential": "one sentence in Korean about what makes it viral",
  "target_audience": "who would click this shorts (Korean)",
  "reason_kr": "왜 이 화제성 점수인지 한국어로 1문장"
}}

RULES for virality_score:
- score 10 = 초대박 이슈 (모든 매체가 다룸, 논란/충격/화제 폭발)
- score 8-9 = 대형 이슈 (특정 팬층 폭발적 반응)
- score 6-7 = 중형 이슈 (일반 관심)
- score 4-5 = 소형 이슈 (팬층만 관심)
- score 1-3 = 무관/광고성/재탕
- 이미 매우 오래된 이슈는 감점
- 단순 홍보성은 감점
- 논란/스캔들/충격 요소는 가점

RULES for key_subjects:
- 기사에 등장하는 핵심 인물 이름 (최대 3명)
- 예: ["아이유", "이종석"] or ["Taylor Swift", "Travis Kelce"]
- 그룹명도 포함 가능: ["BTS", "정국"]

RULES for issue_id:
- 이슈의 핵심을 요약한 슬러그 (소문자, 하이픈)
- 예: "iu-lee-jongsuk-breakup-2026"
- 예: "taylor-travis-wedding-2026"
- 같은 이슈에서 파생된 기사들은 반드시 같은 issue_id
"""


# ============================================================
# Step 2: 후킹 3개 옵션 생성 프롬프트
# ============================================================
HOOK_GENERATION_PROMPT = """You are creating YouTube Shorts hooks for a Korean entertainment news channel.

[ISSUE]
Title: {title}
Source: {source}
Category: {category}
Subcategory: {subcategory}
Key Subjects: {key_subjects}
Hook Potential: {hook_potential}
Summary: {summary}
Link: {link}

============================================================
YOUR TASK: Create 3 different HOOKS (3-second attention grabbers)
============================================================

[HOOK DEFINITION - 매우 중요]
후킹은 시청자가 스크롤을 멈추게 하는 첫 3초 대사입니다.
결과를 밝히지 않고 궁금증을 극대화해야 합니다.

[✅ 좋은 후킹 예시]
- "아이유가 결국 이걸 참지 못했다"
- "유인나가 4개월 전에 이미 알고 있었다"
- "이종석 팬들만 감지했던 그 신호"
- "테일러 스위프트 결혼식장에서 벌어진 일"
- "정국의 이 행동이 K-POP 판을 뒤집었다"

[❌ 나쁜 후킹 예시 - 절대 만들지 마세요]
- "아이유 이종석 4년 만에 결별" (결과 밝힘)
- "다들 잘 될 줄 알았죠? 4년 만에 결별" (밋밋함)
- "결혼식 하나에 하객이 천 명?" (정보 나열)
- "BTS 정국이 신인 걸그룹 언급" (뉴스 헤드라인)

[HOOK 생성 공식 - 5가지 중 랜덤하게 사용]

1. "결국 이걸" 공식:
   - "[인물]이 결국 [행동]을 참지 못했다"
   - "[인물]이 결국 [행동]을 하고야 말았다"

2. "숨겨진 신호" 공식:
   - "[인물]이 [기간] 전에 이미 남긴 신호"
   - "[인물]만 알고 있던 그 진실"
   - "[인물] 팬들만 감지했던 그 신호"

3. "판이 바뀐 순간" 공식:
   - "[인물]의 이 행동이 [업계] 판을 뒤집었다"
   - "[업계]가 이 순간 조용해졌다"

4. "밖으로 새어나온" 공식:
   - "[장소] 밖으로 새어나온 진짜 이야기"
   - "[방송/사건]에서 잘려나간 그 장면"

5. "숫자 미스터리" 공식:
   - "[숫자]가 무엇을 의미하는지 아세요?"
   - "이 [숫자]는 결국 [결과]로 이어졌다"

[FORBIDDEN - 절대 사용 금지]
- 이모지
- "결별", "결혼", "논란" 등 결과 직접 명시
- 팩트만 나열
- 물음표 남발
- 20자 이상 (너무 김)

[LENGTH]
- 각 후킹: 10-18자 사이

[SUMMARY]
Also write a 2-line factual summary in Korean.

[OUTPUT - VALID JSON ONLY]
{{
  "hooks": [
    "후킹 옵션 1 (10-18자)",
    "후킹 옵션 2 (다른 공식 사용, 10-18자)",
    "후킹 옵션 3 (또 다른 공식 사용, 10-18자)"
  ],
  "summary_kr": [
    "1줄 팩트 요약",
    "1줄 추가 팩트"
  ]
}}
"""


# ============================================================
# 클라이언트 초기화
# ============================================================
def get_client(api_key):
    return Anthropic(api_key=api_key)


# ============================================================
# Step 1: 화제성 평가
# ============================================================
def evaluate_articles(client, items):
    """Step 1: 각 기사 화제성 평가"""
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
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}],
            )
            text = msg.content[0].text.strip()
            
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
        
        time.sleep(0.1)
    
    return evaluated


# ============================================================
# Step 1.5: 중복 판정 헬퍼
# ============================================================
def _is_duplicate(item, selected_items):
    """이슈 중복 판정"""
    item_eval = item.get("evaluation", {})
    item_issue_id = item_eval.get("issue_id", "").strip().lower()
    item_subjects = set(
        s.strip().lower() for s in item_eval.get("key_subjects", []) if s
    )
    
    for selected in selected_items:
        sel_eval = selected.get("evaluation", {})
        sel_issue_id = sel_eval.get("issue_id", "").strip().lower()
        sel_subjects = set(
            s.strip().lower() for s in sel_eval.get("key_subjects", []) if s
        )
        
        if item_issue_id and sel_issue_id and item_issue_id == sel_issue_id:
            return True
        
        overlap = item_subjects & sel_subjects
        if len(overlap) >= 2:
            return True
        
        if len(item_subjects) == 1 and len(sel_subjects) == 1 and overlap:
            return True
    
    return False


def _pick_from_pool(pool, selected_items, count, min_score=4):
    """풀에서 중복 없이 상위 N개"""
    picked = []
    for item in pool:
        if len(picked) >= count:
            break
        
        score = item.get("evaluation", {}).get("virality_score", 0)
        if score < min_score:
            continue
        
        if _is_duplicate(item, selected_items + picked):
            continue
        
        picked.append(item)
    
    return picked


# ============================================================
# Step 1.5: 상위 10개 선정 (국내 8 + 해외 2)
# ============================================================
def select_top_10(evaluated_items):
    """국내 8 + 해외 2 고정 (중복 방지 + 유연 대체)"""
    print("\n🎯 상위 10개 선정 중 (국내 8 + 해외 2 목표)...")
    
    domestic_pool = sorted(
        [i for i in evaluated_items 
         if i.get("evaluation", {}).get("category") == "domestic"],
        key=lambda x: x.get("evaluation", {}).get("virality_score", 0),
        reverse=True,
    )
    global_pool = sorted(
        [i for i in evaluated_items 
         if i.get("evaluation", {}).get("category") == "global"],
        key=lambda x: x.get("evaluation", {}).get("virality_score", 0),
        reverse=True,
    )
    
    print(f"  국내 풀: {len(domestic_pool)}건 / 해외 풀: {len(global_pool)}건")
    
    # 국내 8개 (컷 4점)
    domestic_picked = _pick_from_pool(
        domestic_pool, selected_items=[], count=8, min_score=4
    )
    print(f"  국내 선정: {len(domestic_picked)}건")
    
    # 해외 2개 (컷 5점)
    global_picked = _pick_from_pool(
        global_pool, selected_items=domestic_picked, count=2, min_score=5
    )
    print(f"  해외 선정: {len(global_picked)}건")
    
    top_selected = domestic_picked + global_picked
    
    # 10개 못 채우면 국내로 채움
    if len(top_selected) < 10:
        print(f"  ⚠️ 10개 미달 ({len(top_selected)}개) → 국내 추가")
        extra = _pick_from_pool(
            domestic_pool,
            selected_items=top_selected,
            count=10 - len(top_selected),
            min_score=3,
        )
        top_selected.extend(extra)
    
    # 그래도 못 채우면 컷 낮춤
    if len(top_selected) < 10:
        all_pool = sorted(
            evaluated_items,
            key=lambda x: x.get("evaluation", {}).get("virality_score", 0),
            reverse=True,
        )
        extra = _pick_from_pool(
            all_pool,
            selected_items=top_selected,
            count=10 - len(top_selected),
            min_score=1,
        )
        top_selected.extend(extra)
    
    print(f"\n✅ 최종 선정:")
    for i, item in enumerate(top_selected, 1):
        eval_data = item.get("evaluation", {})
        cat = eval_data.get("category", "?")
        score = eval_data.get("virality_score", 0)
        subjects = ", ".join(eval_data.get("key_subjects", []))
        print(f"  {i}. [{cat}] 화제성 {score}/10 · 인물: {subjects}")
        print(f"     {item.get('title', '')[:50]}")
    
    return top_selected


# ============================================================
# Step 2: 후킹 3개 옵션 생성
# ============================================================
def generate_hooks(client, item):
    """단일 이슈에 대한 후킹 3개 옵션 + 요약 생성"""
    evaluation = item.get("evaluation", {})
    
    prompt = HOOK_GENERATION_PROMPT.format(
        title=item.get("title", ""),
        source=item.get("source", ""),
        category=evaluation.get("category", ""),
        subcategory=evaluation.get("subcategory", ""),
        key_subjects=", ".join(evaluation.get("key_subjects", [])),
        hook_potential=evaluation.get("hook_potential", ""),
        summary=item.get("summary", "")[:600],
        link=item.get("link", ""),
    )
    
    try:
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=800,
            messages=[{"role": "user", "content": prompt}],
        )
        text = msg.content[0].text.strip()
        
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
        
        result = json.loads(text)
        
        # 원본 정보 추가
        result["original_title"] = item.get("title", "")
        result["original_link"] = item.get("link", "")
        result["original_source"] = item.get("source", "")
        result["evaluation"] = evaluation
        
        return result
    
    except Exception as e:
        print(f"[ERROR] 후킹 생성 실패: {item.get('title','')[:30]} - {e}")
        return None


# ============================================================
# 전체 파이프라인
# ============================================================
def generate_all_hooks(api_key, items):
    """전체 파이프라인: 평가 → 선정 → 후킹 생성"""
    if not api_key:
        print("[WARN] API 키 없음")
        return []
    
    client = get_client(api_key)
    
    # Step 1: 화제성 평가
    evaluated = evaluate_articles(client, items)
    
    if not evaluated:
        print("❌ 평가된 항목 없음")
        return []
    
    # Step 1.5: 상위 10개 선정
    top_10 = select_top_10(evaluated)
    
    # Step 2: 각 이슈마다 후킹 3개 옵션 생성
    print(f"\n🎣 Step 2: {len(top_10)}개 이슈 후킹 생성 중...")
    
    results = []
    for i, item in enumerate(top_10, 1):
        print(f"  {i}/{len(top_10)}: {item.get('title','')[:40]}")
        hooks = generate_hooks(client, item)
        if hooks:
            results.append(hooks)
        time.sleep(0.2)
    
    print(f"✅ 총 {len(results)}개 이슈 후킹 완성")
    return results
