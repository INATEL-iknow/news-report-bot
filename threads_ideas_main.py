"""
Threads 콘텐츠 아이디어 일일 발송 메인 실행 파일
- 매일 한국시간 08:30 발동
- Claude가 10개 아이디어 생성 + 검색 키워드
- Google News 검색으로 사실 검증
- 영문 + 한글 메일 발송
"""

from datetime import datetime

from threads_ideas_generator import get_client, generate_ideas
from threads_ideas_verifier import verify_all_ideas
import config
from sender import send


CATEGORIES = {
    "price_shock": {
        "title": "가격/비용 충격",
        "icon": "💰",
        "color": "#dc2626",
        "bg": "#fef2f2",
    },
    "scams": {
        "title": "사기/바가지/함정",
        "icon": "⚠️",
        "color": "#f59e0b",
        "bg": "#fffbeb",
    },
    "insider": {
        "title": "한국인만 아는 정보",
        "icon": "🤫",
        "color": "#7c3aed",
        "bg": "#faf5ff",
    },
    "regrets": {
        "title": "외국인 후회/실수",
        "icon": "😅",
        "color": "#0891b2",
        "bg": "#ecfeff",
    },
    "deals": {
        "title": "시간 한정 혜택/특별",
        "icon": "🎁",
        "color": "#16a34a",
        "bg": "#f0fdf4",
    },
}

STATUS_CONFIG = {
    "verified": {
        "icon": "✅",
        "label": "검증됨",
        "color": "#16a34a",
        "bg": "#f0fdf4",
    },
    "partial": {
        "icon": "⚠️",
        "label": "부분 검증",
        "color": "#f59e0b",
        "bg": "#fffbeb",
    },
    "unverified": {
        "icon": "❌",
        "label": "검증 실패 (Claude 추측)",
        "color": "#dc2626",
        "bg": "#fef2f2",
    },
}


def render_idea_card(idea, idx):
    """개별 아이디어 카드"""
    verification = idea.get("verification", {})
    status = verification.get("status", "unverified")
    status_cfg = STATUS_CONFIG.get(status, STATUS_CONFIG["unverified"])
    
    reason = verification.get("reason", "")
    evidence = verification.get("supporting_evidence", "")
    search_count = idea.get("search_count", 0)
    
    evidence_html = ""
    if evidence and status == "verified":
        evidence_html = f"""
        <div style="margin-top:8px;padding:8px;background:#dcfce7;border-radius:4px;
                    border-left:3px solid #16a34a;font-size:12px;">
          <b style="color:#15803d;">📌 증거:</b> {evidence}
        </div>
        """
    
    return f"""
    <div style="margin:10px 0;padding:12px;background:#fff;border-radius:6px;
                border-left:4px solid {status_cfg['color']};">
      
      <div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px;">
        <span style="background:{status_cfg['color']};color:#fff;padding:2px 8px;
                     border-radius:10px;font-size:11px;font-weight:600;">
          {status_cfg['icon']} {status_cfg['label']}
        </span>
        <span style="background:#e5e7eb;color:#666;padding:2px 8px;
                     border-radius:10px;font-size:11px;">
          🔍 {search_count}건 검색
        </span>
      </div>
      
      <div style="font-size:14px;color:#1a1a1a;line-height:1.5;margin:6px 0;">
        <b>EN:</b> {idea.get('idea_en','')}
      </div>
      <div style="font-size:13px;color:#444;line-height:1.5;margin:4px 0 6px 0;
                  padding-left:8px;border-left:2px solid #e5e7eb;">
        <b>KR:</b> {idea.get('idea_kr','')}
      </div>
      
      <div style="font-size:11px;color:#888;font-style:italic;margin-top:4px;">
        {reason}
      </div>
      
      {evidence_html}
    </div>
    """


def render_category(key, ideas):
    """카테고리별 카드"""
    cfg = CATEGORIES.get(key, {})
    
    idea_html = ""
    for i, idea in enumerate(ideas, 1):
        idea_html += render_idea_card(idea, i)
    
    return f"""
    <div style="margin:20px 0;padding:16px;background:{cfg['bg']};border-radius:8px;">
      <h3 style="margin:0 0 12px 0;color:{cfg['color']};">
        {cfg['icon']} {cfg['title']}
      </h3>
      {idea_html}
    </div>
    """


