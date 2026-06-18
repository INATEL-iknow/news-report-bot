"""
Threads V3 콘텐츠 일일 발송 메인 실행 파일
- 매일 한국시간 18:00 발동
- 랜덤 5개 주제 선택
- V3 정의서 기반 콘텐츠 생성 (영문 + 한글)
- 본인 이메일로 발송
"""

from datetime import datetime

from threads_v3_topics import get_random_topics
from threads_v3_generator import get_client, generate_multiple_contents
import config
from sender import send


# 콘텐츠 유형별 색상
POST_TYPE_COLORS = {
    "controversial": {"color": "#dc2626", "bg": "#fef2f2", "label": "논쟁형"},
    "mistake_warning": {"color": "#f59e0b", "bg": "#fffbeb", "label": "실수 경고형"},
    "curiosity": {"color": "#7c3aed", "bg": "#faf5ff", "label": "호기심형"},
    "info": {"color": "#0891b2", "bg": "#ecfeff", "label": "자료 기반"},
    "route": {"color": "#16a34a", "bg": "#f0fdf4", "label": "동선형"},
}


def render_content_card(content, idx):
    """단일 콘텐츠 카드 렌더링"""
    keyword = content.get("keyword", "")
    category = content.get("category_name", "")
    post_type = content.get("post_type", "controversial")
    post_type_kr = content.get("post_type_kr", "")
    
    type_cfg = POST_TYPE_COLORS.get(post_type, POST_TYPE_COLORS["controversial"])
    
    main_en = content.get("main_post_en", "")
    c1_en = content.get("comment_1_en", "")
    c2_en = content.get("comment_2_en", "")
    c3_en = content.get("comment_3_en", "")
    
    main_kr = content.get("main_post_kr", "")
    c1_kr = content.get("comment_1_kr", "")
    c2_kr = content.get("comment_2_kr", "")
    c3_kr = content.get("comment_3_kr", "")
    
    # 브랜드명 노출 경고
    leak_warning = content.get("brand_leak_warning", "")
    leak_html = ""
    if leak_warning:
        leak_html = f"""
        <div style="background:#fef2f2;border:2px solid #dc2626;padding:10px;
                    border-radius:6px;margin:8px 0;font-size:12px;color:#991b1b;">
          <b>⚠️ 검토 필요:</b> {leak_warning}
        </div>
        """
    
    return f"""
    <div style="margin:24px 0;padding:0;border:1px solid #e5e7eb;border-radius:12px;
                overflow:hidden;background:#fff;">
      
      <!-- 헤더 -->
      <div style="background:{type_cfg['bg']};padding:12px 16px;
                  border-bottom:1px solid #e5e7eb;">
        <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;">
          <span style="background:{type_cfg['color']};color:#fff;padding:3px 10px;
                       border-radius:12px;font-size:11px;font-weight:600;">
            #{idx} {type_cfg['label']}
          </span>
          <span style="background:#1a1a1a;color:#fff;padding:3px 10px;
                       border-radius:12px;font-size:11px;font-weight:600;">
            키워드: {keyword}
          </span>
        </div>
        <div style="font-size:13px;color:#444;margin-top:6px;font-weight:600;">
          {category}
        </div>
      </div>
      
      {leak_html}
      
      <!-- 본문 -->
      <div style="padding:16px;">
        <div style="font-size:12px;color:#666;font-weight:600;margin-bottom:6px;
                    padding-bottom:4px;border-bottom:1px solid #f3f4f6;">
          1. BODY (본문)
        </div>
        <div style="background:#f9fafb;padding:12px;border-radius:6px;
                    white-space:pre-wrap;font-size:14px;line-height:1.6;
                    margin-bottom:8px;">{main_en}</div>
        <div style="background:#fff8dc;padding:10px;border-radius:6px;
                    white-space:pre-wrap;font-size:13px;line-height:1.6;
                    color:#555;border-left:3px solid #f59e0b;">{main_kr}</div>
      </div>
      
      <!-- 댓글 1 -->
      <div style="padding:16px;border-top:1px solid #f3f4f6;">
        <div style="font-size:12px;color:#666;font-weight:600;margin-bottom:6px;
                    padding-bottom:4px;border-bottom:1px solid #f3f4f6;">
          2. COMMENT 1 (정답 공개)
        </div>
        <div style="background:#f0f7ff;padding:12px;border-radius:6px;
                    white-space:pre-wrap;font-size:14px;line-height:1.6;
                    margin-bottom:8px;">{c1_en}</div>
        <div style="background:#fff8dc;padding:10px;border-radius:6px;
                    white-space:pre-wrap;font-size:13px;line-height:1.6;
                    color:#555;border-left:3px solid #f59e0b;">{c1_kr}</div>
      </div>
      
      <!-- 댓글 2 -->
      <div style="padding:16px;border-top:1px solid #f3f4f6;">
        <div style="font-size:12px;color:#666;font-weight:600;margin-bottom:6px;
                    padding-bottom:4px;border-bottom:1px solid #f3f4f6;">
          3. COMMENT 2 (저장 가치 정보)
        </div>
        <div style="background:#f5eef8;padding:12px;border-radius:6px;
                    white-space:pre-wrap;font-size:14px;line-height:1.6;
                    margin-bottom:8px;">{c2_en}</div>
        <div style="background:#fff8dc;padding:10px;border-radius:6px;
                    white-space:pre-wrap;font-size:13px;line-height:1.6;
                    color:#555;border-left:3px solid #f59e0b;">{c2_kr}</div>
      </div>
      
      <!-- 댓글 3 -->
      <div style="padding:16px;border-top:1px solid #f3f4f6;">
        <div style="font-size:12px;color:#666;font-weight:600;margin-bottom:6px;
                    padding-bottom:4px;border-bottom:1px solid #f3f4f6;">
          4. COMMENT 3 (피글맵 + 키워드 매그넷)
        </div>
        <div style="background:#f0fff4;padding:12px;border-radius:6px;
                    white-space:pre-wrap;font-size:14px;line-height:1.6;
                    margin-bottom:8px;">{c3_en}</div>
        <div style="background:#fff8dc;padding:10px;border-radius:6px;
                    white-space:pre-wrap;font-size:13px;line-height:1.6;
                    color:#555;border-left:3px solid #f59e0b;">{c3_kr}</div>
      </div>
    </div>
    """


