import re

files = [
    'Notes/311002-engineering-workshop-practice.html',
    'Notes/311005-engineering-workshop-practice.html',
    'Notes/311007-engineering-workshop-practice.html',
    'Notes/311010-civil-engineering-workshop.html'
]

for p in files:
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
    links = re.findall(r'href="(https://drive\.google\.com/[^"]+)"', content)
    h1 = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
    print(f"=== {p} ===")
    print("H1:", [h.strip() for h in h1])
    print("Links:", links)
