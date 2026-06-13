"""
Threads 콘텐츠 일일 발송 메인 실행 파일
- 매일 한국시간 21:30 발동
- 오늘의 카테고리 결정 → 주제 선택 → Claude API로 콘텐츠 생성
- 본인 이메일로 발송 (복붙해서 22:00 Threads에 업로드)
"""

import os
from datetime import datetime
from anthropic import Anthropic

from threads_topics import get_today_category, get_today_topic
from threads_generator import get_client, generate_threads_content
import config
from sender import send


def render_email(category, topic, content):
    """이메일 HTML 렌더링 - 복사하기 쉽게 디자인"""
    
    today = datetime.now().strftime("%Y-%m-%d (%a)")
    weekday_kr = ["월", "화", "수", "목", "금", "토", "일"][datetime.now().weekday()]
    
    main_post = content.get("main_post", "")
    comment_1 = content.get("comment_1", "")
    comment_2 = content.get("comment_2", "")
    comment_3 = content.get("comment_3", "")
    topic_tag = content.get("topic_tag", "Korea Travel")
    
    html = f"""<!doctype html>
<html><body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
                   max-width:640px;margin:0 auto;padding:16px;color:#222;background:#fff;">

  <h2 style="border-bottom:2px solid #333;padding-bottom:8px;">
    📱 오늘의 Threads 콘텐츠
  </h2>
  
  <p style="color:#666;font-size:13px;">
    {today} ({weekday_kr}) · 카테고리: <b>{category}</b><br>
    🕙 업로드 권장 시간: <b>오후 10시</b> (한국시간)
  </p>
  
  <div style="background:#fffbeb;border-left:4px solid #f59e0b;padding:12px;margin:16px 0;border-radius:4px;">
    <b>📝 주제:</b> {topic}<br>
    <b>🏷️ Topic Tag:</b> {topic_tag}
  </div>

  <hr style="margin:24px 0;border:0;border-top:1px dashed #ccc;">

  <!-- 본문 -->
  <h3 style="color:#1a1a1a;margin-top:24px;">
    📝 BODY (본문)
  </h3>
  <div style="background:#f0f7ff;border:1px solid #4a90e2;border-radius:8px;padding:16px;
              white-space:pre-wrap;font-family:'Pretendard',-apple-system,sans-serif;
              font-size:14px;line-height:1.6;">{main_post}

[Topic: {topic_tag}]</div>
  <p style="color:#888;font-size:12px;margin-top:4px;">
    ↑ 위 텍스트 전체 복사해서 Threads에 본문으로 업로드
  </p>

  <!-- 댓글 1 -->
  <h3 style="color:#1a1a1a;margin-top:32px;">
    💬 COMMENT 1 (정답 공개)
  </h3>
  <p style="color:#888;font-size:12px;">⏰ 본문 업로드 후 <b>5분</b> 뒤에 댓글로 달기</p>
  <div style="background:#fff5f0;border:1px solid #ff8c42;border-radius:8px;padding:16px;
              white-space:pre-wrap;font-family:'Pretendard',-apple-system,sans-serif;
              font-size:14px;line-height:1.6;">{comment_1}</div>

  <!-- 댓글 2 -->
  <h3 style="color:#1a1a1a;margin-top:32px;">
    💬 COMMENT 2 (추가 가치)
  </h3>
  <p style="color:#888;font-size:12px;">⏰ 본문 업로드 후 <b>30분</b> 뒤에 댓글로 달기</p>
  <div style="background:#f5eef8;border:1px solid #8e44ad;border-radius:8px;padding:16px;
              white-space:pre-wrap;font-family:'Pretendard',-apple-system,sans-serif;
              font-size:14px;line-height:1.6;">{comment_2}</div>

  <!-- 댓글 3 -->
  <h3 style="color:#1a1a1a;margin-top:32px;">
    💬 COMMENT 3 (피글맵 + Pglemaps 매그넷)
  </h3>
  <p style="color:#888;font-size:12px;">⏰ 본문 업로드 후 <b>1시간</b> 뒤에 댓글로 달기</p>
  <div style="background:#f0fff4;border:1px solid #27ae60;border-radius:8px;padding:16px;
              white-space:pre-wrap;font-family:'Pretendard',-apple-system,sans-serif;
              font-size:14px;line-height:1.6;">{comment_3}</div>

  <hr style="margin:32px 0;border:0;border-top:1px dashed #ccc;">

  <!-- DM 안내 -->
  <h3 style="color:#1a1a1a;">
    📨 DM 처리 가이드
  </h3>
  <p style="font-size:13px;line-height:1.6;">
    오늘 댓글에 <b>"Pglemaps"</b>라고 남긴 사용자들이 있으면:<br>
    1. Threads 앱 → 본인 게시물 → 댓글 확인<br>
    2. 각 사용자에게 DM 발송 (아래 템플릿 복붙)<br>
  </p>
  
  <div style="background:#fafafa;border:1px solid #ddd;border-radius:8px;padding:16px;
              white-space:pre-wrap;font-family:'Pretendard',-apple-system,sans-serif;
              font-size:13px;line-height:1.6;color:#333;">Thanks for reaching out 🙌

Here's the link to Piglemaps:
👉 pglemaps.com

Just save the places you want to visit, and we'll build your perfect route — completely free.

Let me know if you have any questions about your Korea trip!</div>

  <p style="color:#999;font-size:11px;margin-top:32px;text-align:center;">
    Claude AI 자동 생성 · 매일 오후 9시 30분 발송
  </p>

</body></html>"""
    
    subject = f"[{datetime.now():%m/%d}] 오늘의 Threads 콘텐츠 - {category}"
    return subject, html


def main():
    print("🚀 Threads 콘텐츠 생성 시작")
    
    # 1. 오늘의 카테고리 결정
    category = get_today_category()
    print(f"  카테고리: {category}")
    
    # 2. 오늘의 주제 선택
    topic = get_today_topic(category)
    print(f"  주제: {topic}")
    
    if not topic:
        print("❌ 주제 풀이 비어있음")
        return
    
    # 3. Claude API로 콘텐츠 생성
    if not config.ANTHROPIC_API_KEY:
        print("❌ ANTHROPIC_API_KEY 없음")
        return
    
    print("🤖 Claude API로 콘텐츠 생성 중...")
    client = get_client(config.ANTHROPIC_API_KEY)
    content = generate_threads_content(client, category, topic)
    
    if not content:
        print("❌ 콘텐츠 생성 실패")
        return
    
    print("✅ 콘텐츠 생성 완료")
    print(f"  Topic Tag: {content.get('topic_tag', 'N/A')}")
    
    # 4. 이메일 렌더링
    subject, html = render_email(category, topic, content)
    
    # 5. 이메일 발송
    send(subject, html, config)
    print("✅ 발송 완료")


if __name__ == "__main__":
    main()
