import requests

url = "https://event.xflag.com/events/dreamdaze4/re-sale-tickets/274"

response = requests.get(
    url,
    headers={"User-Agent": "Mozilla/5.0"}
)

html = response.text

targets = [
    "現在出品",
    "出品されて",
    "リセールチケット",
    "受付終了",
    "販売終了",
    "予定枚数終了",
    "購入する",
    "申込み",
]

for target in targets:
    if target in html:
        print(f"FOUND: {target}")
