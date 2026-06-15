"""
Threads 아이디어 사실 검증기
- 각 아이디어의 검색 키워드로 Google News 검색
- 검색 결과를 Claude에게 보여서 사실 검증
- 결과: ✅ 검증됨 / ⚠️ 부분 검증 / ❌ 검증 실패
"""

import json
import time
import feedparser
from urllib.parse import quote
from anthropic import Anthropic


def is_korean(text):
    """한국어 키워드 판별"""
    for char in text:
        if '\uac00' <= char <= '\ud7a3':
            return True
    return False


def gnews_search(query, limit=5):
    """Google News에서 키워드 검색"""
    if is_korean(query):
        url = f"https://news.google.com/rss/search?q={quote(query)}&hl=ko&gl=KR&ceid=KR:ko"
    else:
        url = f"https://news.google.com/rss/search?q={quote(query)}&hl=en-US&gl=US&ceid=US:en"
    
    try:
        d = feedparser.parse(url)
        results = []
        for e in d.entries[:limit]:
            results.append({
                "title": (e.get("title") or "").strip(),
                "summary": (e.get("summary") or "").strip()[:200],
                "source": d.feed.get("title", ""),
            })
        return results
    except Exception as e:
        print(f"[WARN] 검색 실패 '{query}': {e}")
        return []


def search_for_idea(idea):
    """하나의 아이디어에 대한 모든 검색 결과 모으기"""
    keywords = idea.get("search_keywords", [])
    all_results = []
    
    for keyword in keywords[:3]:  # 최대 3개 키워드
        results = gnews_search(keyword, limit=3)
        all_results.extend(results)
        time.sleep(0.5)  # Google 부하 방지
    
    return all_results


VERIFY_PROMPT = """You are fact-checking a Threads post idea against real news search results.

[IDEA]
{idea_en}

[SEARCH RESULTS]
{search_results}

[YOUR TASK]
Evaluate if the search results SUPPORT or CONTRADICT the idea.

Verification levels:
- "verified": Search results contain CONCRETE FACTS supporting the idea (specific numbers, sources, names)
- "partial": Some related info but doesn't fully confirm the specific claim
- "unverified": Search results don't contain relevant info OR the idea is too generic to verify

Return ONLY valid JSON:
{{
  "status": "verified | partial | unverified",
  "reason": "1 sentence in Korean explaining why",
  "supporting_evidence": "If verified, specific fact found (1 sentence). Otherwise empty."
}}

IMPORTANT:
- Be STRICT. Don't mark "verified" unless results have concrete supporting facts.
- If search returned 0 useful results → "unverified"
- If results are general K-beauty news without specific data → "partial"
"""


def verify_idea(client, idea, search_results):
    """Claude로 아이디어 검증"""
    if not search_results:
        return {
            "status": "unverified",
            "reason": "검색 결과 없음",
            "supporting_evidence": "",
        }
    
    # 검색 결과 텍스트화
    results_text = ""
    for i, r in enumerate(search_results[:8], 1):  # 최대 8개만
        results_text += f"\n{i}. [{r.get('source','')}] {r.get('title','')}\n   {r.get('summary','')[:150]}\n"
    
    prompt = VERIFY_PROMPT.format(
        idea_en=idea.get("idea_en", ""),
        search_results=results_text,
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
        if start != -1 and end != -1 and end > start:
            text = text[start:end+1]
        
        return json.loads(text)
    
    except Exception as e:
        print(f"[WARN] 검증 실패: {e}")
        return {
            "status": "unverified",
            "reason": f"검증 오류: {e}",
            "supporting_evidence": "",
        }


def verify_all_ideas(api_key, ideas_data):
    """모든 카테고리 × 아이디어 검증"""
    client = Anthropic(api_key=api_key)
    
    total = sum(len(ideas_data.get(cat, [])) for cat in ideas_data)
    current = 0
    
    for category, ideas in ideas_data.items():
        for idea in ideas:
            current += 1
            print(f"  검증 중 ({current}/{total}): {idea.get('idea_en','')[:50]}")
            
            # 1. 검색
            search_results = search_for_idea(idea)
            
            # 2. 검증
            verification = verify_idea(client, idea, search_results)
            
            # 3. 아이디어에 검증 결과 추가
            idea["verification"] = verification
            idea["search_count"] = len(search_results)
            
            time.sleep(0.3)
    
    return ideas_data
