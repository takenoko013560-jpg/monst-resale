import os
import re
import asyncio
import requests
from playwright.async_api import async_playwright

URL = "https://event.xflag.com/events/dreamdaze4/re-sale-tickets/274"
WEBHOOK = os.environ.get("DISCORD_WEBHOOK", "")


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

    #negative1 = "購入できるリセールチケットがありません。" in text
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
    #print(f"negative1={negative1}")

    # 「出品ありっぽい」かつ「出品なし文言がない」なら通知
    if negative:
        print ("NO_ALERT")
    elif (not negative) and positive:
        message = f"🎫 2DAYSチケットがリセール出品されました\n{URL}"
        if WEBHOOK:
            requests.post(WEBHOOK, json={"content": message}, timeout=20)
        print("DISCORD_SENT")
        raise Exception("RESALE FOUND")
    else:
        print("NO_ALERT")

    #if not negative:
        #raise Exception("negative")


if __name__ == "__main__":
    asyncio.run(main())
