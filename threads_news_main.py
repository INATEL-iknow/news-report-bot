"""
Threads 콘텐츠 소재 뉴스 일일 발송 메인 실행 파일
- 매일 한국시간 08:30 발동 (평일만)
- 오늘의 토픽 결정 (23개 아이템 1:1 매칭)
- Google News 수집 → Claude 어그로 점수 분석 → 메일 발송
"""

from datetime import datetime

from threads_news_topics import (
    get_all_topics,
    get_topic_config,
    get_today_topic,
)
from threads_news_collector import fetch_today_topic_news
from threads_news_analyzer import enrich_with_analysis
import config
from sender import send


# 어그로 점수별 색상
SCORE_COLORS = {
    5: "#dc2626",   # 빨강
    4: "#f59e0b",   # 주황
    3: "#10b981",   # 초록
    2: "#999",
    1: "#999",
}

SCORE_LABELS = {
    5: "🔥 완벽한 재료",
    4: "💪 강력한 재료",
    3: "✅ 괜찮은 재료",
    2: "⚪ 약함",
    1: "⚪ 약함",
}

USE_RECOMMENDATION_COLORS = {
    "Use Today": "#dc2626",
    "Use This Week": "#f59e0b",
    "Save for Later": "#3b82f6",
    "Skip": "#999",
}


