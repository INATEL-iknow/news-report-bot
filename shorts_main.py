"""
유튜브 쇼츠 대본 자동화 - 메인 실행
- 매일 한국시간 07:40 발동
- 국내 + 해외 연예 이슈 3개 엄선
- 심층 대본 + 영어 자막 + 관련 기사 링크
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

# 서브카테고리 한글 매핑
SUBCATEGORY_KR = {
    "breakup": "연애/결별",
    "wedding": "결혼",
    "scandal": "스캔들",
    "comeback": "컴백/신곡",
    "collab": "협업",
    "controversy": "논란",
    "other": "이슈",
}


def render_script_card(script, idx):
    """단일 대본 카드 렌더링"""
    issue = script.get("issue_info", {})
    category = script.get("evaluation", {}).get("category", "domestic")
    
    cat_cfg = CATEGORY_COLORS.get(category, CATEGORY_COLORS["domestic"])
    
    # 화제성 별
    virality_stars = issue.get("virality_stars", "⭐⭐⭐")
    subcategory_kr = issue.get("subcategory_kr", "이슈")
    hook_summary = issue.get("hook_summary", "")
    
    # 본문 요약
    summary_lines = script.get("article_summary_kr", [])
    summary_html = "".join(
        f'<li style="margin:4px 0;">{line}</li>' for line in summary_lines
    )
    
    # 한국어 대본
    script_kr = script.get("script_kr", {})
    hook = script_kr.get("hook", "")
    body = script_kr.get("body", "")
    twist = script_kr.get("twist", "")
    cta = script_kr.get("cta", "")
    char_count = script.get("char_count", 0)
    
    # 영어 자막
    subtitles = script.get("english_subtitles", [])
    subtitles_html = "".join(
        f'<div style="padding:3px 0;font-family:monospace;font-size:12px;">{line}</div>'
        for line in subtitles
    )
    
    # 관련 기사 링크
    original_link = script.get("original_link", "")
    original_source = script.get("original_source", "")
    original_title = script.get("original_title", "")
    
    return f"""
    <div style="margin:24px 0;padding:0;border:1px solid #e5e7eb;border-radius:12px;
                overflow:hidden;background:#fff;box-shadow:0 2px 4px rgba(0,0,0,0.05);">
      
      <!-- 헤더 -->
      <div style="background:{cat_cfg['bg']};padding:14px 16px;
                  border-bottom:1px solid #e5e7eb;">
        <div style="display:flex;gap:6px;flex-wrap:wrap;align-items:center;margin-bottom:6px;">
          <span style="background:{cat_cfg['color']};color:#fff;padding:3px 10px;
                       border-radius:12px;font-size:11px;font-weight:600;">
            #{idx} {cat_cfg['icon']} {cat_cfg['label']} · {subcategory_kr}
          </span>
          <span style="background:#1a1a1a;color:#fff;padding:3px 10px;
                       border-radius:12px;font-size:11px;font-weight:600;">
            화제성 {virality_stars}
          </span>
        </div>
        <div style="font-size:13px;color:#444;font-weight:600;">
          💡 {hook_summary}
        </div>
      </div>
      
      <!-- 원문 제목 -->
      <div style="padding:12px 16px;background:#fafafa;border-bottom:1px solid #f3f4f6;">
        <div style="font-size:11px;color:#666;margin-bottom:4px;">원문 기사</div>
        <a href="{original_link}" style="color:#1a1a1a;text-decoration:none;font-size:13px;">
          {original_title}
        </a>
        <div style="font-size:10px;color:#999;margin-top:2px;">{original_source}</div>
      </div>
      
      <!-- 본문 요약 -->
      <div style="padding:14px 16px;border-bottom:1px solid #f3f4f6;">
        <div style="font-size:12px;color:#666;font-weight:600;margin-bottom:6px;">
          📰 본문 요약
        </div>
        <ul style="margin:8px 0;padding-left:20px;font-size:13px;line-height:1.6;color:#333;">
          {summary_html}
        </ul>
      </div>
      
      <!-- 한국어 대본 -->
      <div style="padding:14px 16px;border-bottom:1px solid #f3f4f6;">
        <div style="font-size:12px;color:#666;font-weight:600;margin-bottom:8px;">
          🎬 한국어 대본 (TTS용, 약 {char_count}자 / 60초)
        </div>
        
        <div style="margin:6px 0;padding:10px;background:#fff8dc;border-radius:6px;
                    border-left:3px solid #f59e0b;">
          <div style="font-size:11px;color:#666;font-weight:600;margin-bottom:4px;">
            [후킹 · 0:00-0:04]
          </div>
          <div style="font-size:14px;line-height:1.6;white-space:pre-wrap;">{hook}</div>
        </div>
        
        <div style="margin:6px 0;padding:10px;background:#f9fafb;border-radius:6px;
                    border-left:3px solid #6b7280;">
          <div style="font-size:11px;color:#666;font-weight:600;margin-bottom:4px;">
            [본문 · 0:04-0:43]
          </div>
          <div style="font-size:14px;line-height:1.6;white-space:pre-wrap;">{body}</div>
        </div>
        
        <div style="margin:6px 0;padding:10px;background:#fef2f2;border-radius:6px;
                    border-left:3px solid #dc2626;">
          <div style="font-size:11px;color:#666;font-weight:600;margin-bottom:4px;">
            [반전 · 0:43-0:53]
          </div>
          <div style="font-size:14px;line-height:1.6;white-space:pre-wrap;">{twist}</div>
        </div>
        
        <div style="margin:6px 0;padding:10px;background:#f0fdf4;border-radius:6px;
                    border-left:3px solid #16a34a;">
          <div style="font-size:11px;color:#666;font-weight:600;margin-bottom:4px;">
            [CTA · 0:53-1:00]
          </div>
          <div style="font-size:14px;line-height:1.6;white-space:pre-wrap;">{cta}</div>
        </div>
      </div>
      
      <!-- 영어 자막 -->
      <div style="padding:14px 16px;">
        <div style="font-size:12px;color:#666;font-weight:600;margin-bottom:8px;">
          🌐 영어 자막 ({len(subtitles)}개 컷)
        </div>
        <div style="background:#1a1a1a;color:#fff;padding:12px;border-radius:6px;">
          {subtitles_html}
        </div>
      </div>
    </div>
    """


def render_email(scripts):
    """이메일 HTML 렌더링"""
    today = datetime.now().strftime("%Y-%m-%d (%a)")
    weekday_kr = ["월", "화", "수", "목", "금", "토", "일"][datetime.now().weekday()]
    
    # 카테고리 통계
    domestic_count = sum(
        1 for s in scripts 
        if s.get("evaluation", {}).get("category") == "domestic"
    )
    global_count = sum(
        1 for s in scripts 
        if s.get("evaluation", {}).get("category") == "global"
    )
    
    cards_html = ""
    for i, script in enumerate(scripts, 1):
        cards_html += render_script_card(script, i)
    
    html = f"""<!doctype html>
