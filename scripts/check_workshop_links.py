import re

files = [
    'Notes/311002-engineering-workshop-practice.html',
    'Notes/311005-engineering-workshop-practice.html',
    'Notes/311007-engineering-workshop-practice.html',
    'Notes/311010-civil-engineering-workshop.html',
    'Notes/msbte-first-year-diploma-notes.html'
]

for p in files:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    drive_links = re.findall(r'https://drive\.google\.com/file/d/([^/]+)/view', content)
    print(f"=== {p} ===")
    print("Drive IDs:", set(drive_links))