def render_email(topic, articles):
    """이메일 HTML 렌더링"""
    
    today = datetime.now().strftime("%Y-%m-%d (%a)")
    weekday_kr = ["월", "화", "수", "목", "금", "토", "일"][datetime.now().weekday()]
    
    config_data = get_topic_config(topic)
    icon = config_data.get("icon", "📰")
    color = config_data.get("color", "#333")
    category = config_data.get("category", "")
    
    # 기사 카드 HTML 생성
    article_cards = []
    for i, article in enumerate(articles, 1):
        analysis = article.get("analysis", {})
        score = analysis.get("agro_score", 0)
        score_color = SCORE_COLORS.get(score, "#999")
        score_label = SCORE_LABELS.get(score, "")
        agro_type = analysis.get("agro_type", "")
        key_hook = analysis.get("key_hook", "")
        content_idea = analysis.get("content_idea", "")
        use_rec = analysis.get("use_recommendation", "")
        use_rec_color = USE_RECOMMENDATION_COLORS.get(use_rec, "#999")
        
        lang_flag = "🇰🇷" if article.get("lang") == "ko" else "🇺🇸"
        
        card = f"""
        <div style="margin:16px 0;padding:14px;border-left:4px solid {score_color};
                    background:#fafafa;border-radius:6px;">
          <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:6px;">
            <span style="background:{score_color};color:#fff;padding:3px 10px;
                         border-radius:12px;font-size:11px;font-weight:600;">
              {score_label} ({score}/5)
            </span>
            <span style="background:#e5e7eb;color:#333;padding:3px 10px;
                         border-radius:12px;font-size:11px;font-weight:600;">
              {agro_type}
            </span>
            <span style="background:{use_rec_color};color:#fff;padding:3px 10px;
                         border-radius:12px;font-size:11px;font-weight:600;">
              {use_rec}
            </span>
          </div>
          
          <div style="font-size:11px;color:#888;margin-top:8px;">
            {lang_flag} {article.get('source','')}
          </div>
          
          <div style="font-weight:600;font-size:14px;margin:4px 0;">
            <a href="{article.get('link','')}" 
               style="color:#1a1a1a;text-decoration:none;">{article.get('title','')}</a>
          </div>
          
          <div style="font-size:12px;color:#666;line-height:1.5;margin:6px 0;">
            {article.get('summary','')[:200]}
          </div>
          
          <div style="margin-top:10px;padding:10px;background:#fff5f0;
                      border-radius:4px;border-left:3px solid #f59e0b;">
            <div style="font-size:12px;font-weight:600;color:#92400e;margin-bottom:4px;">
              💡 어그로 후킹
            </div>
            <div style="font-size:13px;color:#333;font-style:italic;">
              "{key_hook}"
            </div>
          </div>
          
          <div style="margin-top:8px;padding:10px;background:#eff6ff;
                      border-radius:4px;border-left:3px solid #3b82f6;">
            <div style="font-size:12px;font-weight:600;color:#1e40af;margin-bottom:4px;">
              📝 콘텐츠 아이디어
            </div>
            <div style="font-size:13px;color:#333;line-height:1.5;">
              {content_idea}
            </div>
          </div>
        </div>
        """
        article_cards.append(card)
    
    articles_html = "\n".join(article_cards) if article_cards else """
        <div style="padding:20px;background:#fef2f2;border-radius:8px;text-align:center;">
          <p style="color:#991b1b;margin:0;">
            오늘 토픽에 대한 어그로 점수 3+ 기사가 없습니다.<br>
            <small>키워드 조정이 필요하거나, 다른 토픽으로 콘텐츠를 만드는 것이 좋습니다.</small>
          </p>
        </div>
    """
    
    html = f"""<!doctype html>
<html><body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
                   max-width:700px;margin:0 auto;padding:16px;color:#222;background:#fff;">

  <h2 style="border-bottom:3px solid {color};padding-bottom:12px;">
    {icon} 오늘의 Threads 콘텐츠 소재
  </h2>
  
  <p style="color:#666;font-size:13px;">
    {today} ({weekday_kr}요일) · 오늘의 토픽: <b style="color:{color};">{topic}</b><br>
    📂 카테고리: {category}
  </p>
  
  <div style="background:#fffbeb;border-left:4px solid #f59e0b;
              padding:12px;margin:16px 0;border-radius:4px;font-size:13px;">
    <b>💡 사용 방법:</b><br>
    어그로 점수 4~5점 기사 중에서 가장 끌리는 1건 선택 →<br>
    오후 9:30 자동 메일이 와도 좋고, 이 기사로 직접 콘텐츠 만들어도 OK.
  </div>

  <h3 style="margin-top:24px;color:#1a1a1a;">
    📰 분석된 기사 ({len(articles)}건)
  </h3>
  
  {articles_html}

  <p style="color:#999;font-size:11px;margin-top:32px;text-align:center;">
    Claude AI 자동 분석 · 매일 오전 8시 30분 발송 (평일만)
  </p>

</body></html>"""
    
    subject = f"[{datetime.now():%m/%d}] 오늘의 Threads 소재 - {topic} ({len(articles)}건)"
    return subject, html


def main():
    print("🚀 Threads 콘텐츠 소재 뉴스 수집 시작")
    
    # 1. 오늘의 토픽 결정
    topic = get_today_topic()
    if not topic:
        print("⏸️ 주말 - 발송 안 함")
        return
    
    print(f"📌 오늘의 토픽: {topic}")
    
    # 2. Google News에서 뉴스 수집
    articles = fetch_today_topic_news(topic)
    
    if not articles:
        print("❌ 수집된 기사 없음")
        # 빈 메일이라도 발송 (키워드 점검 필요 알림)
        subject, html = render_email(topic, [])
        send(subject, html, config)
        return
    
    # 3. Claude로 어그로 점수 분석 + 필터링
    if config.ANTHROPIC_API_KEY:
        articles = enrich_with_analysis(
            config.ANTHROPIC_API_KEY,
            topic,
            articles,
            min_score=3,
        )
    else:
        print("⚠️ ANTHROPIC_API_KEY 없음 - 분석 생략")
    
    # 상위 15건만 메일에 포함
    articles = articles[:15]
    
    # 4. 이메일 렌더링 + 발송
    subject, html = render_email(topic, articles)
    send(subject, html, config)
    print(f"✅ 발송 완료 - {len(articles)}건")


if __name__ == "__main__":
    main()
