import requests

url = "https://event.xflag.com/events/dreamdaze4/re-sale-tickets/274"

response = requests.get(
    url,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
)

print("Status:", response.status_code)
print(response.text[:3000])
