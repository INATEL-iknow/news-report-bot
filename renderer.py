from datetime import datetime

CAT_CONFIG = {
    "오늘의출시도구": {"icon": "🛠", "color": "#16a085"},
    "사이드프로젝트": {"icon": "💭", "color": "#8e44ad"},
    "외국인마케팅성공사례": {"icon": "🌏", "color": "#9b59b6"},
    "방한외국인": {"icon": "🇰🇷", "color": "#e94e77"},
    "정부지원금": {"icon": "💰", "color": "#27ae60"},
    "Reddit인사이트": {"icon": "🗣️", "color": "#ff4500"},
}

CAT_DISPLAY = {
    "오늘의출시도구": "오늘의 출시 도구 (영감)",
    "사이드프로젝트": "사이드 프로젝트 사례",
    "외국인마케팅성공사례": "외국인 마케팅 성공사례",
    "방한외국인": "방한 외국인 트렌드",
    "정부지원금": "관광·창업 지원금",
    "Reddit인사이트": "Reddit - 외국인의 진짜 목소리",
}

LEVEL_BADGES = {
    "Core": ('🎯', '#4a90e2', 'Core (즉시)'),
    "Adjacent": ('🔄', '#f0ad4e', 'Adjacent (1-3개월)'),
    "Transformative": ('🚀', '#d9534f', 'Transformative (6개월+)'),
}

