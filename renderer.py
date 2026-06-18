"""
이메일 HTML 렌더링
"""

from datetime import datetime


CATEGORY_CONFIG = {
    "betalist": {
        "title": "BetaList 신규 서비스",
        "icon": "🚀",
        "color": "#3b82f6",
        "bg": "#eff6ff",
        "score_key": "relevance_score",
        "score_label": "사업 적용도",
        "insight_key": "insight_kr",
        "insight_label": "💡 인사이트",
    },
    "monetize": {
        "title": "수익화 아이디어",
        "icon": "💰",
        "color": "#16a34a",
        "bg": "#f0fdf4",
        "score_key": "monetization_score",
        "score_label": "수익화 가치",
        "insight_key": "actionable_kr",
        "insight_label": "🎯 실행 포인트",
    },
}


def render_item_card(item, cfg):
    """단일 항목 카드 렌더링"""
    analysis = item.get("analysis", {})
    
    title_kr = analysis.get("title_kr", item.get("title", ""))
    summary_kr = analysis.get("summary_kr", "")
    score = analysis.get(cfg["score_key"], 0)
    insight = analysis.get(cfg["insight_key"], "")
    
    title_en = item.get("title", "")
    link = item.get("link", "")
    source = item.get("source", "")
    
    # 점수 색상
    if score >= 4:
        score_color = "#dc2626"  # 빨강
    elif score == 3:
        score_color = "#f59e0b"  # 주황
    else:
        score_color = "#9ca3af"  # 회색
    
    return f"""
    <div style="margin:14px 0;padding:14px;background:#fff;border-radius:8px;
                border-left:4px solid {cfg['color']};box-shadow:0 1px 3px rgba(0,0,0,0.08);">
      
      <div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px;">
        <span style="background:{score_color};color:#fff;padding:2px 10px;
                     border-radius:12px;font-size:11px;font-weight:600;">
          {cfg['score_label']} {score}/5
        </span>
        <span style="background:#e5e7eb;color:#555;padding:2px 10px;
                     border-radius:12px;font-size:11px;">
          {source}
        </span>
      </div>
      
      <div style="font-size:15px;font-weight:600;color:#1a1a1a;margin:4px 0;">
        <a href="{link}" style="color:#1a1a1a;text-decoration:none;">
          {title_kr}
        </a>
      </div>
      <div style="font-size:11px;color:#888;font-style:italic;margin-bottom:8px;">
        {title_en}
      </div>
      
      <div style="font-size:13px;color:#444;line-height:1.5;margin:8px 0;">
        {summary_kr}
      </div>
      
      <div style="margin-top:10px;padding:10px;background:{cfg['bg']};border-radius:6px;
                  font-size:12px;color:#1a1a1a;">
        <b>{cfg['insight_label']}:</b> {insight}
      </div>
    </div>
    """


def render_category(key, items):
    """카테고리 섹션 렌더링"""
    cfg = CATEGORY_CONFIG.get(key, {})
    
    if not items:
        return f"""
        <h3 style="margin:24px 0 12px 0;color:{cfg.get('color','#333')};">
          {cfg.get('icon','')} {cfg.get('title','')} (0건)
        </h3>
        <p style="color:#9ca3af;font-size:13px;">오늘은 수집된 항목이 없어요.</p>
        """
    
    cards_html = ""
    for item in items:
        cards_html += render_item_card(item, cfg)
    
    return f"""
    <h3 style="margin:24px 0 12px 0;color:{cfg['color']};
               border-bottom:2px solid {cfg['color']};padding-bottom:6px;">
      {cfg['icon']} {cfg['title']} ({len(items)}건)
    </h3>
    {cards_html}
    """


def render_email(grouped_items):
    """이메일 HTML 전체 렌더링"""
    today = datetime.now().strftime("%Y-%m-%d (%a)")
    weekday_kr = ["월", "화", "수", "목", "금", "토", "일"][datetime.now().weekday()]
    
    # 총 개수
    total = sum(len(items) for items in grouped_items.values())
    
    # 카테고리별 섹션
    sections = []
    for key in ["betalist", "monetize"]:
        items = grouped_items.get(key, [])
        sections.append(render_category(key, items))
    
    sections_html = "\n".join(sections)
    
    html = f"""<!doctype html>
<html><body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
                   max-width:680px;margin:0 auto;padding:16px;color:#222;background:#f9fafb;">

  <div style="background:#fff;padding:20px;border-radius:12px;">
    
    <h2 style="margin:0 0 8px 0;border-bottom:2px solid #1a1a1a;padding-bottom:10px;">
      📰 오늘의 인사이트 브리핑
    </h2>
    
    <p style="color:#666;font-size:13px;margin:8px 0;">
      {today} ({weekday_kr}요일) · 총 {total}건<br>
      신규 서비스 발견 + 수익화 아이디어
    </p>
    
    <div style="background:#eff6ff;border-left:4px solid #3b82f6;
                padding:12px;margin:16px 0;border-radius:4px;font-size:13px;">
      <b>📌 사용 방법:</b><br>
      점수 4-5점 항목만 빠르게 훑어보기.<br>
      🚀 BetaList = 본인 사업 영감 / 트렌드<br>
      💰 수익화 = 본인이 따라할 만한 사이드 프로젝트
    </div>

    {sections_html}

    <p style="color:#999;font-size:11px;margin-top:32px;text-align:center;
              border-top:1px solid #e5e7eb;padding-top:16px;">
      Claude AI 자동 분석 · 매일 오전 9시 발송
    </p>
  </div>

</body></html>"""
    
    subject = f"[{datetime.now():%m/%d}] 오늘의 인사이트 ({total}건)"
    return subject, html
