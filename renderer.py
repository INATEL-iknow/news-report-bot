from datetime import datetime

CAT_CONFIG = {
    "창업·아이디어": {"icon": "💡", "color": "#4a90e2"},
    "방한외국인": {"icon": "🇰🇷", "color": "#e94e77"},
    "사회·경제": {"icon": "📊", "color": "#5cb85c"},
}

LEVEL_BADGES = {
    "Core": ('🎯', '#4a90e2', 'Core (즉시)'),
    "Adjacent": ('🔄', '#f0ad4e', 'Adjacent (1-3개월)'),
    "Transformative": ('🚀', '#d9534f', 'Transformative (6개월+)'),
}

HTML_TMPL = """<!doctype html>
<html><body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
                   max-width:640px;margin:0 auto;padding:16px;color:#222;background:#fff;">
  <h2 style="border-bottom:2px solid #333;padding-bottom:8px;">
    ☕ 오늘의 사업 인사이트 브리핑
  </h2>
  <p style="color:#666;font-size:13px;">{date} · 총 {n}건 · AI 분석 포함</p>
  {body}
  <p style="color:#999;font-size:11px;margin-top:24px;text-align:center;">
    Claude AI 인사이트 · 출근길 한 줄 정리<br>
    💡 Core 70% / 🔄 Adjacent 20% / 🚀 Transformative 10%
  </p>
</body></html>"""

SECTION_TMPL = """<h3 style="margin-top:28px;padding:8px 0;border-bottom:2px solid {color};color:#333;">
  {icon} {cat} <span style="color:#999;font-size:13px;font-weight:normal;">({n}건)</span>
</h3>
{items}"""

def _badge(level):
    icon, color, label = LEVEL_BADGES.get(level, ('•', '#999', level or ''))
    return f'<span style="display:inline-block;padding:2px 8px;background:{color};color:#fff;font-size:11px;border-radius:10px;font-weight:600;">{icon} {label}</span>'

def _insight_block_startup(insight):
    if not insight: return ""
    return f"""<div style="margin-top:8px;padding:10px;background:#f0f7ff;border-radius:6px;font-size:13px;">
  {_badge(insight.get('innovation_level'))}
  <div style="margin-top:8px;"><b>💡 아이디어:</b> {insight.get('idea','')}</div>
  <div style="margin-top:4px;"><b>💰 수익화:</b> {insight.get('monetization','')}</div>
  <div style="margin-top:4px;color:#666;font-size:12px;">🛠 {insight.get('key_tech','')} · 난이도 {insight.get('build_difficulty','')}</div>
</div>"""

def _insight_block_inbound(insight):
    if not insight: return ""
    return f"""<div style="margin-top:8px;padding:10px;background:#fff0f5;border-radius:6px;font-size:13px;">
  {_badge(insight.get('innovation_level'))}
  <div style="margin-top:8px;"><b>🔗 연결:</b> {insight.get('connection','')}</div>
  <div style="margin-top:4px;"><b>🛍 상품 아이디어:</b> {insight.get('product_idea','')}</div>
  <div style="margin-top:4px;color:#666;font-size:12px;">💰 {insight.get('revenue_model','')} · 우선순위 {insight.get('priority','')}</div>
</div>"""

def _insight_block_economy(insight):
    if not insight: return ""
    tag = insight.get('category_tag','')
    return f"""<div style="margin-top:8px;padding:10px;background:#f0fff4;border-radius:6px;font-size:13px;">
  <span style="display:inline-block;padding:2px 8px;background:#5cb85c;color:#fff;font-size:11px;border-radius:10px;font-weight:600;">📊 {tag}</span>
  <div style="margin-top:8px;"><b>📝 요약:</b> {insight.get('summary','')}</div>
  <div style="margin-top:4px;"><b>🎯 활용:</b> {insight.get('actionable','')}</div>
</div>"""

INSIGHT_RENDERERS = {
    "창업·아이디어": _insight_block_startup,
    "방한외국인": _insight_block_inbound,
    "사회·경제": _insight_block_economy,
}

def _item(item, cat):
    color = CAT_CONFIG.get(cat, {}).get("color", "#4a90e2")
    insight_html = INSIGHT_RENDERERS.get(cat, lambda x: "")(item.get("insight"))
    return f"""<div style="margin:14px 0;padding:12px;border-left:3px solid {color};background:#fafafa;border-radius:4px;">
  <div style="font-size:11px;color:#888;">{item.get('source','')}</div>
  <div style="font-weight:600;font-size:15px;margin:4px 0;">
    <a href="{item.get('link','')}" style="color:#1a1a1a;text-decoration:none;">{item.get('title','')}</a>
  </div>
  <div style="font-size:13px;color:#555;line-height:1.5;">{item.get('summary','')}</div>
  {insight_html}
</div>"""

def render(items_by_cat):
    total = sum(len(v) for v in items_by_cat.values())
    sections = []
    for cat, items in items_by_cat.items():
        if not items: continue
        cfg = CAT_CONFIG.get(cat, {})
        item_html = "\n".join(_item(it, cat) for it in items)
        sections.append(SECTION_TMPL.format(
            icon=cfg.get("icon", "•"),
            color=cfg.get("color", "#333"),
            cat=cat,
            n=len(items),
            items=item_html,
        ))
    body = "\n".join(sections)
    html = HTML_TMPL.format(
        date=datetime.now().strftime("%Y-%m-%d (%a)"),
        n=total,
        body=body,
    )
    subject = f"[{datetime.now():%m/%d}] 오늘의 사업 인사이트 ({total}건)"
    return subject, html
