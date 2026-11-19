import os
import glob
import re

# 1. Collect all URLs from all generated XML sitemaps
sitemap_files = glob.glob('sitemap-*.xml')
sitemap_urls = set()

for sm in sitemap_files:
    with open(sm, 'r', encoding='utf-8') as f:
        content = f.read()
    locs = re.findall(r'<loc>(.*?)</loc>', content)
    for loc in locs:
        # Normalize to path without domain
        path = loc.replace('https://msbtenotes-info.netlify.app', '')
        if not path:
            path = '/'
        sitemap_urls.add(path)

print(f"Total unique URLs in all XML sitemaps: {len(sitemap_urls)}")

# 2. Collect all HTML files on disk
ignored_dirs = {'.git', 'node_modules', 'brain', '.gemini', '.system_generated', 'dist', 'build'}

all_disk_html = []
for root, dirs, files in os.walk('.'):
    # filter ignored dirs
    dirs[:] = [d for d in dirs if d not in ignored_dirs]
    for file in files:
        if file.endswith('.html'):
            rel_path = os.path.relpath(os.path.join(root, file), '.').replace('\\', '/')
            all_disk_html.append(rel_path)

print(f"Total HTML files on disk: {len(all_disk_html)}")

# 3. Map disk html to canonical clean URL
def html_to_canonical_path(filepath):
    # index files
    if filepath == 'index.html':
        return '/'
    if filepath.endswith('/index.html'):
        folder = filepath[:-11]
        return '/' + folder.lower() + '/'
    
    # other html files
    clean = '/' + filepath[:-5].lower()
    return clean

# Check each disk file
missing = []
intentional_exclusions = {
    # 0-byte or template or test files
    'courses/test.html',
    'courses/certificate.html',
    'collegeinfo/article-template.html',
    'notes/manual/manual-blank.html',
    # obituary rumor posts explicitly noindexed
    'blog/nana-patekar-tribute',
    'blog/asha-bhosle-death-news',
    'blog/ajit-pawar-death-news'
}

for f in all_disk_html:
    canon = html_to_canonical_path(f)
    if canon not in sitemap_urls:
        missing.append((f, canon))

print(f"\nHTML files on disk not in sitemap: {len(missing)}")
for f, canon in missing:
    print(f"  Disk: {f} -> Clean URL: {canon}")
