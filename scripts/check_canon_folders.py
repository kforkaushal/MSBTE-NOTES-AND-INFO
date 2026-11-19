import os
import re
from collections import Counter

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

canon_by_folder = Counter()
canon_examples = {}

for p in all_html:
    with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
        content = fp.read()
    m = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', content)
    if m:
        c_url = m.group(1)
        if c_url.endswith('.html'):
            fld = p.split(os.sep)[0]
            canon_by_folder[fld] += 1
            if fld not in canon_examples:
                canon_examples[fld] = c_url

print("Canonicals ending with .html by folder:")
for fld, cnt in canon_by_folder.items():
    print(f"  {fld}: {cnt} (e.g. {canon_examples[fld]})")
