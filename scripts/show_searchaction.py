import re
import json

for html in ['index.html', 'Notes/index.html']:
    with open(html, 'r', encoding='utf-8') as f:
        content = f.read()
    m = re.findall(r'<script type="application/ld\+json">(.*?)</script>', content, flags=re.DOTALL)
    print(f"=== {html} ===")
    for block in m:
        if 'SearchAction' in block:
            print(block.strip())
