import os
import re
import asyncio
import requests
from playwright.async_api import async_playwright

URLS = [
    {
        "name": "2DAYSチケット",
        "url": "https://event.xflag.com/events/dreamdaze4/re-sale-tickets/274",
    },
    # 追加する場合はこの形で増やしてください
    {
        "name": "7/11チケット",
        "url": "https://event.xflag.com/events/dreamdaze4/re-sale-tickets/275",
    },
    {
        "name": "7/12チケット",
        "url": "https://event.xflag.com/events/dreamdaze4/re-sale-tickets/276",
    },
]

WEBHOOK = os.environ.get("DISCORD_WEBHOOK", "")


def has_any(patterns, text):
    return any(re.search(p, text, re.IGNORECASE | re.DOTALL) for p in patterns)


async def check_one(page, item):
    name = item["name"]
    url = item["url"]

    await page.goto(url, wait_until="domcontentloaded", timeout=60000)
    await page.wait_for_timeout(3000)

    text = await page.locator("body").inner_text()

    print(f"CHECK_NAME={name}")
    print(f"CHECK_URL={url}")
    print("VISIBLE_TEXT_START")
    print(text[:3000])
    print("VISIBLE_TEXT_END")

    negative = (
        "購入できるリセールチケットがありません。" in text
        and "すべて" in text
        and "イベント詳細に戻る" in text
    )

    positive = (
        "件表示" in text
        or "¥" in text
        or "￥" in text
    )

    print(f"negative={negative}")
    print(f"positive={positive}")

    if negative:
        return item

    if positive:
        return item

    return item


async def main():
    found_items = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(locale="ja-JP")

        for item in URLS:
            try:
                result = await check_one(page, item)
                if result:
                    found_items.append(result)
            except Exception as e:
                print(f"ERROR checking {item['name']}: {e}")

        await browser.close()

    if found_items:
        message = "テスト️📝 🎫 モンストTICKETでリセール出品されました\n"

        for item in found_items:
            message += f"{item['name']}\n{item['url']}\n\n"

        if WEBHOOK:
            requests.post(WEBHOOK, json={"content": message}, timeout=20)

        print("DISCORD_SENT")
        raise Exception("RESALE FOUND")

    print("NO_ALERT")


if __name__ == "__main__":
    asyncio.run(main())
