import re

core_pages = ['index.html', 'start.html', 'sitemap.html', 'Notes/index.html', 'pyq/index.html', 'model-answer/index.html', 'Notes/osy-k-scheme-notes.html', 'Notes/msbte-first-year-diploma-notes.html']

for cp in core_pages:
    with open(cp, 'r', encoding='utf-8') as f:
        content = f.read()
    links = re.findall(r'href=["\'](/[^"\']+)["\']', content)
    upper_or_html = [l for l in links if any(cap in l for cap in ['/Blog/', '/Notes/', '/Branches/', '/CollegeInfo/', '/Jobs/', '/Courses/', '/News/']) or l.endswith('.html')]
    print(f"=== {cp}: {len(upper_or_html)} non-canonical hrefs ===")
    for l in list(set(upper_or_html))[:8]:
        print("  ", l)
