import os
import re

folders = ['Blog', 'Branches', 'CollegeInfo', 'Courses', 'Jobs', 'mock-tests', 'model-answer', 'News', 'Notes', 'pyq', 'scheme', 'video-course']
root_files = ['index.html', 'start.html', 'about.html', 'contact.html', 'internships.html', 'privacy-policy.html', 'sitemap.html']

all_html = []
for rf in root_files:
    if os.path.exists(rf):
        all_html.append(rf)

for fld in folders:
    if os.path.exists(fld):
        for root, _, filenames in os.walk(fld):
            for fn in filenames:
                if fn.endswith('.html'):
                    all_html.append(os.path.join(root, fn))

canonicals_with_html = []
canonicals_uppercase = []
start_canonical = None

cap_prefixes = ['/Blog/', '/Notes/', '/Branches/', '/CollegeInfo/', '/Jobs/', '/Courses/', '/News/', '/PYQ/', '/Model-Answer/']
internal_href_caps = {p: 0 for p in cap_prefixes}
internal_href_dot_html = 0

for p in all_html:
    with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
        content = fp.read()
    
    # check canonical
    m = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', content)
    if m:
        c_url = m.group(1)
        if p == 'start.html':
            start_canonical = c_url
        if c_url.endswith('.html'):
            canonicals_with_html.append((p, c_url))
        for cap in ['/Blog/', '/Notes/', '/Branches/', '/CollegeInfo/', '/Jobs/', '/Courses/', '/News/', '/PYQ/', '/Model-Answer/']:
            if cap in c_url:
                canonicals_uppercase.append((p, c_url))
                break

    # check internal hrefs
    for cap in cap_prefixes:
        count = content.count(f'href="{cap}')
        internal_href_caps[cap] += count
    
    # count hrefs ending with .html
    # e.g. href="/anything.html"
    matches = re.findall(r'href="(/[^"?#]+\.html)"', content)
    internal_href_dot_html += len(matches)

print(f"start.html canonical: {start_canonical}")
print(f"Total canonicals ending with .html: {len(canonicals_with_html)}")
for p, c in canonicals_with_html[:10]:
    print(f"  {p} -> {c}")
print(f"Total canonicals with uppercase path: {len(canonicals_uppercase)}")
print("Internal hrefs with uppercase prefixes:")
for cap, cnt in internal_href_caps.items():
    print(f"  {cap}: {cnt}")
print(f"Total internal hrefs ending with .html: {internal_href_dot_html}")
