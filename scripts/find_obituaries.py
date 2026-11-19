import json

with open('blogs.json', 'r', encoding='utf-8') as f:
    blogs = json.load(f)

for b in blogs:
    title = b.get('title', '')
    id_ = b.get('id', '')
    if any(w in title.lower() for w in ['death', 'passes away', 'rip', 'passed away']):
        print(f"Obituary blog: {id_} -> {title}")
