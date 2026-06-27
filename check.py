import os
import re
import asyncio
import requests
from playwright.async_api import async_playwright

URL = "https://event.xflag.com/events/dreamdaze4/re-sale-tickets/274"
WEBHOOK = os.environ.get("DISCORD_WEBHOOK", "")

# ここは後で調整しやすいようにしてあります
POSITIVE_PATTERNS = [
    r"購入する",
    r"申込",
    r"受付中",
    r"出品中",
]

NEGATIVE_PATTERNS = [
    r"出品はありません",
    r"現在.*ありません",
    r"該当.*ありません",
    r"リセール.*ありません",
]

def has_any(patterns, text):
    return any(re.search(p, text, re.IGNORECASE | re.DOTALL) for p in patterns)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(locale="ja-JP")
        await page.goto(URL, wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_timeout(3000)

        text = await page.locator("body").inner_text()
        await browser.close()

    print("VISIBLE_TEXT_START")
    print(text[:3000])
    print("VISIBLE_TEXT_END")

    negative = "購入できるリセールチケットがありません。" in text

    print(f"negative={negative}")

    # 「出品ありっぽい」かつ「出品なし文言がない」なら通知
    if not negative:
        message = f"🎫 モンストTICKETでリセール出品の可能性があります\n{URL}"
        if WEBHOOK:
            requests.post(WEBHOOK, json={"content": message}, timeout=20)
        print("DISCORD_SENT")
    else:
        print("NO_ALERT")

if __name__ == "__main__":
    asyncio.run(main())