def render_email(ideas_data):
    """이메일 HTML 렌더링"""
    today = datetime.now().strftime("%Y-%m-%d (%a)")
    weekday_kr = ["월", "화", "수", "목", "금", "토", "일"][datetime.now().weekday()]
    
    # 검증 통계
    all_ideas = []
    for cat_ideas in ideas_data.values():
        all_ideas.extend(cat_ideas)
    
    verified = len([i for i in all_ideas if i.get("verification", {}).get("status") == "verified"])
    partial = len([i for i in all_ideas if i.get("verification", {}).get("status") == "partial"])
    unverified = len([i for i in all_ideas if i.get("verification", {}).get("status") == "unverified"])
    total = len(all_ideas)
    
    # 5개 카테고리 카드
    sections = []
    category_order = ["price_shock", "scams", "insider", "regrets", "deals"]
    for key in category_order:
        ideas = ideas_data.get(key, [])
        if ideas:
            sections.append(render_category(key, ideas))
    
    sections_html = "\n".join(sections)
    
    html = f"""<!doctype html>
<html><body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
                   max-width:680px;margin:0 auto;padding:16px;color:#222;background:#fff;">

  <h2 style="border-bottom:3px solid #1a1a1a;padding-bottom:12px;">
    💡 오늘의 Threads 콘텐츠 아이디어
  </h2>
  
  <p style="color:#666;font-size:13px;">
    {today} ({weekday_kr}요일) · 총 {total}개 아이디어 (영문 + 한글)<br>
    🕙 콘텐츠 작성 시간: 오후 9:30 메일 또는 직접 작성
  </p>
  
  <div style="background:#f3f4f6;padding:12px;margin:16px 0;border-radius:8px;
              display:flex;gap:10px;justify-content:space-around;text-align:center;">
    <div>
      <div style="font-size:20px;font-weight:bold;color:#16a34a;">✅ {verified}</div>
      <div style="font-size:11px;color:#666;">검증됨</div>
    </div>
    <div>
      <div style="font-size:20px;font-weight:bold;color:#f59e0b;">⚠️ {partial}</div>
      <div style="font-size:11px;color:#666;">부분 검증</div>
    </div>
    <div>
      <div style="font-size:20px;font-weight:bold;color:#dc2626;">❌ {unverified}</div>
      <div style="font-size:11px;color:#666;">검증 실패</div>
    </div>
  </div>
  
  <div style="background:#eff6ff;border-left:4px solid #3b82f6;
              padding:12px;margin:16px 0;border-radius:4px;font-size:13px;">
    <b>💡 사용 방법:</b><br>
    ✅ 검증된 아이디어 우선 사용 (사실 확인 완료)<br>
    ⚠️ 부분 검증은 본인이 추가 확인 후 사용<br>
    ❌ 검증 실패는 참고만 (Claude 추측, 사용 시 주의)
  </div>

  {sections_html}

  <p style="color:#999;font-size:11px;margin-top:32px;text-align:center;">
    Claude AI 자동 생성 + Google News 검증 · 매일 오전 8시 30분 발송
  </p>

</body></html>"""
    
    subject = f"[{datetime.now():%m/%d}] 오늘의 Threads 아이디어 ({verified}/{total} 검증)"
    return subject, html


def main():
    print("🚀 Threads 콘텐츠 아이디어 생성 시작")
    
    # 1. API 키 확인
    if not config.ANTHROPIC_API_KEY:
        print("❌ ANTHROPIC_API_KEY 없음")
        return
    
    # 2. Claude로 10개 아이디어 + 검색 키워드 생성
    print("🤖 Claude로 아이디어 생성 중...")
    client = get_client(config.ANTHROPIC_API_KEY)
    ideas_data = generate_ideas(client)
    
    if not ideas_data:
        print("❌ 아이디어 생성 실패")
        return
    
    total = sum(len(ideas_data.get(key, [])) for key in CATEGORIES.keys())
    print(f"✅ {total}개 아이디어 생성 완료")
    
    # 3. Google News 검색으로 사실 검증
    print("🔍 사실 검증 중 (각 아이디어마다 검색)...")
    ideas_data = verify_all_ideas(config.ANTHROPIC_API_KEY, ideas_data)
    
    # 검증 통계
    all_ideas = []
    for cat_ideas in ideas_data.values():
        all_ideas.extend(cat_ideas)
    verified = len([i for i in all_ideas if i.get("verification", {}).get("status") == "verified"])
    print(f"✅ 검증 완료: {verified}/{total} 검증됨")
    
    # 4. 이메일 렌더링 + 발송
    subject, html = render_email(ideas_data)
    send(subject, html, config)
    print("✅ 발송 완료")


if __name__ == "__main__":
    main()
