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

print(f"Total HTML files to process: {len(all_html)}")

hubs_map = {
    '/notes': '/notes/',
    '/notes/': '/notes/',
    '/notes/index.html': '/notes/',
    '/pyq': '/pyq/',
    '/pyq/': '/pyq/',
    '/pyq/index.html': '/pyq/',
    '/model-answer': '/model-answer/',
    '/model-answer/': '/model-answer/',
    '/model-answer/index.html': '/model-answer/',
    '/blog': '/blog/',
    '/blog/': '/blog/',
    '/blog/index.html': '/blog/',
    '/collegeinfo': '/collegeinfo/',
    '/collegeinfo/': '/collegeinfo/',
    '/collegeinfo/index.html': '/collegeinfo/',
    '/jobs': '/jobs/',
    '/jobs/': '/jobs/',
    '/jobs/index.html': '/jobs/',
    '/courses': '/courses/',
    '/courses/': '/courses/',
    '/courses/index.html': '/courses/',
    '/news': '/news/',
    '/news/': '/news/',
    '/news/index.html': '/news/',
}

asset_exts = ('.png', '.jpg', '.jpeg', '.svg', '.gif', '.webp', '.ico', '.css', '.js', '.json', '.xml', '.txt', '.webmanifest', '.pdf')

def clean_target_url(url):
    # Strip domain if present
    is_domain = False
    prefix = ''
    domain = 'https://msbtenotes-info.netlify.app'
    if url.startswith(domain):
        is_domain = True
        prefix = domain
        url = url[len(domain):]
        if not url:
            url = '/'
    
    # Relative links like "about.html", "contact.html"
    if url in ['about.html', 'contact.html', 'privacy-policy.html', 'internships.html', 'sitemap.html']:
        return prefix + '/' + url[:-5]
    
    if not url.startswith('/'):
        return (prefix + url) if is_domain else url
    
    # It's an absolute path
    base = url
    suffix = ''
    if '#' in base:
        base, hash_part = base.split('#', 1)
        suffix = '#' + hash_part + suffix
    if '?' in base:
        base, query_part = base.split('?', 1)
        suffix = '?' + query_part + suffix

    if any(base.lower().endswith(ext) for ext in asset_exts):
        return (prefix + url) if is_domain else url

    base_lower = base.lower()

    if base_lower in hubs_map:
        return prefix + hubs_map[base_lower] + suffix

    if base_lower.endswith('.html'):
        base_lower = base_lower[:-5]

    if base_lower == '/index':
        base_lower = '/'

    return prefix + base_lower + suffix

total_mod_files = 0
total_replaced_links = 0

for filepath in all_html:
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    orig_content = content

    # 1. Replace in href attributes
    def repl_href(m):
        quote = m.group(1)
        url = m.group(2)
        cleaned = clean_target_url(url)
        return f'href={quote}{cleaned}{quote}'

    content = re.sub(r'href=(["\'])(.*?)\1', repl_href, content)

    # 2. Replace Netlify domain URLs with .html inside schemas/text
    content = re.sub(r'https://msbtenotes-info\.netlify\.app/(about|contact|privacy-policy|internships|start|sitemap)\.html', r'https://msbtenotes-info.netlify.app/\1', content)
    content = re.sub(r'https://msbtenotes-info\.netlify\.app/([Bb]log|[Nn]otes|[Bb]ranches|[Pp]yq|[Mm]odel-[Aa]nswer)/([a-zA-Z0-9_-]+)\.html', lambda m: f'https://msbtenotes-info.netlify.app/{m.group(1).lower()}/{m.group(2).lower()}', content)

    # 3. Clean author url in schemas to /about
    content = re.sub(r'"url":\s*"https://msbtenotes-info\.netlify\.app/about\.html"', r'"url": "https://msbtenotes-info.netlify.app/about"', content)

    if content != orig_content:
        total_mod_files += 1
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

print(f"Done! Modified {total_mod_files} HTML files with clean internal URLs.")
