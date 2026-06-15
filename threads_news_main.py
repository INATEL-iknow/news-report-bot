"""
Threads 콘텐츠 소재 뉴스 - 메인 실행 파일 (최종 버전)
- 매일 한국시간 08:30 발동
- 진짜 뉴스 수집 → Claude 필터링 → 어그로 아이디어 생성 → 메일
"""

from datetime import datetime

from threads_news_collector import fetch_all_news
from threads_news_filter import filter_news_with_claude, filter_by_category
from threads_news_ideator import generate_ideas_from_news_pool
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


def render_news_card(news, cfg):
    """개별 뉴스 카드 렌더링"""
    evaluation = news.get("evaluation", {})
    idea = news.get("idea", {})
    
    score = evaluation.get("score", 0)
    key_fact = evaluation.get("key_fact", "")
    
    idea_en = idea.get("idea_en", "")
    idea_kr = idea.get("idea_kr", "")
    facts_used = idea.get("facts_used", "")
    
    lang_flag = "🇰🇷" if news.get("lang") == "ko" else "🇺🇸"
    
    return f"""
    <div style="margin:10px 0;padding:14px;background:#fff;border-radius:8px;
                border-left:4px solid {cfg['color']};">
      
      <div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px;">
        <span style="background:{cfg['color']};color:#fff;padding:2px 8px;
                     border-radius:10px;font-size:11px;font-weight:600;">
          ⭐ 점수 {score}/5
        </span>
        <span style="background:#e5e7eb;color:#666;padding:2px 8px;
                     border-radius:10px;font-size:11px;">
          {lang_flag} {news.get('source','')}
        </span>
      </div>
      
      <div style="font-size:12px;color:#555;margin:6px 0;font-weight:600;">
        📰 원본 기사
      </div>
      <div style="font-size:13px;color:#1a1a1a;margin:4px 0 8px 0;">
        <a href="{news.get('link','')}" style="color:#1a1a1a;text-decoration:none;">
          {news.get('title','')}
        </a>
      </div>
      
      <div style="margin:10px 0;padding:10px;background:#fff8dc;border-radius:6px;
                  border-left:3px solid #f59e0b;">
        <div style="font-size:11px;color:#92400e;font-weight:600;margin-bottom:4px;">
          💡 어그로 아이디어 (영문)
        </div>
        <div style="font-size:14px;color:#1a1a1a;line-height:1.5;">
          {idea_en}
        </div>
      </div>
      
      <div style="margin:8px 0;padding:10px;background:#eff6ff;border-radius:6px;
                  border-left:3px solid #3b82f6;">
        <div style="font-size:11px;color:#1e40af;font-weight:600;margin-bottom:4px;">
          🇰🇷 한글 번역
        </div>
        <div style="font-size:14px;color:#1a1a1a;line-height:1.5;">
          {idea_kr}
        </div>
      </div>
      
      <div style="margin-top:8px;padding:8px;background:#f0fdf4;border-radius:4px;
                  font-size:11px;color:#15803d;">
        <b>📌 사용한 사실:</b> {facts_used}
      </div>
    </div>
    """


def render_category(key, news_list):
    """카테고리 카드 렌더링"""
    cfg = CATEGORIES.get(key, {})
    
    if not news_list:
        return f"""
        <div style="margin:20px 0;padding:16px;background:#f9fafb;border-radius:8px;
                    border:1px dashed #d1d5db;">
          <h3 style="margin:0 0 8px 0;color:#9ca3af;">
            {cfg['icon']} {cfg['title']}
          </h3>
          <p style="font-size:13px;color:#9ca3af;margin:0;">
            오늘은 검증된 뉴스가 없어요
          </p>
        </div>
        """
    
    news_html = ""
    for news in news_list:
        news_html += render_news_card(news, cfg)
    
    return f"""
    <div style="margin:20px 0;padding:16px;background:{cfg['bg']};border-radius:8px;">
      <h3 style="margin:0 0 12px 0;color:{cfg['color']};">
        {cfg['icon']} {cfg['title']} ({len(news_list)}건)
      </h3>
      {news_html}
    </div>
    """


