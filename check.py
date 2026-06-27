import requests

url = "https://event.xflag.com/events/dreamdaze4/re-sale-tickets/274"

response = requests.get(
    url,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
)

html = response.text

print("Status:", response.status_code)

keywords = [
    "リセール",
    "出品",
    "購入",
    "チケット",
    "販売",
    "SOLD",
]

for keyword in keywords:
    print(f"{keyword}: {keyword in html}")