PRIORITY_COLORS = {
    "높음": "#d9534f",
    "매우높음": "#c0392b",
    "중간": "#f0ad4e",
    "낮음": "#999",
    "보통": "#999",
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
    Claude AI 인사이트 · 매일 오전 9시 자동 발송
  </p>
</body></html>"""

SECTION_TMPL = """<h3 style="margin-top:28px;padding:8px 0;border-bottom:2px solid {color};color:#333;">
  {icon} {cat} <span style="color:#999;font-size:13px;font-weight:normal;">({n}건)</span>
</h3>
{items}"""

def _priority_badge(priority):
    color = PRIORITY_COLORS.get(priority, "#999")
    return f'<span style="display:inline-block;padding:2px 8px;background:{color};color:#fff;font-size:11px;border-radius:10px;font-weight:600;">우선순위 {priority}</span>'

def _level_badge(level):
    icon, color, label = LEVEL_BADGES.get(level, ('•', '#999', level or ''))
    return f'<span style="display:inline-block;padding:2px 8px;background:{color};color:#fff;font-size:11px;border-radius:10px;font-weight:600;">{icon} {label}</span>'

def _insight_tool(insight):
    if not insight: return ""
    return f"""<div style="margin-top:8px;padding:12px;background:#e8f8f5;border-radius:6px;font-size:13px;border-left:3px solid #16a085;">
  <div><b>🔧 이 도구는:</b> {insight.get('what_it_does','')}</div>
  <div style="margin-top:6px;padding:8px;background:#fff;border-radius:4px;">
    <b>💡 한국 버전 아이디어:</b> {insight.get('korean_market_idea','')}
  </div>
  <div style="margin-top:6px;"><b>🎯 타겟:</b> {insight.get('target_user','')}</div>
  <div style="margin-top:4px;"><b>💰 수익화:</b> {insight.get('monetization','')}</div>
  <div style="margin-top:4px;"><b>📊 예상 월 수익:</b> <b style="color:#27ae60;">{insight.get('revenue_estimate','')}</b></div>
  <div style="margin-top:4px;color:#666;font-size:12px;">🛠 {insight.get('key_tech','')} · ⏱ {insight.get('build_time','')}</div>
  <div style="margin-top:8px;padding:8px;background:#fff8dc;border-radius:4px;">
    <b>✅ 내일 첫 액션:</b> {insight.get('first_step','')}
  </div>
</div>"""

def _insight_sideproject(insight):
    if not insight: return ""
    return f"""<div style="margin-top:8px;padding:12px;background:#f5eef8;border-radius:6px;font-size:13px;border-left:3px solid #8e44ad;">
  <div><b>📦 그들이 만든 것:</b> {insight.get('what_they_built','')}</div>
  <div style="margin-top:6px;"><b>💎 배울 점:</b> {insight.get('their_insight','')}</div>
  <div style="margin-top:6px;padding:8px;background:#fff;border-radius:4px;">
    <b>💡 본인 버전 아이디어:</b> {insight.get('my_version_idea','')}
  </div>
  <div style="margin-top:4px;"><b>🎯 타겟:</b> {insight.get('target_user','')}</div>
  <div style="margin-top:4px;"><b>💰 수익화:</b> {insight.get('monetization','')}</div>
  <div style="margin-top:4px;"><b>📊 예상 월 수익:</b> <b style="color:#27ae60;">{insight.get('revenue_estimate','')}</b></div>
  <div style="margin-top:4px;color:#666;font-size:12px;">난이도 {insight.get('execution_difficulty','')}</div>
  <div style="margin-top:8px;padding:8px;background:#fff8dc;border-radius:4px;">
    <b>✅ 내일 첫 액션:</b> {insight.get('first_step','')}
  </div>
</div>"""

def _insight_marketing(insight):
    if not insight: return ""
    metric = insight.get('key_metric', '')
    metric_html = f'<div style="margin-top:4px;"><b>📈 성과:</b> {metric}</div>' if metric and metric not in ("없음", "정보 없음") else ""
    return f"""<div style="margin-top:8px;padding:10px;background:#faf5ff;border-radius:6px;font-size:13px;">
  {_priority_badge(insight.get('priority','중간'))}
  <div style="margin-top:8px;"><b>✨ 성공 요인:</b> {insight.get('success_factor','')}</div>
  {metric_html}
  <div style="margin-top:4px;"><b>🎯 피글맵스 적용:</b> {insight.get('piglemaps_application','')}</div>
  <div style="margin-top:4px;color:#666;font-size:12px;">⏱ {insight.get('execution_difficulty','')}</div>
</div>"""

def _insight_inbound(insight):
    if not insight: return ""
    return f"""<div style="margin-top:8px;padding:10px;background:#fff0f5;border-radius:6px;font-size:13px;">
  {_level_badge(insight.get('innovation_level'))}
  <div style="margin-top:8px;"><b>🔗 연결:</b> {insight.get('connection','')}</div>
  <div style="margin-top:4px;"><b>🛍 상품 아이디어:</b> {insight.get('product_idea','')}</div>
  <div style="margin-top:4px;color:#666;font-size:12px;">💰 {insight.get('revenue_model','')} · 우선순위 {insight.get('priority','')}</div>
</div>"""

def _insight_grant(insight):
    if not insight: return ""
    fit = insight.get('fit_for_piglemaps', '보통')
    fit_color = PRIORITY_COLORS.get(fit, "#999")
    fit_badge = f'<span style="display:inline-block;padding:2px 8px;background:{fit_color};color:#fff;font-size:11px;border-radius:10px;font-weight:600;">피글맵스 적합도 {fit}</span>'
    
    deadline = insight.get('deadline', '')
    deadline_html = f'<div style="margin-top:4px;"><b>⏰ 일정:</b> <b style="color:#d9534f;">{deadline}</b></div>' if deadline and deadline not in ("없음", "정보 없음") else ""
    
    return f"""<div style="margin-top:8px;padding:10px;background:#f0fff4;border-radius:6px;font-size:13px;">
  {fit_badge}
  <div style="margin-top:8px;"><b>📋 사업명:</b> {insight.get('program_name','')}</div>
  <div style="margin-top:4px;"><b>🎯 대상:</b> {insight.get('target','')}</div>
  <div style="margin-top:4px;"><b>💵 지원 규모:</b> {insight.get('support_amount','')}</div>
  {deadline_html}
  <div style="margin-top:6px;padding:6px;background:#fff;border-radius:4px;"><b>✅ 액션:</b> {insight.get('action','')}</div>
</div>"""

def _insight_reddit(insight):
    if not insight: return ""
    return f"""<div style="margin-top:8px;padding:12px;background:#fff5f0;border-radius:6px;font-size:13px;border-left:3px solid #ff4500;">
  {_priority_badge(insight.get('priority','중간'))}
  <div style="margin-top:8px;padding:8px;background:#fff;border-radius:4px;">
    <div><b>🇰🇷 제목 (한국어):</b> {insight.get('title_kr','')}</div>
    <div style="margin-top:4px;color:#555;"><b>📝 요약:</b> {insight.get('summary_kr','')}</div>
  </div>
  <div style="margin-top:8px;"><b>💭 진짜 원하는 것:</b> {insight.get('user_intent','')}</div>
  <div style="margin-top:6px;padding:8px;background:#fff8dc;border-radius:4px;">
    <b>🎯 피글맵스 기회:</b> {insight.get('piglemaps_opportunity','')}
  </div>
  <div style="margin-top:6px;padding:6px;background:#e8f4f8;border-radius:4px;">
    <b>📢 콘텐츠 아이디어:</b> {insight.get('content_idea','')}
  </div>
</div>"""

def _reddit_meta(item):
    """Reddit 글에 대한 추가 메타 정보"""
    score = item.get('score', 0)
    comments = item.get('num_comments', 0)
    subcat = item.get('subcategory', '')
    subcat_badge = ""
    if subcat == "인기":
        subcat_badge = '<span style="background:#ff4500;color:#fff;padding:1px 6px;border-radius:8px;font-size:10px;font-weight:600;">🔥 인기</span> '
    elif subcat == "질문":
        subcat_badge = '<span style="background:#0079d3;color:#fff;padding:1px 6px;border-radius:8px;font-size:10px;font-weight:600;">❓ 질문</span> '
    return f'<div style="font-size:11px;color:#888;">{subcat_badge}⬆️ {score} · 💬 {comments} · {item.get("source","")}</div>'

INSIGHT_RENDERERS = {
    "오늘의출시도구": _insight_tool,
    "사이드프로젝트": _insight_sideproject,
    "외국인마케팅성공사례": _insight_marketing,
    "방한외국인": _insight_inbound,
    "정부지원금": _insight_grant,
    "Reddit인사이트": _insight_reddit,
}

def _item(item, cat):
    color = CAT_CONFIG.get(cat, {}).get("color", "#4a90e2")
    insight_html = INSIGHT_RENDERERS.get(cat, lambda x: "")(item.get("insight"))
    
    # Reddit은 메타 정보 다르게 표시
    if cat == "Reddit인사이트":
        meta_html = _reddit_meta(item)
    else:
        meta_html = f'<div style="font-size:11px;color:#888;">{item.get("source","")}</div>'
    
    return f"""<div style="margin:14px 0;padding:12px;border-left:3px solid {color};background:#fafafa;border-radius:4px;">
  {meta_html}
  <div style="font-weight:600;font-size:15px;margin:4px 0;">
    <a href="{item.get('link','')}" style="color:#1a1a1a;text-decoration:none;">{item.get('title','')}</a>
  </div>
  <div style="font-size:13px;color:#555;line-height:1.5;">{item.get('summary','')[:200]}</div>
  {insight_html}
</div>"""

def render(items_by_cat):
    total = sum(len(v) for v in items_by_cat.values())
    sections = []
    for cat, items in items_by_cat.items():
        if not items: continue
        cfg = CAT_CONFIG.get(cat, {})
        display = CAT_DISPLAY.get(cat, cat)
        item_html = "\n".join(_item(it, cat) for it in items)
        sections.append(SECTION_TMPL.format(
            icon=cfg.get("icon", "•"),
            color=cfg.get("color", "#333"),
            cat=display,
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