def render_email(news_by_category, total_collected, total_filtered):
    """이메일 HTML"""
    today = datetime.now().strftime("%Y-%m-%d (%a)")
    weekday_kr = ["월", "화", "수", "목", "금", "토", "일"][datetime.now().weekday()]
    
    # 5개 카테고리 카드
    sections = []
    category_order = ["price_shock", "scams", "insider", "regrets", "deals"]
    for key in category_order:
        news_list = news_by_category.get(key, [])
        sections.append(render_category(key, news_list))
    
    sections_html = "\n".join(sections)
    
    # 총 카운트
    total_ideas = sum(len(v) for v in news_by_category.values())
    
    html = f"""<!doctype html>
<html><body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
                   max-width:680px;margin:0 auto;padding:16px;color:#222;background:#fff;">

  <h2 style="border-bottom:3px solid #1a1a1a;padding-bottom:12px;">
    💡 오늘의 Threads 콘텐츠 아이디어
  </h2>
  
  <p style="color:#666;font-size:13px;">
    {today} ({weekday_kr}요일) · 진짜 뉴스 기반 검증된 아이디어<br>
    🕙 콘텐츠 작성: 오후 9:30 메일 또는 직접 작성
  </p>
  
  <div style="background:#f3f4f6;padding:12px;margin:16px 0;border-radius:8px;
              display:flex;gap:10px;justify-content:space-around;text-align:center;">
    <div>
      <div style="font-size:20px;font-weight:bold;color:#3b82f6;">{total_collected}</div>
      <div style="font-size:11px;color:#666;">수집된 뉴스</div>
    </div>
    <div>
      <div style="font-size:20px;font-weight:bold;color:#f59e0b;">{total_filtered}</div>
      <div style="font-size:11px;color:#666;">필터 통과 (4+점)</div>
    </div>
    <div>
      <div style="font-size:20px;font-weight:bold;color:#16a34a;">{total_ideas}</div>
      <div style="font-size:11px;color:#666;">검증된 아이디어</div>
    </div>
  </div>
  
  <div style="background:#eff6ff;border-left:4px solid #3b82f6;
              padding:12px;margin:16px 0;border-radius:4px;font-size:13px;">
    <b>💡 사용 방법:</b><br>
    모든 아이디어는 <b>진짜 뉴스 기사 기반</b>입니다.<br>
    1. 원하는 아이디어 선택<br>
    2. 원본 기사 링크 클릭해서 사실 확인<br>
    3. 본인 콘텐츠 공식으로 작성 (어그로 + Open Loop + Pglemaps)
  </div>

  {sections_html}

  <p style="color:#999;font-size:11px;margin-top:32px;text-align:center;">
    Google News + Claude AI · 매일 오전 8시 30분 발송
  </p>

</body></html>"""
    
    subject = f"[{datetime.now():%m/%d}] 오늘의 Threads 아이디어 ({total_ideas}건 검증)"
    return subject, html


def main():
    print("🚀 Threads 콘텐츠 아이디어 시스템 시작")
    
    # 1. 뉴스 수집
    news_items = fetch_all_news()
    total_collected = len(news_items)
    
    if not news_items:
        print("❌ 수집된 뉴스 없음")
        return
    
    # 2. Claude로 필터링 (4점 이상만)
    if not config.ANTHROPIC_API_KEY:
        print("❌ ANTHROPIC_API_KEY 없음")
        return
    
    filtered = filter_news_with_claude(
        config.ANTHROPIC_API_KEY,
        news_items,
        min_score=4,
    )
    total_filtered = len(filtered)
    
    # 3. 카테고리별 그룹화 (각 최대 2건)
    news_by_category = filter_by_category(filtered)
    
    # 4. 검증된 뉴스로 아이디어 생성
    news_by_category = generate_ideas_from_news_pool(
        config.ANTHROPIC_API_KEY,
        news_by_category,
    )
    
    # 5. 메일 발송
    subject, html = render_email(news_by_category, total_collected, total_filtered)
    send(subject, html, config)
    print("✅ 발송 완료")


if __name__ == "__main__":
    main()
