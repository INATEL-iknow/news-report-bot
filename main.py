import config
from collector import fetch_all
from processor import curate_by_category
from insight import enrich_items
from renderer import render
from sender import send

def main():
    items = fetch_all(config.FEEDS, hours=24)
    print(f"수집: {len(items)}건")

    items_by_cat = curate_by_category(
        items,
        config.KEYWORDS_BOOST,
        config.KEYWORDS_BLOCK,
        config.CATEGORY_QUOTA,
    )
    for cat, lst in items_by_cat.items():
        print(f"  - {cat}: {len(lst)}건")

    # AI 인사이트 추가
    if config.ANTHROPIC_API_KEY:
        print("🤖 Claude AI로 인사이트 생성 중...")
        items_by_cat = enrich_items(
            items_by_cat,
            config.ANTHROPIC_API_KEY,
            config.PIGLEMAPS_CONTEXT,
        )
    else:
        print("⚠️ ANTHROPIC_API_KEY 없음 - 인사이트 생략")

    subject, html = render(items_by_cat)
    send(subject, html, config)
    print("✅ 발송 완료")

if __name__ == "__main__":
    main()
