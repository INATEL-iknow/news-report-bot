"""
Threads 콘텐츠 아이디어 일일 발송 메인 실행 파일
- 매일 한국시간 08:30 발동
- Claude가 5개 카테고리 × 각 2개 = 10개 새 주제 생성
- 본인 이메일로 발송
"""

from datetime import datetime

from threads_ideas_generator import get_client, generate_ideas
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


def render_category(key, ideas):
    """카테고리별 카드 HTML"""
    cfg = CATEGORIES.get(key, {})
    
    idea_html = ""
    for i, idea in enumerate(ideas, 1):
        idea_html += f"""
        <div style="margin:10px 0;padding:12px;background:#fff;border-radius:6px;
                    border-left:3px solid {cfg['color']};">
          <div style="font-size:12px;color:{cfg['color']};font-weight:600;margin-bottom:4px;">
            아이디어 {i}
          </div>
          <div style="font-size:14px;color:#1a1a1a;line-height:1.5;">
            {idea}
          </div>
        </div>
        """
    
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
    
    # 5개 카테고리 카드 생성
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
    {today} ({weekday_kr}요일) · 5개 카테고리 × 각 2개 = 총 10개 아이디어<br>
    🕙 콘텐츠 작성 시간: 오후 9:30 메일 또는 직접 작성
  </p>
  
  <div style="background:#eff6ff;border-left:4px solid #3b82f6;
              padding:12px;margin:16px 0;border-radius:4px;font-size:13px;">
    <b>💡 사용 방법:</b><br>
    1. 10개 중 가장 끌리는 아이디어 1개 선택<br>
    2. 오후 9:30 자동 콘텐츠 메일로 받거나, 직접 작성<br>
    3. 오후 10시 Threads 업로드
  </div>

  {sections_html}

  <p style="color:#999;font-size:11px;margin-top:32px;text-align:center;">
    Claude AI 자동 생성 · 매일 오전 8시 30분 발송
  </p>

</body></html>"""
    
    subject = f"[{datetime.now():%m/%d}] 오늘의 Threads 아이디어 10개"
    return subject, html


def main():
    print("🚀 Threads 콘텐츠 아이디어 생성 시작")
    
    # 1. API 키 확인
    if not config.ANTHROPIC_API_KEY:
        print("❌ ANTHROPIC_API_KEY 없음")
        return
    
    # 2. Claude로 10개 아이디어 생성
    print("🤖 Claude가 10개 아이디어 생성 중...")
    client = get_client(config.ANTHROPIC_API_KEY)
    ideas_data = generate_ideas(client)
    
    if not ideas_data:
        print("❌ 아이디어 생성 실패")
        return
    
    # 총 개수 확인
    total = sum(len(ideas_data.get(key, [])) for key in CATEGORIES.keys())
    print(f"✅ {total}개 아이디어 생성 완료")
    
    # 3. 이메일 렌더링 + 발송
    subject, html = render_email(ideas_data)
    send(subject, html, config)
    print("✅ 발송 완료")


if __name__ == "__main__":
    main()
