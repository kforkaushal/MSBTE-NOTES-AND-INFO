import os
import re

root_candidates = ['links.html', 'forum.html', 'videos.html', 'services.html']

for f in root_candidates:
    if os.path.exists(f):
        with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
            content = fp.read()
        title = re.findall(r'<title>(.*?)</title>', content)
        canon = re.findall(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', content)
        robots = re.findall(r'<meta\s+name=["\']robots["\'][^>]+>', content)
        size = os.path.getsize(f)
        print(f"{f} (Size: {size}) | Title: {title[0] if title else 'No Title'} | Canonical: {canon[0] if canon else 'No Canon'} | Robots: {robots}")
