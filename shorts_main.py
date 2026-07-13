"""
유튜브 쇼츠 후킹 자동화 - 메인 실행
- 매일 07:40 KST
- 국내 8 + 해외 2 = 총 10개 이슈
- 각 이슈마다 후킹 3개 옵션
"""

from datetime import datetime

import shorts_topics
import shorts_generator
import config
from sender import send


# 카테고리별 색상
CATEGORY_COLORS = {
    "domestic": {
        "color": "#dc2626",
        "bg": "#fef2f2",
        "label": "국내",
        "icon": "🇰🇷",
    },
    "global": {
        "color": "#3b82f6",
        "bg": "#eff6ff",
        "label": "해외",
        "icon": "🌎",
    },
}


SUBCATEGORY_KR = {
    "breakup": "연애/결별",
    "wedding": "결혼",
    "scandal": "스캔들",
    "comeback": "컴백/신곡",
    "collab": "협업",
    "controversy": "논란",
    "other": "이슈",
}


def render_issue_card(result, idx):
    """단일 이슈 카드 (후킹 3개 옵션 표시)"""
    evaluation = result.get("evaluation", {})
    category = evaluation.get("category", "domestic")
    subcategory = evaluation.get("subcategory", "other")
    subcategory_kr = SUBCATEGORY_KR.get(subcategory, "이슈")
    virality = evaluation.get("virality_score", 0)
    subjects = ", ".join(evaluation.get("key_subjects", []))
    
    cat_cfg = CATEGORY_COLORS.get(category, CATEGORY_COLORS["domestic"])
    
    hooks = result.get("hooks", [])
    summary_lines = result.get("summary_kr", [])
    
    original_link = result.get("original_link", "")
    original_source = result.get("original_source", "")
    original_title = result.get("original_title", "")
    
    # 화제성 별
    stars = "⭐" * min(int((virality + 1) / 2), 5)
    
    # 후킹 옵션 3개 HTML
    hooks_html = ""
    for i, hook in enumerate(hooks, 1):
        hooks_html += f"""
        <div style="margin:6px 0;padding:12px;background:#fff8dc;border-radius:6px;
                    border-left:4px solid #f59e0b;">
          <div style="font-size:10px;color:#666;font-weight:600;margin-bottom:4px;">
            후킹 옵션 {i}
          </div>
          <div style="font-size:15px;line-height:1.5;font-weight:600;">
            {hook}
          </div>
        </div>
        """
    
    # 요약 HTML
    summary_html = "".join(
        f'<li style="margin:2px 0;">{line}</li>' for line in summary_lines
    )
    
    return f"""
    <div style="margin:16px 0;padding:0;border:1px solid #e5e7eb;border-radius:10px;
                overflow:hidden;background:#fff;">
      
      <!-- 헤더 -->
      <div style="background:{cat_cfg['bg']};padding:10px 14px;
                  border-bottom:1px solid #e5e7eb;">
        <div style="display:flex;gap:6px;flex-wrap:wrap;align-items:center;">
          <span style="background:{cat_cfg['color']};color:#fff;padding:2px 8px;
                       border-radius:10px;font-size:10px;font-weight:600;">
            #{idx} {cat_cfg['icon']} {cat_cfg['label']} · {subcategory_kr}
          </span>
          <span style="background:#1a1a1a;color:#fff;padding:2px 8px;
                       border-radius:10px;font-size:10px;font-weight:600;">
            {stars} {virality}/10
          </span>
        </div>
        <div style="font-size:12px;color:#444;margin-top:4px;">
          <b>핵심 인물:</b> {subjects}
        </div>
      </div>
      
      <!-- 후킹 3개 옵션 -->
      <div style="padding:12px 14px;">
        <div style="font-size:11px;color:#666;font-weight:600;margin-bottom:6px;">
          🎣 후킹 옵션 (마음에 드는 것 선택)
        </div>
        {hooks_html}
      </div>
      
      <!-- 요약 -->
      <div style="padding:10px 14px;border-top:1px solid #f3f4f6;background:#fafafa;">
        <div style="font-size:11px;color:#666;font-weight:600;margin-bottom:4px;">
          📰 요약
        </div>
        <ul style="margin:4px 0;padding-left:18px;font-size:12px;line-height:1.5;color:#333;">
          {summary_html}
        </ul>
      </div>
      
      <!-- 원문 링크 -->
      <div style="padding:10px 14px;background:#f3f4f6;">
        <a href="{original_link}" style="color:#3b82f6;text-decoration:none;font-size:11px;">
          🔗 원문 기사 보기 ({original_source})
        </a>
      </div>
    </div>
    """


