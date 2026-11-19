import re

with open('Branches/Computer.html', 'r', encoding='utf-8') as f:
    content = f.read()

links = re.findall(r'href=["\'](/[^"\']+)["\']', content)
print("Sample internal links in Branches/Computer.html:")
for l in links[:15]:
    print(" ", l)
