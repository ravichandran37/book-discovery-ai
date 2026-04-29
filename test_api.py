import requests
import json

url = "http://127.0.0.1:8000/api/discovery/ask/"

payload = {
    "query": "I want a dark, gritty sci-fi book about rogue AI."
}

headers = {
    "Content-Type": "application/json"
}

print("Thinking...")
response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200:
    data = response.json()
    print("\n--- AI RECOMMENDATION ---")
    print(data.get("recommendation"))
    print("\n--- BOOK DATA ---")
    print(json.dumps(data.get("book_data"), indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)