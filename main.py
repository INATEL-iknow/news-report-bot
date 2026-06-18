"""
News Report - 메인 실행 (슬림 버전)
- 매일 한국시간 09:00 발동
- BetaList + 수익화 아이디어 = 총 10건
"""

import collector
import processor
import insight
import renderer
import sender
import config


def main():
    print("🚀 News Report 시작")
    
    # 1. RSS 수집
    items = collector.fetch_all()
    
    if not items:
        print("❌ 수집된 항목 없음")
        return
    
    # 2. 처리 (중복 제거 + 카테고리 그룹화)
    grouped = processor.process(items)
    
    # 3. Claude로 분석 + 상위 5건 선별
    if not config.ANTHROPIC_API_KEY:
        print("❌ ANTHROPIC_API_KEY 없음")
        return
    
    grouped = insight.enrich_items(config.ANTHROPIC_API_KEY, grouped)
    
    # 4. 이메일 렌더링 + 발송
    subject, html = renderer.render_email(grouped)
    sender.send(subject, html, config)
    print("✅ 발송 완료")


if __name__ == "__main__":
    main()