def render_email(contents):
    """이메일 HTML 렌더링"""
    today = datetime.now().strftime("%Y-%m-%d (%a)")
    weekday_kr = ["월", "화", "수", "목", "금", "토", "일"][datetime.now().weekday()]
    
    cards_html = ""
    for i, content in enumerate(contents, 1):
        cards_html += render_content_card(content, i)
    
    html = f"""<!doctype html>
<html><body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
                   max-width:720px;margin:0 auto;padding:16px;color:#222;background:#fff;">

  <h2 style="border-bottom:3px solid #1a1a1a;padding-bottom:12px;">
    오늘의 Threads 콘텐츠 5개
  </h2>
  
  <p style="color:#666;font-size:13px;">
    {today} ({weekday_kr}요일) · V3 정의서 기반 자동 생성<br>
    각 콘텐츠: 본문 + 댓글 3개 (영문 + 한글)<br>
    업로드 권장 시간: 오후 10시 (한국시간)
  </p>
  
  <div style="background:#eff6ff;border-left:4px solid #3b82f6;
              padding:12px;margin:16px 0;border-radius:4px;font-size:13px;">
    <b>업로드 방법:</b><br>
    1. 5개 중 원하는 콘텐츠 선택<br>
    2. 본문 업로드 (30초 후) 댓글 1 (30초 후) 댓글 2 (30초 후) 댓글 3<br>
    3. 노란 박스 = 한글 번역 (참고용, 업로드 안 함)<br>
    4. 댓글에 키워드 (HOTEL, ROUTE 등) 단 사람에게 DM 발송
  </div>

  {cards_html}

  <p style="color:#999;font-size:11px;margin-top:32px;text-align:center;">
    Claude AI V3 자동 생성 · 매일 오후 6시 발송
  </p>

</body></html>"""
    
    subject = f"[{datetime.now():%m/%d}] 오늘의 Threads 콘텐츠 5개 (V3)"
    return subject, html


def main():
    print("Threads V3 콘텐츠 생성 시작")
    
    # 1. API 키 확인
    if not config.ANTHROPIC_API_KEY:
        print("ANTHROPIC_API_KEY 없음")
        return
    
    # 2. 랜덤 5개 주제 선택
    keywords = get_random_topics(count=5)
    print(f"오늘의 주제 5개: {', '.join(keywords)}")
    
    # 3. Claude로 콘텐츠 생성
    print("Claude API로 콘텐츠 생성 중...")
    client = get_client(config.ANTHROPIC_API_KEY)
    contents = generate_multiple_contents(client, keywords)
    
    if not contents:
        print("콘텐츠 생성 실패")
        return
    
    print(f"{len(contents)}개 콘텐츠 생성 완료")
    
    # 4. 브랜드명 노출 통계
    leak_count = sum(1 for c in contents if c.get("brand_leak_warning"))
    if leak_count > 0:
        print(f"브랜드명 노출 경고: {leak_count}개 (메일에서 검토 필요)")
    
    # 5. 이메일 렌더링 + 발송
    subject, html = render_email(contents)
    send(subject, html, config)
    print("발송 완료")


if __name__ == "__main__":
    main()
