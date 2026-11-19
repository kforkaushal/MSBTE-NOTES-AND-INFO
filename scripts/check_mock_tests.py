import os
import re

for f in os.listdir('mock-tests'):
    if f.endswith('.html'):
        p = os.path.join('mock-tests', f)
        with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
            c = fp.read()
        title = re.findall(r'<title>(.*?)</title>', c)
        canon = re.findall(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', c)
        print(f"{f} -> Title: {title[0] if title else 'None'} | Canon: {canon[0] if canon else 'None'}")