<html><body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
                   max-width:720px;margin:0 auto;padding:16px;color:#222;background:#f9fafb;">

  <div style="background:#fff;padding:24px;border-radius:12px;">
    
    <h2 style="margin:0 0 8px 0;border-bottom:2px solid #1a1a1a;padding-bottom:10px;">
      🎬 오늘의 유튜브 쇼츠 대본 3개
    </h2>
    
    <p style="color:#666;font-size:13px;margin:8px 0;">
      {today} ({weekday_kr}요일)<br>
      국내 {domestic_count}건 + 해외 {global_count}건 = 총 {len(scripts)}개 대본<br>
      TTS 나레이션용 · 자극 + 공감 + 분쟁 CTA
    </p>
    
    <div style="background:#eff6ff;border-left:4px solid #3b82f6;
                padding:12px;margin:16px 0;border-radius:4px;font-size:13px;">
      <b>📌 사용 방법:</b><br>
      1. 3개 중 촬영/편집할 대본 1-2개 선택<br>
      2. 한국어 대본 → TTS 서비스로 나레이션 생성<br>
      3. 영어 자막을 편집 프로그램에 시간대별 입력<br>
      4. 본문 요약과 관련 링크는 영상 설명에 활용<br>
      <br>
      <b>⏰ 발송 시간:</b> 매일 오전 7:40 (오늘 촬영용)
    </div>

    {cards_html}

    <p style="color:#999;font-size:11px;margin-top:32px;text-align:center;
              border-top:1px solid #e5e7eb;padding-top:16px;">
      Claude AI 자동 생성 · 매일 오전 7:40 발송<br>
      Step 1 Haiku 화제성 평가 → Step 2 Opus 심층 대본
    </p>
  </div>

</body></html>"""
    
    subject = f"[{datetime.now():%m/%d}] 오늘의 유튜브 쇼츠 대본 {len(scripts)}개"
    return subject, html


def main():
    print("🎬 유튜브 쇼츠 대본 자동화 시작")
    
    # 1. API 키 확인
    if not config.ANTHROPIC_API_KEY:
        print("❌ ANTHROPIC_API_KEY 없음")
        return
    
    # 2. 연예 뉴스 수집
    print("\n[1단계] 뉴스 수집")
    items = shorts_topics.fetch_all()
    
    if not items:
        print("❌ 수집된 뉴스 없음")
        return
    
    # 3. Claude로 평가 + 상위 3개 선정 + 대본 생성
    print("\n[2단계] 화제성 평가 + 대본 생성")
    scripts = shorts_generator.generate_all_scripts(
        config.ANTHROPIC_API_KEY, items
    )
    
    if not scripts:
        print("❌ 대본 생성 실패")
        return
    
    # 4. 이메일 발송
    print("\n[3단계] 메일 발송")
    subject, html = render_email(scripts)
    send(subject, html, config)
    
    print(f"\n✅ 완료: {len(scripts)}개 대본 발송")


if __name__ == "__main__":
    main()
