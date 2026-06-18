"""
이메일 HTML 렌더링 - 7개 카테고리
"""

from datetime import datetime


CATEGORY_CONFIG = {
    "betalist": {
        "title": "BetaList 신규 서비스",
        "icon": "🚀",
        "color": "#3b82f6",
        "bg": "#eff6ff",
        "score_label": "사업 적용도",
        "insight_label": "💡 인사이트",
    },
    "monetize": {
        "title": "수익화 아이디어",
        "icon": "💰",
        "color": "#16a34a",
        "bg": "#f0fdf4",
        "score_label": "수익화 가치",
        "insight_label": "🎯 실행 포인트",
    },
    "inbound_tourism": {
        "title": "방한 외국인 트렌드",
        "icon": "📊",
        "color": "#dc2626",
        "bg": "#fef2f2",
        "score_label": "트렌드 가치",
        "insight_label": "📌 활용 포인트",
    },
    "gov_policy": {
        "title": "정부 정책 / 지원금",
        "icon": "🏛️",
        "color": "#7c3aed",
        "bg": "#faf5ff",
        "score_label": "신청 가능성",
        "insight_label": "💰 활용 방법",
    },
    "tourism_industry": {
        "title": "한국 관광 업계 동향",
        "icon": "🗺️",
        "color": "#0891b2",
        "bg": "#ecfeff",
        "score_label": "경쟁 정보",
        "insight_label": "🎯 대응 전략",
    },
    "affiliate": {
        "title": "어필리에이트 마케팅 사례",
        "icon": "🤝",
        "color": "#f59e0b",
        "bg": "#fffbeb",
        "score_label": "전략 가치",
        "insight_label": "💼 적용 포인트",
    },
    "foreigner_business": {
        "title": "외국인 대상 한국 비즈니스",
        "icon": "📱",
        "color": "#ec4899",
        "bg": "#fdf2f8",
        "score_label": "마케팅 가치",
        "insight_label": "📈 활용 포인트",
    },
}


# 카테고리 표시 순서
CATEGORY_ORDER = [
    "gov_policy",          # 정부 지원금 (가장 액션 가능)
    "inbound_tourism",     # 방한 외국인 트렌드
    "tourism_industry",    # 관광 업계 동향
    "foreigner_business",  # 외국인 비즈니스
    "affiliate",           # 어필리에이트 사례
    "betalist",            # BetaList 신규
    "monetize",            # 수익화 아이디어
]


def render_item_card(item, cfg):
    """단일 항목 카드"""
    analysis = item.get("analysis", {})
    
    title_kr = analysis.get("title_kr", item.get("title", ""))
    summary_kr = analysis.get("summary_kr", "")
    score = analysis.get("score", 0)
    insight = analysis.get("insight_kr", "")
    
    title_en = item.get("title", "")
    link = item.get("link", "")
    source = item.get("source", "")
    
    # 점수 색상
    if score >= 4:
        score_color = "#dc2626"
    elif score == 3:
        score_color = "#f59e0b"
    else:
        score_color = "#9ca3af"
    
    return f"""
    <div style="margin:12px 0;padding:14px;background:#fff;border-radius:8px;
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
    """카테고리 섹션"""
    cfg = CATEGORY_CONFIG.get(key, {})
    
    if not items:
        return f"""
        <div style="margin:20px 0;">
          <h3 style="margin:0 0 8px 0;color:#9ca3af;
                     border-bottom:2px solid #e5e7eb;padding-bottom:6px;">
            {cfg.get('icon','')} {cfg.get('title','')} (0건)
          </h3>
          <p style="color:#9ca3af;font-size:12px;margin:8px 0;font-style:italic;">
            오늘은 수집된 항목이 없어요.
          </p>
        </div>
        """
    
    cards_html = ""
    for item in items:
        cards_html += render_item_card(item, cfg)
    
    return f"""
    <div style="margin:24px 0;">
      <h3 style="margin:0 0 12px 0;color:{cfg['color']};
                 border-bottom:2px solid {cfg['color']};padding-bottom:6px;">
        {cfg['icon']} {cfg['title']} ({len(items)}건)
      </h3>
      {cards_html}
    </div>
    """


def render_email(grouped_items):
    """이메일 HTML 전체"""
    today = datetime.now().strftime("%Y-%m-%d (%a)")
    weekday_kr = ["월", "화", "수", "목", "금", "토", "일"][datetime.now().weekday()]
    
    # 총 건수
    total = sum(len(items) for items in grouped_items.values())
    
    # 카테고리별 통계
    stats_html = ""
    for key in CATEGORY_ORDER:
        items = grouped_items.get(key, [])
        cfg = CATEGORY_CONFIG.get(key, {})
        count = len(items)
        color = cfg.get("color", "#999") if count > 0 else "#d1d5db"
        stats_html += f"""
        <div style="background:#fff;padding:8px;border-radius:6px;text-align:center;
                    flex:1;min-width:90px;border:1px solid #e5e7eb;">
          <div style="font-size:18px;font-weight:bold;color:{color};">{count}</div>
          <div style="font-size:10px;color:#666;margin-top:2px;">
            {cfg.get('icon','')} {cfg.get('title','').split(' ')[0]}
          </div>
        </div>
        """
    
    # 카테고리별 섹션
    sections = []
    for key in CATEGORY_ORDER:
        items = grouped_items.get(key, [])
        sections.append(render_category(key, items))
    
    sections_html = "\n".join(sections)
    
    html = f"""<!doctype html>
<html><body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
                   max-width:720px;margin:0 auto;padding:16px;color:#222;background:#f9fafb;">

  <div style="background:#fff;padding:24px;border-radius:12px;">
    
    <h2 style="margin:0 0 8px 0;border-bottom:2px solid #1a1a1a;padding-bottom:10px;">
      📰 오늘의 인사이트 브리핑
    </h2>
    
    <p style="color:#666;font-size:13px;margin:8px 0;">
      {today} ({weekday_kr}요일) · 총 {total}건<br>
      7개 카테고리 × 각 최대 3건
    </p>
    
    <!-- 카테고리별 통계 -->
    <div style="display:flex;gap:8px;flex-wrap:wrap;margin:16px 0;
                background:#f3f4f6;padding:12px;border-radius:8px;">
      {stats_html}
    </div>
    
    <div style="background:#eff6ff;border-left:4px solid #3b82f6;
                padding:12px;margin:16px 0;border-radius:4px;font-size:13px;">
      <b>📌 읽는 방법:</b><br>
      <b>점수 4-5점</b>만 집중. 빨간색 점수가 진짜 가치 있는 정보.<br>
      카테고리 순서: 정부 지원금 → 트렌드 → 업계 → 비즈니스 → 어필리에이트 → BetaList → 수익화
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
