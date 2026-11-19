import glob
import re
from collections import Counter

for sm in glob.glob('sitemap*.xml'):
    if sm == 'sitemap.xml':
        continue
    with open(sm, 'r', encoding='utf-8') as f:
        c = f.read()
    dates = re.findall(r'<lastmod>(.*?)</lastmod>', c)
    counts = Counter(dates)
    print(f"=== {sm} ({len(dates)} URLs) ===")
    for d, cnt in counts.most_common(5):
        print(f"  {d}: {cnt}")
