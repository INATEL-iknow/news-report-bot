from datetime import datetime

CAT_ICONS = {
    "마케팅": "📌",
    "스타트업·아이디어": "🚀",
    "경제·사회": "📈",
}

HTML_TMPL = """<!doctype html>
<html><body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
                   max-width:600px;margin:0 auto;padding:16px;color:#222;">
  <h2 style="border-bottom:2px solid #333;padding-bottom:8px;">
    ☕ 오늘의 마케팅·아이디어 브리핑
  </h2>
  <p style="color:#666;font-size:13px;">{date} · 총 {n}건</p>
  {body}
  <p style="color:#999;font-size:11px;margin-top:24px;">
    자동 생성된 리포트 · 출근길 한 줄 정리
  </p>
</body></html>"""

SECTION_TMPL = """<h3 style="margin-top:24px;padding:8px 0;border-bottom:1px solid #ddd;color:#333;">
  {icon} {cat} <span style="color:#999;font-size:13px;font-weight:normal;">({n}건)</span>
</h3>
{items}"""

ITEM_TMPL = """<div style="margin:10px 0;padding:10px;border-left:3px solid #4a90e2;background:#fafafa;">
  <div style="font-size:11px;color:#888;">{source}</div>
  <div style="font-weight:600;font-size:15px;margin:4px 0;">
    <a href="{link}" style="color:#1a1a1a;text-decoration:none;">{title}</a>
  </div>
  <div style="font-size:13px;color:#555;line-height:1.5;">{summary}</div>
</div>"""

def render(items_by_cat):
    total = sum(len(v) for v in items_by_cat.values())
    sections = []
    for cat, items in items_by_cat.items():
        if not items:
            continue
        item_html = "\n".join(ITEM_TMPL.format(**it) for it in items)
        sections.append(SECTION_TMPL.format(
            icon=CAT_ICONS.get(cat, "•"),
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
    subject = f"[{datetime.now():%m/%d}] 오늘의 마케팅·아이디어 브리핑 ({total}건)"
    return subject, html