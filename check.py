import os
import asyncio
import requests
from playwright.async_api import async_playwright

URL = "https://event.xflag.com/events/dreamdaze4/re-sale-tickets/274"
WEBHOOK = os.environ.get("DISCORD_WEBHOOK", "")

NO_TICKET_TEXT = "購入できるリセールチケットがありません。"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--disable-dev-shm-usage",
                "--no-sandbox",
            ],
        )

        page = await browser.new_page(locale="ja-JP")

        await page.goto(URL, wait_until="domcontentloaded", timeout=30000)

        # JavaScript描画を少しだけ待つ
        await page.wait_for_timeout(1000)

        text = await page.locator("body").inner_text()

        await browser.close()

    print("VISIBLE_TEXT_START")
    print(text[:1500])
    print("VISIBLE_TEXT_END")

    no_ticket = NO_TICKET_TEXT in text

    print(f"no_ticket={no_ticket}")

    if no_ticket:
        print("NO_ALERT")
        return

    message = f"🎫 モンストTICKETでリセール出品の可能性があります\n{URL}"

    if WEBHOOK:
        response = requests.post(
            WEBHOOK,
            json={"content": message},
            timeout=20,
        )
        print(f"Discord status={response.status_code}")
        print("DISCORD_SENT")
    else:
        print("WEBHOOK_NOT_SET")

if __name__ == "__main__":
    asyncio.run(main())
