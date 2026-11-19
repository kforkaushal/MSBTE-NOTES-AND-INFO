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

bad_html_hrefs = []
uppercase_hrefs = []

for filepath in all_html:
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    matches = re.findall(r'href=["\'](/[^"\']+)["\']', content)
    for m in matches:
        # Check if internal link ends in .html
        if m.endswith('.html'):
            bad_html_hrefs.append((filepath, m))
        # Check if internal link has uppercase folder like /Notes/, /Blog/, etc.
        for u in ['/Notes/', '/Blog/', '/Branches/', '/CollegeInfo/', '/Jobs/', '/Courses/', '/News/', '/PYQ/', '/Model-Answer/']:
            if u in m:
                uppercase_hrefs.append((filepath, m))

print(f"Remaining internal hrefs ending with .html: {len(bad_html_hrefs)}")
if bad_html_hrefs:
    print("Samples:", bad_html_hrefs[:10])

print(f"Remaining uppercase folder hrefs: {len(uppercase_hrefs)}")
if uppercase_hrefs:
    print("Samples:", uppercase_hrefs[:10])
