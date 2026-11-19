import re

with open('sitemap.html', 'r', encoding='utf-8') as f:
    text = f.read()

links = re.findall(r'href=["\']([^"\']+)["\']', text)
bad = [l for l in links if l.endswith('.html') or any(u in l for u in ['/Notes/', '/Blog/', '/Branches/'])]
print(f"sitemap.html total links: {len(links)}, non-clean links: {len(bad)}")
if bad:
    print("Sample bad:", bad[:10])