def render_email(results):
    """이메일 HTML 렌더링"""
    today = datetime.now().strftime("%Y-%m-%d (%a)")
    weekday_kr = ["월", "화", "수", "목", "금", "토", "일"][datetime.now().weekday()]
    
    # 카테고리 통계
    domestic_count = sum(
        1 for r in results 
        if r.get("evaluation", {}).get("category") == "domestic"
    )
    global_count = sum(
        1 for r in results 
        if r.get("evaluation", {}).get("category") == "global"
    )
    
    total_hooks = sum(len(r.get("hooks", [])) for r in results)
    
    cards_html = ""
    for i, result in enumerate(results, 1):
        cards_html += render_issue_card(result, i)
    
    html = f"""<!doctype html>
<html><body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
                   max-width:720px;margin:0 auto;padding:12px;color:#222;background:#f9fafb;">

  <div style="background:#fff;padding:20px;border-radius:12px;">
    
    <h2 style="margin:0 0 8px 0;border-bottom:2px solid #1a1a1a;padding-bottom:10px;">
      🎬 오늘의 쇼츠 후킹 {len(results)}개 이슈
    </h2>
    
    <p style="color:#666;font-size:13px;margin:8px 0;">
      {today} ({weekday_kr}요일)<br>
      국내 {domestic_count}건 + 해외 {global_count}건 = 총 {len(results)}개 이슈<br>
      각 이슈마다 후킹 3개 옵션 = 총 {total_hooks}개 후킹
    </p>
    
    <div style="background:#eff6ff;border-left:4px solid #3b82f6;
                padding:10px;margin:14px 0;border-radius:4px;font-size:12px;">
      <b>📌 사용 방법:</b><br>
      1. 10개 이슈 중 촬영할 것 골라내기<br>
      2. 각 이슈의 후킹 3개 중 마음에 드는 것 선택<br>
      3. 원문 기사 링크로 팩트 확인<br>
      4. 본인 스타일로 촬영/편집
    </div>

    {cards_html}

    <p style="color:#999;font-size:10px;margin-top:24px;text-align:center;
              border-top:1px solid #e5e7eb;padding-top:12px;">
      Claude Haiku 자동 생성 · 매일 오전 7:40 발송
    </p>
  </div>

</body></html>"""
    
    subject = f"[{datetime.now():%m/%d}] 오늘의 쇼츠 후킹 {len(results)}개 이슈"
    return subject, html


def main():
    print("🎬 유튜브 쇼츠 후킹 자동화 시작")
    
    if not config.ANTHROPIC_API_KEY:
        print("❌ ANTHROPIC_API_KEY 없음")
        return
    
    # 1. 연예 뉴스 수집
    print("\n[1단계] 뉴스 수집")
    items = shorts_topics.fetch_all()
    
    if not items:
        print("❌ 수집된 뉴스 없음")
        return
    
    # 2. Claude로 평가 + 선정 + 후킹 생성
    print("\n[2단계] 화제성 평가 + 후킹 생성")
    results = shorts_generator.generate_all_hooks(
        config.ANTHROPIC_API_KEY, items
    )
    
    if not results:
        print("❌ 후킹 생성 실패")
        return
    
    # 3. 이메일 발송
    print("\n[3단계] 메일 발송")
    subject, html = render_email(results)
    send(subject, html, config)
    
    print(f"\n✅ 완료: {len(results)}개 이슈 후킹 발송")


if __name__ == "__main__":
    main()
