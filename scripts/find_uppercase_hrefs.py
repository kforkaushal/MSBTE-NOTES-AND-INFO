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

# Let's inspect uppercase hrefs
cap_patterns = ['/Blog/', '/Notes/', '/Branches/', '/CollegeInfo/', '/Jobs/', '/Courses/', '/News/']
caps_found = []

for p in all_html:
    with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
        content = fp.read()
    for cp in cap_patterns:
        matches = re.findall(rf'href=["\']({cp}[^"\']*)["\']', content)
        if matches:
            caps_found.append((p, cp, len(matches), matches[:3]))

print(f"Total files containing uppercase hrefs: {len(caps_found)}")
for p, cp, count, sample in caps_found[:15]:
    print(f"  {p} [{cp}] x{count}: {sample}")
