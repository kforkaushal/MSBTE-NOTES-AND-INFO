import urllib.request
import json

with open('scripts/indexnow_payload.json', 'r', encoding='utf-8') as f:
    payload = json.load(f)

endpoints = [
    "https://api.indexnow.org/indexnow",
    "https://www.bing.com/indexnow",
    "https://yandex.com/indexnow"
]

data = json.dumps(payload).encode('utf-8')

for ep in endpoints:
    print(f"\nSubmitting to: {ep}")
    req = urllib.request.Request(
        ep,
        data=data,
        headers={
            'Content-Type': 'application/json; charset=utf-8',
            'User-Agent': 'IndexNowSubmitter/1.0'
        },
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            print(f"-> SUCCESS: HTTP {resp.getcode()} ({resp.reason})")
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='ignore')
        print(f"-> HTTP Error {e.code}: {e.reason}")
        if body:
            print(f"   Response Body: {body}")
    except Exception as e:
        print(f"-> Error: {e}")
