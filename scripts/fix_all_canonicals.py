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

updated_files = 0

for p in all_html:
    with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
        content = fp.read()

    # Look for canonical link tag
    m = re.search(r'(<link\s+rel=["\']canonical["\']\s+href=["\'])([^"\']+)(["\'])', content)
    if m:
        prefix = m.group(1)
        url = m.group(2)
        suffix = m.group(3)

        new_url = url
        # If url is not the homepage and ends with .html, strip .html
        if new_url != 'https://msbtenotes-info.netlify.app/' and new_url.endswith('.html'):
            new_url = new_url[:-5]
        
        # Lowercase the path part of the URL (after domain)
        domain = 'https://msbtenotes-info.netlify.app'
        if new_url.startswith(domain):
            path_part = new_url[len(domain):]
            # specific exceptions: none, all paths should be lowercase
            path_part = path_part.lower()
            new_url = domain + path_part

        if new_url != url:
            old_tag = m.group(0)
            new_tag = f'{prefix}{new_url}{suffix}'
            content = content.replace(old_tag, new_tag)
            with open(p, 'w', encoding='utf-8') as fp:
                fp.write(content)
            updated_files += 1

print(f"Updated canonical tags in {updated_files} files.")
