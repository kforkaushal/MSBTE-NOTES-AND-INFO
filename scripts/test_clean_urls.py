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

def clean_internal_url(url):
    # Only touch internal absolute paths starting with /
    # Ignore protocol, mailto, tel, javascript, hash-only
    if not url.startswith('/') or url.startswith('//'):
        return url
    
    # Separate query/hash
    base = url
    suffix = ''
    if '#' in base:
        base, hash_part = base.split('#', 1)
        suffix = '#' + hash_part + suffix
    if '?' in base:
        base, query_part = base.split('?', 1)
        suffix = '?' + query_part + suffix

    # Ignore static assets
    asset_exts = ('.png', '.jpg', '.jpeg', '.svg', '.gif', '.webp', '.ico', '.css', '.js', '.json', '.xml', '.txt', '.webmanifest', '.pdf')
    if any(base.lower().endswith(ext) for ext in asset_exts):
        return url

    # Lowercase path
    base_lower = base.lower()

    # Handle hubs
    hubs = [
        '/notes/index.html', '/notes/', '/notes',
        '/pyq/index.html', '/pyq/', '/pyq',
        '/model-answer/index.html', '/model-answer/', '/model-answer',
        '/blog/index.html', '/blog/', '/blog',
        '/collegeinfo/index.html', '/collegeinfo/', '/collegeinfo',
        '/jobs/index.html', '/jobs/', '/jobs',
        '/courses/index.html', '/courses/', '/courses',
        '/news/index.html', '/news/', '/news',
        '/scheme/index.html', '/scheme/', '/scheme',
        '/mock-tests/index.html', '/mock-tests/', '/mock-tests',
        '/video-course/index.html', '/video-course/', '/video-course'
    ]
    
    for h in ['/notes', '/pyq', '/model-answer', '/blog', '/collegeinfo', '/jobs', '/courses', '/news', '/scheme', '/mock-tests', '/video-course']:
        if base_lower in [h, h + '/', h + '/index.html']:
            return h + '/' + suffix

    # Strip .html
    if base_lower.endswith('.html'):
        base_lower = base_lower[:-5]

    # Specific root pages
    if base_lower == '/index':
        base_lower = '/'

    return base_lower + suffix

# Let's test on index.html
with open('index.html', 'r', encoding='utf-8') as f:
    sample_content = f.read()

matches = re.findall(r'href=["\'](/[^"\']+)["\']', sample_content)
changes = []
for m in matches:
    cleaned = clean_internal_url(m)
    if cleaned != m:
        changes.append((m, cleaned))

print(f"Sample index.html cleanable hrefs: {len(changes)}")
for o, n in changes[:15]:
    print(f"  {o} -> {n}")
