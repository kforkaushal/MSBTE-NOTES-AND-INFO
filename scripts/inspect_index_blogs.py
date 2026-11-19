with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# find all blog cards or links
matches = re.findall(r'<a href="([^"]*(?:blog|Blog)[^"]*)"', text)
for m in matches:
    print(m)
