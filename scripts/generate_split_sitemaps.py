import os
import subprocess
import re

BASE_URL = "https://msbtenotes-info.netlify.app"

git_date_cache = {}

def get_git_date(filepath):
    norm_path = filepath.replace('\\', '/')
    if norm_path in git_date_cache:
        return git_date_cache[norm_path]
    try:
        res = subprocess.run(
            ['git', 'log', '-1', '--format=%cs', filepath],
            capture_output=True, text=True, check=True
        )
        date = res.stdout.strip()
        if not date:
            date = "2026-11-12"
    except Exception:
        date = "2026-11-12"
    git_date_cache[norm_path] = date
    return date

def format_url_entry(loc, lastmod, changefreq="monthly", priority="0.7"):
    return f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>"""

def write_sitemap(filename, entries):
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    xml.extend(entries)
    xml.append('</urlset>\n')
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(xml))
    print(f"Wrote {filename} with {len(entries)} URLs.")

# 1. Main & Core Platform Pages
main_files = [
    ('', 'index.html', 'weekly', '1.0'),
    ('/start', 'start.html', 'monthly', '0.8'),
    ('/about', 'about.html', 'monthly', '0.6'),
    ('/contact', 'contact.html', 'monthly', '0.5'),
    ('/internships', 'internships.html', 'weekly', '0.7'),
    ('/privacy-policy', 'privacy-policy.html', 'yearly', '0.3'),
    ('/sitemap', 'sitemap.html', 'weekly', '0.5'),
    ('/forum', 'forum.html', 'weekly', '0.7'),
    ('/services', 'services.html', 'monthly', '0.7'),
    ('/videos', 'videos.html', 'weekly', '0.7'),
    ('/links', 'links.html', 'monthly', '0.5'),
    ('/scheme/', 'scheme/index.html', 'monthly', '0.8'),
    ('/scheme/k-scheme', 'scheme/k-scheme.html', 'monthly', '0.8'),
    ('/scheme/i-scheme', 'scheme/i-scheme.html', 'monthly', '0.7'),
    ('/mock-tests/', 'mock-tests/index.html', 'weekly', '0.8'),
    ('/mock-tests/test', 'mock-tests/test.html', 'monthly', '0.6'),
    ('/courses/dsa-basic', 'Courses/DSA-Basic.html', 'monthly', '0.7'),
    ('/jobs/', 'Jobs/index.html', 'weekly', '0.8'),
    ('/news/', 'News/index.html', 'weekly', '0.8'),
]
main_entries = []
for path, src_file, freq, prio in main_files:
    lastmod = get_git_date(src_file) if os.path.exists(src_file) else "2026-11-19"
    main_entries.append(format_url_entry(f"{BASE_URL}{path}" if path else f"{BASE_URL}/", lastmod, freq, prio))
write_sitemap('sitemap-main.xml', main_entries)

# 2. Notes Pages (Hub + Subjects + Lab Manuals)
notes_entries = []
notes_hub_mod = get_git_date('Notes/index.html')
notes_entries.append(format_url_entry(f"{BASE_URL}/notes/", notes_hub_mod, "daily", "0.9"))

for f in sorted(os.listdir('Notes')):
    if f.endswith('.html') and f != 'index.html':
        src = os.path.join('Notes', f)
        slug = f[:-5].lower()
        lastmod = get_git_date(src)
        notes_entries.append(format_url_entry(f"{BASE_URL}/notes/{slug}", lastmod, "weekly", "0.8"))

# Lab manuals
if os.path.exists('Notes/Manual'):
    for f in sorted(os.listdir('Notes/Manual')):
        if f.endswith('.html') and f != 'manual-blank.html':
            src = os.path.join('Notes/Manual', f)
            slug = f[:-5].lower()
            lastmod = get_git_date(src)
            notes_entries.append(format_url_entry(f"{BASE_URL}/notes/manual/{slug}", lastmod, "weekly", "0.7"))

write_sitemap('sitemap-notes.xml', notes_entries)

# 3. Video Courses Sitemap
vc_entries = []
vc_hub_mod = get_git_date('video-course/index.html') if os.path.exists('video-course/index.html') else "2026-11-19"
vc_entries.append(format_url_entry(f"{BASE_URL}/video-course/", vc_hub_mod, "weekly", "0.8"))

if os.path.exists('video-course'):
    for f in sorted(os.listdir('video-course')):
        if f.endswith('.html') and f not in ('index.html', 'topic-template.html'):
            src = os.path.join('video-course', f)
            slug = f[:-5].lower()
            lastmod = get_git_date(src)
            vc_entries.append(format_url_entry(f"{BASE_URL}/video-course/{slug}", lastmod, "monthly", "0.7"))
write_sitemap('sitemap-video-courses.xml', vc_entries)

# 4. PYQ Pages
pyq_entries = []
pyq_hub_mod = get_git_date('pyq/index.html')
pyq_entries.append(format_url_entry(f"{BASE_URL}/pyq/", pyq_hub_mod, "daily", "0.9"))

for f in sorted(os.listdir('pyq')):
    if f.endswith('.html') and f != 'index.html':
        src = os.path.join('pyq', f)
        slug = f[:-5].lower()
        lastmod = get_git_date(src)
        pyq_entries.append(format_url_entry(f"{BASE_URL}/pyq/{slug}", lastmod, "monthly", "0.7"))
write_sitemap('sitemap-pyq.xml', pyq_entries)

# 5. Model Answer Pages
ma_entries = []
ma_hub_mod = get_git_date('model-answer/index.html')
ma_entries.append(format_url_entry(f"{BASE_URL}/model-answer/", ma_hub_mod, "daily", "0.9"))

for f in sorted(os.listdir('model-answer')):
    if f.endswith('.html') and f != 'index.html':
        src = os.path.join('model-answer', f)
        slug = f[:-5].lower()
        lastmod = get_git_date(src)
        ma_entries.append(format_url_entry(f"{BASE_URL}/model-answer/{slug}", lastmod, "monthly", "0.7"))
write_sitemap('sitemap-model-answer.xml', ma_entries)

# 6. Branches Pages
branches_entries = []
for f in sorted(os.listdir('Branches')):
    if f.endswith('.html'):
        src = os.path.join('Branches', f)
        if os.path.getsize(src) == 0:
            continue
        slug = f[:-5].lower()
        lastmod = get_git_date(src)
        branches_entries.append(format_url_entry(f"{BASE_URL}/branches/{slug}", lastmod, "monthly", "0.7"))
write_sitemap('sitemap-branches.xml', branches_entries)

# 7. Blog Pages (Exclude noindexed obituaries)
blog_entries = []
blog_hub_mod = get_git_date('Blog/index.html')
blog_entries.append(format_url_entry(f"{BASE_URL}/blog/", blog_hub_mod, "daily", "0.9"))

excluded_blogs = {'nana-patekar-tribute.html', 'asha-bhosle-death-news.html', 'ajit-pawar-death-news.html'}

for f in sorted(os.listdir('Blog')):
    if f.endswith('.html') and f != 'index.html' and f not in excluded_blogs:
        src = os.path.join('Blog', f)
        slug = f[:-5].lower()
        lastmod = get_git_date(src)
        blog_entries.append(format_url_entry(f"{BASE_URL}/blog/{slug}", lastmod, "monthly", "0.7"))
write_sitemap('sitemap-blog.xml', blog_entries)

# 8. Colleges Pages
colleges_entries = []
colleges_hub_mod = get_git_date('CollegeInfo/index.html') if os.path.exists('CollegeInfo/index.html') else "2026-11-12"
colleges_entries.append(format_url_entry(f"{BASE_URL}/collegeinfo/", colleges_hub_mod, "weekly", "0.8"))

if os.path.exists('CollegeInfo'):
    for f in sorted(os.listdir('CollegeInfo')):
        if f.endswith('.html') and f not in ('index.html', 'article-template.html'):
            src = os.path.join('CollegeInfo', f)
            slug = f[:-5].lower()
            lastmod = get_git_date(src)
            colleges_entries.append(format_url_entry(f"{BASE_URL}/collegeinfo/{slug}", lastmod, "monthly", "0.6"))
write_sitemap('sitemap-colleges.xml', colleges_entries)

# 9. Master Sitemap Index (sitemap.xml)
sitemaps_list = [
    ('sitemap-main.xml', main_entries),
    ('sitemap-notes.xml', notes_entries),
    ('sitemap-pyq.xml', pyq_entries),
    ('sitemap-model-answer.xml', ma_entries),
    ('sitemap-branches.xml', branches_entries),
    ('sitemap-blog.xml', blog_entries),
    ('sitemap-colleges.xml', colleges_entries),
    ('sitemap-video-courses.xml', vc_entries)
]

index_xml = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']

for s_file, s_entries in sitemaps_list:
    dates = re.findall(r'<lastmod>(.*?)</lastmod>', '\n'.join(s_entries))
    latest = max(dates) if dates else "2026-11-19"
    index_xml.append(f"""  <sitemap>
    <loc>{BASE_URL}/{s_file}</loc>
    <lastmod>{latest}</lastmod>
  </sitemap>""")

index_xml.append('</sitemapindex>\n')

with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write('\n'.join(index_xml))

print("Wrote master sitemap index: sitemap.xml")
