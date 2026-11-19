import os
import re
import datetime
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
from collections import defaultdict

BASE_URL = "https://msbtenotes-info.netlify.app"

EXCLUDE_EXACT = {
    '404.html',
    'googlef85124961115b472.html',
    'pinterest-9961f.html',
    'yandex_7a3f92ea9dc08f64.html',
    'note_page_template.html',
    'article-template.html',
    'topic-template.html',
    'single_post_template.html',
    'blog-frame.html',
    'Courses/test.html',
    'Notes/Manual/manual-blank.html',
    'Branches/3316326-emerging-trends-in-electrical-engineering.html',
    'Jobs/apply-redirect.html',
    'Jobs/success-redirect.html',
    'search-results.html'
}

def get_lastmod(filepath):
    try:
        ts = os.path.getmtime(filepath)
        dt = datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc)
        return dt.strftime('%Y-%m-%d')
    except Exception:
        return '2026-11-16'

def get_title_and_canonical(filepath, default_url):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as fp:
            head = fp.read(4000)
        c_match = re.search(r'<link rel=["\']canonical["\'] href=["\'](.*?)["\']', head, re.I)
        t_match = re.search(r'<title>(.*?)</title>', head, re.I | re.S)
        
        canon = c_match.group(1).strip() if c_match else default_url
        title = re.sub(r'\s+', ' ', t_match.group(1)).strip() if t_match else os.path.basename(filepath)
        return title, canon
    except Exception:
        return os.path.basename(filepath), default_url

def clean_subject_title(filename, raw_title):
    t = raw_title.split('—')[0].split('|')[0].strip()
    if 'MSBTE' in t:
        t = t.replace('MSBTE', '').strip()
    if 'K-Scheme' in t:
        t = t.replace('K-Scheme', '').strip()
    if 'Notes' in t and len(t) > 25:
        t = t.replace('Notes', '').strip()
    if not t or len(t) < 3:
        base = os.path.splitext(os.path.basename(filename))[0]
        t = base.replace('-', ' ').title()
    return t.strip(' -:')

print("Collecting site pages across all folders...")

core_entries = []
notes_entries = []
manual_entries = []
pyq_entries = []
model_answer_entries = []
branches_hubs_entries = []
branches_subject_entries = []
blog_entries = []
college_entries = []
video_entries = []
courses_entries = []
jobs_entries = []
schemes_entries = []
mock_entries = []
news_entries = []

# 1. CORE / ROOT
core_defs = [
    ('index.html', f"{BASE_URL}/", 'daily', '1.0', '🏠 Home'),
    ('start.html', f"{BASE_URL}/start.html", 'weekly', '0.95', '🚀 Start Here Guide'),
    ('services.html', f"{BASE_URL}/services", 'weekly', '0.85', '⚡ Services'),
    ('videos.html', f"{BASE_URL}/videos", 'weekly', '0.85', '🎥 Videos & Tutorials'),
    ('internships.html', f"{BASE_URL}/internships", 'weekly', '0.82', '💼 Internships Portal'),
    ('forum.html', f"{BASE_URL}/forum", 'weekly', '0.78', '💬 Forum / Community'),
    ('sitemap.html', f"{BASE_URL}/sitemap", 'monthly', '0.60', '📍 Sitemap (HTML)'),
    ('about.html', f"{BASE_URL}/about", 'yearly', '0.50', 'ℹ️ About Us'),
    ('contact.html', f"{BASE_URL}/contact", 'yearly', '0.50', '📬 Contact Us'),
    ('links.html', f"{BASE_URL}/links", 'yearly', '0.40', '🔗 Official Links'),
    ('privacy-policy.html', f"{BASE_URL}/privacy-policy", 'yearly', '0.30', '🔒 Privacy Policy'),
]
for fname, def_url, freq, prio, display_title in core_defs:
    if os.path.exists(fname):
        title, canon = get_title_and_canonical(fname, def_url)
        core_entries.append({
            'file': fname, 'loc': def_url, 'title': display_title,
            'lastmod': get_lastmod(fname), 'changefreq': freq, 'priority': prio
        })

# 2. NOTES
if os.path.exists('Notes/index.html'):
    title, canon = get_title_and_canonical('Notes/index.html', f"{BASE_URL}/notes/")
    notes_entries.append({
        'file': 'Notes/index.html', 'loc': f"{BASE_URL}/notes/", 'title': 'All Study Notes & Resources Hub',
        'lastmod': get_lastmod('Notes/index.html'), 'changefreq': 'weekly', 'priority': '0.95'
    })
for f in sorted(os.listdir('Notes')):
    rel = f"Notes/{f}"
    if f.endswith('.html') and f != 'index.html' and rel not in EXCLUDE_EXACT:
        def_url = f"{BASE_URL}/notes/{f[:-5]}"
        title, canon = get_title_and_canonical(rel, def_url)
        loc = canon if canon and canon.startswith(BASE_URL) else def_url
        is_fy = 'first-year' in f or '31100' in f or '31101' in f
        prio = '0.95' if 'first-year' in f else ('0.90' if is_fy or 'k-scheme-question-banks' in f else '0.85')
        freq = 'weekly' if is_fy else 'monthly'
        notes_entries.append({
            'file': rel, 'loc': loc, 'title': clean_subject_title(f, title),
            'lastmod': get_lastmod(rel), 'changefreq': freq, 'priority': prio
        })

# 3. LAB MANUALS
if os.path.exists('Notes/Manual'):
    for f in sorted(os.listdir('Notes/Manual')):
        rel = f"Notes/Manual/{f}"
        if f.endswith('.html') and rel not in EXCLUDE_EXACT:
            def_url = f"{BASE_URL}/notes/manual/{f[:-5]}"
            title, canon = get_title_and_canonical(rel, def_url)
            loc = canon if canon and canon.startswith(BASE_URL) else def_url
            manual_entries.append({
                'file': rel, 'loc': loc, 'title': clean_subject_title(f, title),
                'lastmod': get_lastmod(rel), 'changefreq': 'monthly', 'priority': '0.80'
            })

# 4. PYQ
if os.path.exists('pyq/index.html'):
    title, canon = get_title_and_canonical('pyq/index.html', f"{BASE_URL}/pyq/")
    pyq_entries.append({
        'file': 'pyq/index.html', 'loc': f"{BASE_URL}/pyq/", 'title': 'All Question Papers (PYQ) Hub',
        'lastmod': get_lastmod('pyq/index.html'), 'changefreq': 'weekly', 'priority': '0.92'
    })
for f in sorted(os.listdir('pyq')):
    rel = f"pyq/{f}"
    if f.endswith('.html') and f != 'index.html' and rel not in EXCLUDE_EXACT:
        def_url = f"{BASE_URL}/pyq/{f}"
        title, canon = get_title_and_canonical(rel, def_url)
        loc = canon if canon and canon.startswith(BASE_URL) else def_url
        pyq_entries.append({
            'file': rel, 'loc': loc, 'title': clean_subject_title(f, title),
            'lastmod': get_lastmod(rel), 'changefreq': 'weekly', 'priority': '0.82'
        })

# 5. MODEL ANSWER
if os.path.exists('model-answer/index.html'):
    title, canon = get_title_and_canonical('model-answer/index.html', f"{BASE_URL}/model-answer/")
    model_answer_entries.append({
        'file': 'model-answer/index.html', 'loc': f"{BASE_URL}/model-answer/", 'title': 'All Model Answer Papers Hub',
        'lastmod': get_lastmod('model-answer/index.html'), 'changefreq': 'weekly', 'priority': '0.90'
    })
for f in sorted(os.listdir('model-answer')):
    rel = f"model-answer/{f}"
    if f.endswith('.html') and f != 'index.html' and rel not in EXCLUDE_EXACT:
        def_url = f"{BASE_URL}/model-answer/{f}"
        title, canon = get_title_and_canonical(rel, def_url)
        loc = canon if canon and canon.startswith(BASE_URL) else def_url
        model_answer_entries.append({
            'file': rel, 'loc': loc, 'title': clean_subject_title(f, title),
            'lastmod': get_lastmod(rel), 'changefreq': 'weekly', 'priority': '0.82'
        })

# 6 & 7. BRANCHES
if os.path.exists('Branches'):
    for f in sorted(os.listdir('Branches')):
        rel = f"Branches/{f}"
        if f.endswith('.html') and rel not in EXCLUDE_EXACT:
            slug = f[:-5].lower()
            def_url = f"{BASE_URL}/branches/{slug}"
            title, canon = get_title_and_canonical(rel, def_url)
            loc = canon if canon and canon.startswith(BASE_URL) else def_url
            
            is_subject = bool(re.match(r'^(?:elective-)?\d{6}-', f))
            if not is_subject and any(b in f.lower() for b in ['computer', 'civil', 'mechanical', 'electrical', 'information', 'ai-ml', 'etc', 'an6k']):
                prio = '0.90' if f in ['Computer.html', 'Civil.html', 'Mechanical-Engineering.html', 'Electrical-Engineering.html', 'Information-Technology.html', 'AI-ML.html', 'ETC-Engineering.html'] else '0.85'
                branches_hubs_entries.append({
                    'file': rel, 'loc': loc, 'title': clean_subject_title(f, title),
                    'lastmod': get_lastmod(rel), 'changefreq': 'monthly', 'priority': prio
                })
            else:
                branches_subject_entries.append({
                    'file': rel, 'loc': loc, 'title': clean_subject_title(f, title),
                    'lastmod': get_lastmod(rel), 'changefreq': 'monthly', 'priority': '0.80'
                })

# 8. BLOG
if os.path.exists('Blog/index.html'):
    title, canon = get_title_and_canonical('Blog/index.html', f"{BASE_URL}/blog/")
    blog_entries.append({
        'file': 'Blog/index.html', 'loc': f"{BASE_URL}/blog/", 'title': 'All Blog Posts & Exam Updates',
        'lastmod': get_lastmod('Blog/index.html'), 'changefreq': 'daily', 'priority': '0.95'
    })
for f in sorted(os.listdir('Blog')):
    rel = f"Blog/{f}"
    if f.endswith('.html') and f != 'index.html' and rel not in EXCLUDE_EXACT:
        slug = f[:-5].lower()
        def_url = f"{BASE_URL}/blog/{slug}"
        title, canon = get_title_and_canonical(rel, def_url)
        loc = canon if canon and canon.startswith(BASE_URL) else def_url
        prio = '0.92' if any(w in f.lower() for w in ['timetable', 'result', 'admission', 'calendar', 'dse']) else '0.85'
        freq = 'weekly' if any(w in f.lower() for w in ['timetable', 'result', '2026']) else 'monthly'
        blog_entries.append({
            'file': rel, 'loc': loc, 'title': clean_subject_title(f, title),
            'lastmod': get_lastmod(rel), 'changefreq': freq, 'priority': prio
        })

# 9. COLLEGE INFO
if os.path.exists('CollegeInfo/index.html'):
    title, canon = get_title_and_canonical('CollegeInfo/index.html', f"{BASE_URL}/collegeinfo/")
    college_entries.append({
        'file': 'CollegeInfo/index.html', 'loc': f"{BASE_URL}/collegeinfo/", 'title': 'Maharashtra Engineering Colleges Hub',
        'lastmod': get_lastmod('CollegeInfo/index.html'), 'changefreq': 'weekly', 'priority': '0.90'
    })
for f in sorted(os.listdir('CollegeInfo')):
    rel = f"CollegeInfo/{f}"
    if f.endswith('.html') and f != 'index.html' and rel not in EXCLUDE_EXACT:
        slug = f[:-5].lower()
        def_url = f"{BASE_URL}/collegeinfo/{slug}"
        title, canon = get_title_and_canonical(rel, def_url)
        loc = canon if canon and canon.startswith(BASE_URL) else def_url
        college_entries.append({
            'file': rel, 'loc': loc, 'title': clean_subject_title(f, title),
            'lastmod': get_lastmod(rel), 'changefreq': 'monthly', 'priority': '0.80'
        })

# 10. VIDEO COURSES
if os.path.exists('video-course/index.html'):
    title, canon = get_title_and_canonical('video-course/index.html', f"{BASE_URL}/video-course/")
    video_entries.append({
        'file': 'video-course/index.html', 'loc': f"{BASE_URL}/video-course/", 'title': 'All Video Courses Hub',
        'lastmod': get_lastmod('video-course/index.html'), 'changefreq': 'weekly', 'priority': '0.88'
    })
for f in sorted(os.listdir('video-course')):
    rel = f"video-course/{f}"
    if f.endswith('.html') and f != 'index.html' and rel not in EXCLUDE_EXACT:
        def_url = f"{BASE_URL}/video-course/{f}"
        title, canon = get_title_and_canonical(rel, def_url)
        loc = canon if canon and canon.startswith(BASE_URL) else def_url
        video_entries.append({
            'file': rel, 'loc': loc, 'title': clean_subject_title(f, title),
            'lastmod': get_lastmod(rel), 'changefreq': 'monthly', 'priority': '0.78'
        })

# 11. COURSES
if os.path.exists('Courses/index.html'):
    title, canon = get_title_and_canonical('Courses/index.html', f"{BASE_URL}/courses/")
    courses_entries.append({
        'file': 'Courses/index.html', 'loc': f"{BASE_URL}/courses/", 'title': 'Professional Courses Hub',
        'lastmod': get_lastmod('Courses/index.html'), 'changefreq': 'weekly', 'priority': '0.82'
    })
for f in sorted(os.listdir('Courses')):
    rel = f"Courses/{f}"
    if f.endswith('.html') and f != 'index.html' and rel not in EXCLUDE_EXACT:
        slug = f[:-5].lower()
        def_url = f"{BASE_URL}/courses/{slug}"
        title, canon = get_title_and_canonical(rel, def_url)
        loc = canon if canon and canon.startswith(BASE_URL) else def_url
        courses_entries.append({
            'file': rel, 'loc': loc, 'title': clean_subject_title(f, title),
            'lastmod': get_lastmod(rel), 'changefreq': 'monthly', 'priority': '0.75'
        })

# 12. JOBS
if os.path.exists('Jobs/index.html'):
    title, canon = get_title_and_canonical('Jobs/index.html', f"{BASE_URL}/jobs/")
    jobs_entries.append({
        'file': 'Jobs/index.html', 'loc': f"{BASE_URL}/jobs/", 'title': 'Diploma Engineering Jobs Portal',
        'lastmod': get_lastmod('Jobs/index.html'), 'changefreq': 'daily', 'priority': '0.85'
    })
for f in sorted(os.listdir('Jobs')):
    rel = f"Jobs/{f}"
    if f.endswith('.html') and f != 'index.html' and rel not in EXCLUDE_EXACT:
        slug = f[:-5].lower()
        def_url = f"{BASE_URL}/jobs/{slug}"
        title, canon = get_title_and_canonical(rel, def_url)
        loc = canon if canon and canon.startswith(BASE_URL) else def_url
        jobs_entries.append({
            'file': rel, 'loc': loc, 'title': clean_subject_title(f, title),
            'lastmod': get_lastmod(rel), 'changefreq': 'weekly', 'priority': '0.75'
        })

# 13. SCHEMES
if os.path.exists('scheme/index.html'):
    title, canon = get_title_and_canonical('scheme/index.html', f"{BASE_URL}/scheme/")
    schemes_entries.append({
        'file': 'scheme/index.html', 'loc': f"{BASE_URL}/scheme/", 'title': 'MSBTE Curriculum Schemes Directory',
        'lastmod': get_lastmod('scheme/index.html'), 'changefreq': 'weekly', 'priority': '0.85'
    })
for f in sorted(os.listdir('scheme')):
    rel = f"scheme/{f}"
    if f.endswith('.html') and f != 'index.html' and rel not in EXCLUDE_EXACT:
        def_url = f"{BASE_URL}/scheme/{f}"
        title, canon = get_title_and_canonical(rel, def_url)
        loc = canon if canon and canon.startswith(BASE_URL) else def_url
        schemes_entries.append({
            'file': rel, 'loc': loc, 'title': clean_subject_title(f, title),
            'lastmod': get_lastmod(rel), 'changefreq': 'monthly', 'priority': '0.80'
        })

# 14. MOCK TESTS
if os.path.exists('mock-tests/index.html'):
    title, canon = get_title_and_canonical('mock-tests/index.html', f"{BASE_URL}/mock-tests/")
    mock_entries.append({
        'file': 'mock-tests/index.html', 'loc': f"{BASE_URL}/mock-tests/", 'title': 'Online MSBTE Mock Tests',
        'lastmod': get_lastmod('mock-tests/index.html'), 'changefreq': 'weekly', 'priority': '0.80'
    })
for f in sorted(os.listdir('mock-tests')):
    rel = f"mock-tests/{f}"
    if f.endswith('.html') and f != 'index.html' and rel not in EXCLUDE_EXACT and f not in ['admin.html', 'profile.html']:
        def_url = f"{BASE_URL}/mock-tests/{f}"
        title, canon = get_title_and_canonical(rel, def_url)
        loc = canon if canon and canon.startswith(BASE_URL) else def_url
        mock_entries.append({
            'file': rel, 'loc': loc, 'title': clean_subject_title(f, title),
            'lastmod': get_lastmod(rel), 'changefreq': 'monthly', 'priority': '0.75'
        })

# 15. NEWS
if os.path.exists('News/index.html'):
    title, canon = get_title_and_canonical('News/index.html', f"{BASE_URL}/news/")
    news_entries.append({
        'file': 'News/index.html', 'loc': f"{BASE_URL}/news/", 'title': 'Latest MSBTE News & Notifications',
        'lastmod': get_lastmod('News/index.html'), 'changefreq': 'daily', 'priority': '0.90'
    })

section_list = [
    ('1. CORE & MAIN NAVIGATION PAGES (Folder: /)', core_entries),
    ('2. DIPLOMA STUDY NOTES & 1ST YEAR PORTAL (Folder: /Notes/)', notes_entries),
    ('3. LAB MANUALS & PRACTICAL SOLUTIONS (Folder: /Notes/Manual/)', manual_entries),
    ('4. PREVIOUS YEAR QUESTION PAPERS (Folder: /pyq/)', pyq_entries),
    ('5. MODEL ANSWER PAPERS (Folder: /model-answer/)', model_answer_entries),
    ('6. BRANCH HUBS & SEMESTERS (Folder: /Branches/)', branches_hubs_entries),
    ('7. BRANCH SUBJECT SYLLABUS & ELECTIVES (Folder: /Branches/)', branches_subject_entries),
    ('8. BLOG POSTS & EXAMINATION UPDATES (Folder: /Blog/)', blog_entries),
    ('9. COLLEGES & DISTRICT CUT-OFFS (Folder: /CollegeInfo/)', college_entries),
    ('10. VIDEO COURSES & LECTURES (Folder: /video-course/)', video_entries),
    ('11. COURSES & CERTIFICATIONS (Folder: /Courses/)', courses_entries),
    ('12. JOBS & CAREER OPPORTUNITIES (Folder: /Jobs/)', jobs_entries),
    ('13. DIPLOMA CURRICULUM SCHEMES (Folder: /scheme/)', schemes_entries),
    ('14. ONLINE MOCK TESTS (Folder: /mock-tests/)', mock_entries),
    ('15. ANNOUNCEMENTS & NEWS (Folder: /News/)', news_entries)
]

# Generate clean sitemap.xml
xml_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
]

total_entries = 0
for heading, entries in section_list:
    xml_lines.append('')
    xml_lines.append('  <!-- ' + '=' * 68 + ' -->')
    xml_lines.append(f'  <!-- {heading:<68} -->')
    xml_lines.append('  <!-- ' + '=' * 68 + ' -->')
    for e in entries:
        total_entries += 1
        xml_lines.append('  <url>')
        xml_lines.append(f'    <loc>{e["loc"]}</loc>')
        xml_lines.append(f'    <lastmod>{e["lastmod"]}</lastmod>')
        xml_lines.append(f'    <changefreq>{e["changefreq"]}</changefreq>')
        xml_lines.append(f'    <priority>{e["priority"]}</priority>')
        xml_lines.append('  </url>')

xml_lines.append('</urlset>')
xml_lines.append('')

sitemap_xml_content = '\n'.join(xml_lines)

with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(sitemap_xml_content)

print(f"Generated sitemap.xml with {total_entries} entries.")

# Validate XML
ET.fromstring(sitemap_xml_content)
print("sitemap.xml verified valid XML!")

# -------------------------------------------------------------
# BUILD MODERN, RICH sitemap.html
# -------------------------------------------------------------

def make_link_html(entry, is_hot=False, is_new=False):
    classes = ['sm-link']
    if is_hot: classes.append('hot')
    if is_new: classes.append('new')
    cls_str = ' '.join(classes)
    href = entry['file']
    # If file begins with folder, make sure leading slash
    if not href.startswith('/'):
        href = '/' + href
    return f'<a href="{href}" class="{cls_str}"><span class="dot"></span>{entry["title"]}</a>'

# Generate HTML sitemap
total_pages_count = total_entries
blog_count = len(blog_entries)
branch_count = len(branches_hubs_entries) + len(branches_subject_entries)
pyq_count = len(pyq_entries)
notes_count = len(notes_entries)
ma_count = len(model_answer_entries)
districts_count = len(college_entries) - 1

html_parts = []
html_parts.append(f'''<!DOCTYPE html>
<html lang="en">

<head>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-H5G5CCD95W"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag() {{ dataLayer.push(arguments); }}
        gtag('js', new Date());
        gtag('config', 'G-H5G5CCD95W');
    </script>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Sitemap — MSBTE Notes &amp; Info | All Pages &amp; Subjects</title>
    <meta name="description" content="Complete sitemap of MSBTE Notes &amp; Info ({total_pages_count}+ pages). Easily browse diploma notes, question papers (PYQ), model answers, branch syllabus, lab manuals, college cut-offs, and blog updates." />
    <meta name="robots" content="index, follow" />
    <link rel="canonical" href="https://msbtenotes-info.netlify.app/sitemap" />
    <meta property="og:title" content="Sitemap — MSBTE Notes &amp; Info" />
    <meta property="og:description" content="Full site index of MSBTE Notes &amp; Info. Find study notes, PYQ question papers, model answers, blogs, college cut-offs, and video courses." />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="https://msbtenotes-info.netlify.app/sitemap" />
    <meta property="og:image" content="https://msbtenotes-info.netlify.app/resourse/msbte-notes-og.png" />

    <!-- Favicon -->
    <link rel="apple-touch-icon" sizes="180x180" href="/resourse/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/resourse/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/resourse/favicon-16x16.png">
    <link rel="manifest" href="/resourse/site.webmanifest">
    <link rel="icon" href="/resourse/favicon.ico" type="image/x-icon">

    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
    <link href="https://api.fontshare.com/v2/css?f[]=clash-display@600&display=swap" rel="stylesheet">

    <style>
        :root {{
            --blue: #2563eb;
            --blue-dark: #1d4ed8;
            --blue-light: #dbeafe;
            --purple: #7c3aed;
            --green: #059669;
            --orange: #d97706;
            --pink: #db2777;
            --indigo: #4f46e5;
            --bg: #f8faff;
            --card-bg: #ffffff;
            --text: #1e293b;
            --muted: #64748b;
            --border: #e2e8f0;
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}

        body {{
            font-family: 'Inter', sans-serif;
            background: var(--bg);
            color: var(--text);
            background-image: radial-gradient(circle at 15% 15%, rgba(37,99,235,0.05) 0%, transparent 40%),
                              radial-gradient(circle at 85% 85%, rgba(124,58,237,0.05) 0%, transparent 40%);
            min-height: 100vh;
        }}

        h1, h2, h3, .font-display {{ font-family: 'Outfit', 'Clash Display', sans-serif; }}

        /* NAV */
        nav {{
            background: rgba(255,255,255,0.96);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 0;
            z-index: 100;
            padding: 0 1.5rem;
        }}
        .nav-inner {{
            max-width: 1240px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            height: 64px;
        }}
        .nav-logo {{
            display: flex;
            align-items: center;
            gap: 0.6rem;
            font-weight: 700;
            font-size: 1.15rem;
            color: var(--blue);
            text-decoration: none;
            font-family: 'Outfit', sans-serif;
        }}
        .nav-logo svg {{ width: 28px; height: 28px; }}
        .nav-back {{
            background: var(--blue);
            color: white;
            padding: 0.5rem 1.25rem;
            border-radius: 99px;
            font-weight: 600;
            font-size: 0.875rem;
            text-decoration: none;
            transition: background 0.2s;
        }}
        .nav-back:hover {{ background: var(--blue-dark); }}

        /* HEADER */
        .site-header {{
            text-align: center;
            padding: 3.5rem 1.5rem 2rem;
        }}
        .site-header h1 {{
            font-size: clamp(2rem, 5vw, 3.4rem);
            font-weight: 800;
            background: linear-gradient(135deg, var(--blue) 0%, var(--purple) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            line-height: 1.15;
        }}
        .site-header p {{
            margin-top: 0.75rem;
            color: var(--muted);
            font-size: 1.05rem;
            max-width: 640px;
            margin-left: auto;
            margin-right: auto;
        }}

        /* SEARCH */
        .search-wrap {{
            max-width: 580px;
            margin: 1.75rem auto 0;
            position: relative;
        }}
        .search-wrap input {{
            width: 100%;
            padding: 0.9rem 1.25rem 0.9rem 3.2rem;
            border: 2px solid var(--border);
            border-radius: 99px;
            font-size: 0.95rem;
            outline: none;
            background: white;
            transition: border-color 0.2s, box-shadow 0.2s;
        }}
        .search-wrap input:focus {{
            border-color: var(--blue);
            box-shadow: 0 0 0 4px rgba(37,99,235,0.12);
        }}
        .search-wrap .search-icon {{
            position: absolute;
            left: 1.15rem;
            top: 50%;
            transform: translateY(-50%);
            color: var(--muted);
        }}
        #search-count {{
            text-align: center;
            margin-top: 0.6rem;
            color: var(--muted);
            font-size: 0.875rem;
            min-height: 1.25rem;
        }}

        /* STATS BAR */
        .stats-bar {{
            display: flex;
            justify-content: center;
            gap: 1.5rem;
            flex-wrap: wrap;
            padding: 1.25rem 1.5rem;
            margin-bottom: 0.75rem;
        }}
        .stat-item {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.885rem;
            color: var(--muted);
            background: white;
            padding: 0.4rem 0.9rem;
            border-radius: 99px;
            border: 1px solid var(--border);
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        }}
        .stat-item strong {{ color: var(--text); font-weight: 700; }}

        /* CONTAINER */
        .sitemap-container {{
            max-width: 1240px;
            margin: 0 auto;
            padding: 0 1.5rem 5rem;
        }}

        /* SECTION */
        .sm-section {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 1.25rem;
            margin-bottom: 1.5rem;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.03);
            transition: box-shadow 0.2s;
        }}
        .sm-section:hover {{ box-shadow: 0 6px 20px rgba(0,0,0,0.06); }}

        .sm-section-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 1.25rem 1.5rem;
            cursor: pointer;
            user-select: none;
            background: linear-gradient(135deg, rgba(37,99,235,0.03), rgba(124,58,237,0.03));
            border-bottom: 1px solid transparent;
            transition: background 0.2s;
        }}
        .sm-section-header:hover {{ background: linear-gradient(135deg, rgba(37,99,235,0.06), rgba(124,58,237,0.05)); }}
        .sm-section-header.open {{ border-bottom-color: var(--border); }}

        .sm-section-title {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}
        .sm-icon {{
            width: 38px; height: 38px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            flex-shrink: 0;
        }}
        .sm-section-title h2 {{
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--text);
        }}
        .sm-badge {{
            background: var(--blue-light);
            color: var(--blue);
            font-size: 0.75rem;
            font-weight: 700;
            padding: 0.2rem 0.65rem;
            border-radius: 99px;
            white-space: nowrap;
        }}
        .sm-chevron {{
            color: var(--muted);
            transition: transform 0.3s;
            flex-shrink: 0;
        }}
        .sm-section-header.open .sm-chevron {{ transform: rotate(180deg); }}

        .sm-body {{
            padding: 1.25rem 1.5rem;
            display: none;
        }}
        .sm-body.open {{ display: block; }}

        /* SUBSECTION */
        .sm-sub {{
            margin-bottom: 1.5rem;
        }}
        .sm-sub:last-child {{ margin-bottom: 0; }}
        .sm-sub-title {{
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--muted);
            margin-bottom: 0.75rem;
            padding-bottom: 0.4rem;
            border-bottom: 1px solid var(--border);
        }}

        /* LINK GRID */
        .link-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
            gap: 0.45rem;
        }}
        .link-grid.cols-2 {{ grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); }}
        .link-grid.cols-3 {{ grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); }}
        .link-grid.cols-4 {{ grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); }}

        .sm-link {{
            display: flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.5rem 0.7rem;
            border-radius: 0.5rem;
            color: #374151;
            text-decoration: none;
            font-size: 0.865rem;
            transition: background 0.15s, color 0.15s;
            line-height: 1.35;
        }}
        .sm-link:hover {{
            background: var(--blue-light);
            color: var(--blue);
        }}
        .sm-link .dot {{
            width: 5px;
            height: 5px;
            border-radius: 50%;
            background: currentColor;
            opacity: 0.45;
            flex-shrink: 0;
        }}
        .sm-link.hot {{
            color: var(--blue);
            font-weight: 600;
        }}
        .sm-link.hot .dot {{ opacity: 1; }}
        .sm-link.new::after {{
            content: 'NEW';
            font-size: 0.65rem;
            font-weight: 800;
            color: var(--green);
            background: #d1fae5;
            padding: 0.1rem 0.4rem;
            border-radius: 4px;
            margin-left: auto;
            flex-shrink: 0;
        }}

        /* TABS */
        .branch-tabs {{
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
            margin-bottom: 1rem;
        }}
        .branch-tab {{
            padding: 0.45rem 1rem;
            border-radius: 99px;
            font-size: 0.82rem;
            font-weight: 600;
            cursor: pointer;
            border: 2px solid var(--border);
            background: white;
            color: var(--muted);
            transition: all 0.2s;
        }}
        .branch-tab.active, .branch-tab:hover {{
            border-color: var(--blue);
            background: var(--blue);
            color: white;
        }}

        .branch-panel {{ display: none; }}
        .branch-panel.active {{ display: block; }}

        .sm-link.hidden-search {{ display: none !important; }}
        .sm-section.all-hidden {{ opacity: 0.4; display: none; }}

        footer {{
            text-align: center;
            padding: 2.5rem 1.5rem;
            color: var(--muted);
            font-size: 0.875rem;
            border-top: 1px solid var(--border);
            background: white;
        }}
        footer a {{ color: var(--blue); text-decoration: none; }}

        @media (max-width: 640px) {{
            .link-grid {{ grid-template-columns: 1fr; }}
            .link-grid.cols-2 {{ grid-template-columns: 1fr; }}
            .stats-bar {{ gap: 0.5rem; }}
            .stat-item {{ font-size: 0.8rem; padding: 0.35rem 0.75rem; }}
        }}
    </style>
</head>

<body>

    <nav>
        <div class="nav-inner">
            <a href="/" class="nav-logo" aria-label="MSBTE Notes &amp; Info Home">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512" fill="currentColor">
                    <path d="M249.6 471.5c10.8 3.8 22.4-4.1 22.4-15.5V78.6c0-4.2-1.6-8.4-5-11C247.4 52 202.4 32 144 32C93.5 32 46.3 45.3 18.1 56.1C6.8 60.5 0 71.7 0 83.8V454.1c0 11.9 12.8 20.2 24.1 16.5C55.6 460.1 105.5 448 144 448c33.9 0 79 14 105.6 23.5zm76.8 0C353 462 398.1 448 432 448c38.5 0 88.4 12.1 119.9 22.6c11.3 3.8 24.1-4.6 24.1-16.5V83.8c0-12.1-6.8-23.3-18.1-27.6C529.7 45.3 482.5 32 432 32c-58.4 0-103.4 20-123 35.6c-3.3 2.6-5 6.8-5 11V456c0 11.4 11.7 19.3 22.4 15.5z"/>
                </svg>
                MSBTE Notes &amp; Info
            </a>
            <a href="/" class="nav-back">← Back to Home</a>
        </div>
    </nav>

    <header class="site-header">
        <h1>📍 Site Map &amp; Directory</h1>
        <p>Comprehensive directory of all {total_pages_count}+ pages across notes, previous year question papers (PYQ), model answers, branch syllabi, lab manuals, and exam updates.</p>
        <div class="search-wrap">
            <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
            </svg>
            <input type="text" id="sitemap-search" placeholder="Search pages, subjects, question papers, codes (e.g. 311302)..." autocomplete="off" />
        </div>
        <div id="search-count"></div>
    </header>

    <div class="stats-bar">
        <div class="stat-item">📄 <strong>{total_pages_count}</strong> Total Pages</div>
        <div class="stat-item">📝 <strong>{pyq_count}</strong> PYQ Collections</div>
        <div class="stat-item">📚 <strong>{notes_count}</strong> Notes &amp; Guides</div>
        <div class="stat-item">🎓 <strong>{branch_count}</strong> Branch Pages</div>
        <div class="stat-item">📰 <strong>{blog_count}</strong> Blog Posts</div>
        <div class="stat-item">✅ <strong>{ma_count}</strong> Model Answers</div>
        <div class="stat-item">🏫 <strong>{districts_count}</strong> Districts</div>
    </div>

    <main class="sitemap-container" id="sitemap-root">
''')

# 1. CORE SECTION
html_parts.append(f'''
        <!-- ════════ 1. CORE & MAIN PAGES ════════ -->
        <div class="sm-section">
            <div class="sm-section-header open" onclick="toggleSection(this)">
                <div class="sm-section-title">
                    <div class="sm-icon" style="background:#dbeafe;">🏠</div>
                    <h2>Core &amp; Main Navigation</h2>
                </div>
                <div style="display:flex;align-items:center;gap:0.75rem">
                    <span class="sm-badge">{len(core_entries)} pages</span>
                    <svg class="sm-chevron" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="m6 9 6 6 6-6"/></svg>
                </div>
            </div>
            <div class="sm-body open">
                <div class="link-grid cols-2">
''')
for e in core_entries:
    html_parts.append(f'                    <a href="{e["loc"].replace(BASE_URL, "") or "/"}" class="sm-link hot"><span class="dot"></span>{e["title"]}</a>\n')
html_parts.append('''                </div>
            </div>
        </div>
''')

# 2. STUDY NOTES
html_parts.append(f'''
        <!-- ════════ 2. STUDY NOTES & QUESTION BANKS ════════ -->
        <div class="sm-section">
            <div class="sm-section-header open" onclick="toggleSection(this)">
                <div class="sm-section-title">
                    <div class="sm-icon" style="background:#d1fae5;">📚</div>
                    <h2>Study Notes &amp; First Year Portal</h2>
                </div>
                <div style="display:flex;align-items:center;gap:0.75rem">
                    <span class="sm-badge">{len(notes_entries)} pages</span>
                    <svg class="sm-chevron" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="m6 9 6 6 6-6"/></svg>
                </div>
            </div>
            <div class="sm-body open">
                <div class="sm-sub">
                    <div class="sm-sub-title">📌 Key Hubs &amp; Portals</div>
                    <div class="link-grid cols-2">
                        <a href="/notes/" class="sm-link hot"><span class="dot"></span>All Study Notes Hub</a>
                        <a href="/Notes/msbte-first-year-diploma-notes.html" class="sm-link hot new"><span class="dot"></span>1st Year Diploma Portal (Sem 1 &amp; 2)</a>
                        <a href="/notes/msbte-k-scheme-question-banks.html" class="sm-link hot"><span class="dot"></span>K-Scheme All Question Banks</a>
                    </div>
                </div>

                <div class="sm-sub">
                    <div class="sm-sub-title">🛠️ Workshop Practical Guides</div>
                    <div class="link-grid cols-2">
                        <a href="/Notes/311002-engineering-workshop-practice.html" class="sm-link hot"><span class="dot"></span>Workshop Practice Guide (311002 — ME/Auto/Prod)</a>
                        <a href="/Notes/311005-engineering-workshop-practice.html" class="sm-link hot"><span class="dot"></span>Workshop Practice Guide (311005 — EE/EP)</a>
                        <a href="/Notes/311007-engineering-workshop-practice.html" class="sm-link hot"><span class="dot"></span>Workshop Practice Guide (311007 — EJ/ETC)</a>
                        <a href="/Notes/311010-civil-engineering-workshop.html" class="sm-link hot"><span class="dot"></span>Civil Engineering Workshop (311010 — CE)</a>
                    </div>
                </div>

                <div class="sm-sub">
                    <div class="sm-sub-title">📘 All Subject Notes &amp; Handbooks</div>
                    <div class="link-grid">
''')
for e in notes_entries:
    if e['file'] in ['Notes/index.html', 'Notes/msbte-first-year-diploma-notes.html']:
        continue
    html_parts.append(f'                        {make_link_html(e)}\n')
html_parts.append('''                    </div>
                </div>
            </div>
        </div>
''')

# 3. LAB MANUALS
html_parts.append(f'''
        <!-- ════════ 3. LAB MANUALS ════════ -->
        <div class="sm-section">
            <div class="sm-section-header" onclick="toggleSection(this)">
                <div class="sm-section-title">
                    <div class="sm-icon" style="background:#fef3c7;">🔬</div>
                    <h2>Lab Manuals &amp; Practical Solutions</h2>
                </div>
                <div style="display:flex;align-items:center;gap:0.75rem">
                    <span class="sm-badge">{len(manual_entries)} manuals</span>
                    <svg class="sm-chevron" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="m6 9 6 6 6-6"/></svg>
                </div>
            </div>
            <div class="sm-body">
                <div class="link-grid">
''')
for e in manual_entries:
    html_parts.append(f'                    {make_link_html(e)}\n')
html_parts.append('''                </div>
            </div>
        </div>
''')

# 4. PREVIOUS YEAR QUESTION PAPERS (PYQ)
html_parts.append(f'''
        <!-- ════════ 4. PREVIOUS YEAR QUESTION PAPERS (PYQ) ════════ -->
        <div class="sm-section">
            <div class="sm-section-header open" onclick="toggleSection(this)">
                <div class="sm-section-title">
                    <div class="sm-icon" style="background:#ede9fe;">📝</div>
                    <h2>Previous Year Question Papers (PYQ)</h2>
                </div>
                <div style="display:flex;align-items:center;gap:0.75rem">
                    <span class="sm-badge">{len(pyq_entries)} subjects</span>
                    <svg class="sm-chevron" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="m6 9 6 6 6-6"/></svg>
                </div>
            </div>
            <div class="sm-body open">
                <div class="sm-sub">
                    <div class="sm-sub-title">📌 Main Portal</div>
                    <div class="link-grid cols-2">
                        <a href="/pyq/" class="sm-link hot new"><span class="dot"></span>🎯 All MSBTE Question Papers Hub</a>
                    </div>
                </div>

                <div class="sm-sub">
                    <div class="sm-sub-title">📄 All Subject Question Papers</div>
                    <div class="link-grid">
''')
for e in pyq_entries:
    if e['file'] == 'pyq/index.html':
        continue
    html_parts.append(f'                        {make_link_html(e)}\n')
html_parts.append('''                    </div>
                </div>
            </div>
        </div>
''')

# 5. MODEL ANSWER PAPERS
html_parts.append(f'''
        <!-- ════════ 5. MODEL ANSWER PAPERS ════════ -->
        <div class="sm-section">
            <div class="sm-section-header open" onclick="toggleSection(this)">
                <div class="sm-section-title">
                    <div class="sm-icon" style="background:#ecfdf5;">✅</div>
                    <h2>MSBTE Model Answer Papers</h2>
                </div>
                <div style="display:flex;align-items:center;gap:0.75rem">
                    <span class="sm-badge">{len(model_answer_entries)} papers</span>
                    <svg class="sm-chevron" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="m6 9 6 6 6-6"/></svg>
                </div>
            </div>
            <div class="sm-body open">
                <div class="sm-sub">
                    <div class="sm-sub-title">📌 Main Portal</div>
                    <div class="link-grid cols-2">
                        <a href="/model-answer/" class="sm-link hot new"><span class="dot"></span>🏆 All Official Model Answer Papers Hub</a>
                    </div>
                </div>

                <div class="sm-sub">
                    <div class="sm-sub-title">📋 Subject Model Answers</div>
                    <div class="link-grid">
''')
for e in model_answer_entries:
    if e['file'] == 'model-answer/index.html':
        continue
    html_parts.append(f'                        {make_link_html(e, is_hot=True)}\n')
html_parts.append('''                    </div>
                </div>
            </div>
        </div>
''')

# 6. BRANCHES
html_parts.append(f'''
        <!-- ════════ 6. BRANCHES & SEMESTERS ════════ -->
        <div class="sm-section">
            <div class="sm-section-header open" onclick="toggleSection(this)">
                <div class="sm-section-title">
                    <div class="sm-icon" style="background:#e0e7ff;">🎓</div>
                    <h2>Branches — Semester-wise Pages &amp; Syllabus</h2>
                </div>
                <div style="display:flex;align-items:center;gap:0.75rem">
                    <span class="sm-badge">{branch_count} pages</span>
                    <svg class="sm-chevron" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="m6 9 6 6 6-6"/></svg>
                </div>
            </div>
            <div class="sm-body open">
                <div class="branch-tabs" id="branchTabs">
                    <button class="branch-tab active" onclick="switchBranch('computer', this)">💻 Computer</button>
                    <button class="branch-tab" onclick="switchBranch('it', this)">🖥️ IT</button>
                    <button class="branch-tab" onclick="switchBranch('aiml', this)">🤖 AI-ML</button>
                    <button class="branch-tab" onclick="switchBranch('civil', this)">🏗️ Civil</button>
                    <button class="branch-tab" onclick="switchBranch('mechanical', this)">⚙️ Mechanical</button>
                    <button class="branch-tab" onclick="switchBranch('electrical', this)">⚡ Electrical</button>
                    <button class="branch-tab" onclick="switchBranch('etc', this)">📡 ETC</button>
                    <button class="branch-tab" onclick="switchBranch('all_subjects', this)">📚 All Branch Subjects</button>
                </div>

                <!-- Computer -->
                <div class="branch-panel active" id="branch-computer">
                    <div class="sm-sub">
                        <div class="sm-sub-title">Computer Engineering (CO) — K-Scheme Semesters</div>
                        <div class="link-grid cols-3">
                            <a href="/branches/Computer.html" class="sm-link hot"><span class="dot"></span>Computer Branch Hub</a>
                            <a href="/branches/Computer-Semester-1.html" class="sm-link"><span class="dot"></span>Semester 1</a>
                            <a href="/branches/Computer-Semester-2.html" class="sm-link"><span class="dot"></span>Semester 2</a>
                            <a href="/branches/Computer-Semester-3.html" class="sm-link"><span class="dot"></span>Semester 3</a>
                            <a href="/branches/Computer-Semester-4.html" class="sm-link"><span class="dot"></span>Semester 4</a>
                            <a href="/branches/Computer-Semester-5.html" class="sm-link"><span class="dot"></span>Semester 5</a>
                            <a href="/branches/Computer-Semester-6.html" class="sm-link"><span class="dot"></span>Semester 6</a>
                        </div>
                    </div>
                    <div class="sm-sub">
                        <div class="sm-sub-title">Computer Engineering — I-Scheme Semesters</div>
                        <div class="link-grid cols-3">
                            <a href="/branches/Computer-I-Scheme.html" class="sm-link hot"><span class="dot"></span>Computer I-Scheme Hub</a>
                            <a href="/branches/Computer-I-Scheme-Semester-1.html" class="sm-link"><span class="dot"></span>I-Scheme Sem 1</a>
                            <a href="/branches/Computer-I-Scheme-Semester-2.html" class="sm-link"><span class="dot"></span>I-Scheme Sem 2</a>
                            <a href="/branches/Computer-I-Scheme-Semester-3.html" class="sm-link"><span class="dot"></span>I-Scheme Sem 3</a>
                            <a href="/branches/Computer-I-Scheme-Semester-4.html" class="sm-link"><span class="dot"></span>I-Scheme Sem 4</a>
                            <a href="/branches/Computer-I-Scheme-Semester-5.html" class="sm-link"><span class="dot"></span>I-Scheme Sem 5</a>
                        </div>
                    </div>
                </div>

                <!-- IT -->
                <div class="branch-panel" id="branch-it">
                    <div class="sm-sub">
                        <div class="sm-sub-title">Information Technology (IF) — K-Scheme Semesters</div>
                        <div class="link-grid cols-3">
                            <a href="/branches/Information-Technology.html" class="sm-link hot"><span class="dot"></span>IT Branch Hub</a>
                            <a href="/branches/Information-Technology-Semester-1.html" class="sm-link"><span class="dot"></span>Semester 1</a>
                            <a href="/branches/Information-Technology-Semester-2.html" class="sm-link"><span class="dot"></span>Semester 2</a>
                            <a href="/branches/Information-Technology-Semester-3.html" class="sm-link"><span class="dot"></span>Semester 3</a>
                            <a href="/branches/Information-Technology-Semester-4.html" class="sm-link"><span class="dot"></span>Semester 4</a>
                            <a href="/branches/Information-Technology-Semester-5.html" class="sm-link"><span class="dot"></span>Semester 5</a>
                            <a href="/branches/Information-Technology-Semester-6.html" class="sm-link"><span class="dot"></span>Semester 6</a>
                        </div>
                    </div>
                </div>

                <!-- AI-ML -->
                <div class="branch-panel" id="branch-aiml">
                    <div class="sm-sub">
                        <div class="sm-sub-title">Artificial Intelligence &amp; Machine Learning (AIML)</div>
                        <div class="link-grid cols-3">
                            <a href="/branches/AI-ML.html" class="sm-link hot"><span class="dot"></span>AI-ML Branch Hub</a>
                            <a href="/branches/AI-ML-Semester-1.html" class="sm-link"><span class="dot"></span>Semester 1</a>
                            <a href="/branches/AI-ML-Semester-2.html" class="sm-link"><span class="dot"></span>Semester 2</a>
                            <a href="/branches/AI-ML-Semester-3.html" class="sm-link"><span class="dot"></span>Semester 3</a>
                            <a href="/branches/AI-ML-Semester-4.html" class="sm-link"><span class="dot"></span>Semester 4</a>
                            <a href="/branches/AI-ML-Semester-5.html" class="sm-link"><span class="dot"></span>Semester 5</a>
                            <a href="/branches/AI-ML-Semester-6.html" class="sm-link"><span class="dot"></span>Semester 6</a>
                        </div>
                    </div>
                </div>

                <!-- Civil -->
                <div class="branch-panel" id="branch-civil">
                    <div class="sm-sub">
                        <div class="sm-sub-title">Civil Engineering (CE) — K-Scheme Semesters</div>
                        <div class="link-grid cols-3">
                            <a href="/branches/Civil.html" class="sm-link hot"><span class="dot"></span>Civil Branch Hub</a>
                            <a href="/branches/Civil-Semester-1.html" class="sm-link"><span class="dot"></span>Semester 1</a>
                            <a href="/branches/Civil-Semester-2.html" class="sm-link"><span class="dot"></span>Semester 2</a>
                            <a href="/branches/Civil-Semester-3.html" class="sm-link"><span class="dot"></span>Semester 3</a>
                            <a href="/branches/Civil-Semester-4.html" class="sm-link"><span class="dot"></span>Semester 4</a>
                            <a href="/branches/Civil-Semester-5.html" class="sm-link"><span class="dot"></span>Semester 5</a>
                            <a href="/branches/Civil-Semester-6.html" class="sm-link"><span class="dot"></span>Semester 6</a>
                        </div>
                    </div>
                </div>

                <!-- Mechanical -->
                <div class="branch-panel" id="branch-mechanical">
                    <div class="sm-sub">
                        <div class="sm-sub-title">Mechanical Engineering (ME) — K-Scheme Semesters</div>
                        <div class="link-grid cols-3">
                            <a href="/branches/Mechanical-Engineering.html" class="sm-link hot"><span class="dot"></span>Mechanical Branch Hub</a>
                            <a href="/branches/Mechanical-Engineering-Semester-1.html" class="sm-link"><span class="dot"></span>Semester 1</a>
                            <a href="/branches/Mechanical-Engineering-Semester-2.html" class="sm-link"><span class="dot"></span>Semester 2</a>
                            <a href="/branches/Mechanical-Engineering-Semester-3.html" class="sm-link"><span class="dot"></span>Semester 3</a>
                            <a href="/branches/Mechanical-Engineering-Semester-4.html" class="sm-link"><span class="dot"></span>Semester 4</a>
                            <a href="/branches/Mechanical-Engineering-Semester-5.html" class="sm-link"><span class="dot"></span>Semester 5</a>
                            <a href="/branches/Mechanical-Engineering-Semester-6.html" class="sm-link"><span class="dot"></span>Semester 6</a>
                        </div>
                    </div>
                </div>

                <!-- Electrical -->
                <div class="branch-panel" id="branch-electrical">
                    <div class="sm-sub">
                        <div class="sm-sub-title">Electrical Engineering (EE) — K-Scheme Semesters</div>
                        <div class="link-grid cols-3">
                            <a href="/branches/Electrical-Engineering.html" class="sm-link hot"><span class="dot"></span>Electrical Branch Hub</a>
                            <a href="/branches/Electrical-Engineering-Semester-1.html" class="sm-link"><span class="dot"></span>Semester 1</a>
                            <a href="/branches/Electrical-Engineering-Semester-2.html" class="sm-link"><span class="dot"></span>Semester 2</a>
                            <a href="/branches/Electrical-Engineering-Semester-3.html" class="sm-link"><span class="dot"></span>Semester 3</a>
                            <a href="/branches/Electrical-Engineering-Semester-4.html" class="sm-link"><span class="dot"></span>Semester 4</a>
                            <a href="/branches/Electrical-Engineering-Semester-5.html" class="sm-link"><span class="dot"></span>Semester 5</a>
                            <a href="/branches/Electrical-Engineering-Semester-6.html" class="sm-link"><span class="dot"></span>Semester 6</a>
                        </div>
                    </div>
                </div>

                <!-- ETC -->
                <div class="branch-panel" id="branch-etc">
                    <div class="sm-sub">
                        <div class="sm-sub-title">Electronics &amp; Telecommunication (EJ/ETC)</div>
                        <div class="link-grid cols-3">
                            <a href="/branches/ETC-Engineering.html" class="sm-link hot"><span class="dot"></span>ETC Branch Hub</a>
                            <a href="/branches/ETC-Engineering-Semester-1.html" class="sm-link"><span class="dot"></span>Semester 1</a>
                            <a href="/branches/ETC-Engineering-Semester-2.html" class="sm-link"><span class="dot"></span>Semester 2</a>
                            <a href="/branches/ETC-Engineering-Semester-3.html" class="sm-link"><span class="dot"></span>Semester 3</a>
                            <a href="/branches/ETC-Engineering-Semester-4.html" class="sm-link"><span class="dot"></span>Semester 4</a>
                            <a href="/branches/ETC-Engineering-Semester-5.html" class="sm-link"><span class="dot"></span>Semester 5</a>
                            <a href="/branches/ETC-Engineering-Semester-6.html" class="sm-link"><span class="dot"></span>Semester 6</a>
                        </div>
                    </div>
                </div>

                <!-- All Subjects -->
                <div class="branch-panel" id="branch-all_subjects">
                    <div class="sm-sub">
                        <div class="sm-sub-title">All Branch Subject Syllabus Guides &amp; Electives</div>
                        <div class="link-grid">
''')
for e in branches_subject_entries:
    html_parts.append(f'                            {make_link_html(e)}\n')
html_parts.append('''                        </div>
                    </div>
                </div>
            </div>
        </div>
''')

# 7. BLOG
html_parts.append(f'''
        <!-- ════════ 7. BLOG & ARTICLES ════════ -->
        <div class="sm-section">
            <div class="sm-section-header open" onclick="toggleSection(this)">
                <div class="sm-section-title">
                    <div class="sm-icon" style="background:#fce7f3;">📰</div>
                    <h2>Blog Posts &amp; MSBTE Examination News</h2>
                </div>
                <div style="display:flex;align-items:center;gap:0.75rem">
                    <span class="sm-badge">{blog_count} posts</span>
                    <svg class="sm-chevron" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="m6 9 6 6 6-6"/></svg>
                </div>
            </div>
            <div class="sm-body open">
                <div class="sm-sub">
                    <div class="sm-sub-title">📌 Blog Index</div>
                    <div class="link-grid cols-2">
                        <a href="/blog/" class="sm-link hot new"><span class="dot"></span>All Official Blog Posts &amp; Updates</a>
                    </div>
                </div>

                <div class="sm-sub">
                    <div class="sm-sub-title">📰 All Published Articles</div>
                    <div class="link-grid">
''')
for e in blog_entries:
    if e['file'] == 'Blog/index.html':
        continue
    is_hot = any(w in e['file'].lower() for w in ['timetable', 'result', '2026', 'admission', 'dse'])
    html_parts.append(f'                        {make_link_html(e, is_hot=is_hot)}\n')
html_parts.append('''                    </div>
                </div>
            </div>
        </div>
''')

# 8. COLLEGES
html_parts.append(f'''
        <!-- ════════ 8. COLLEGES BY DISTRICT ════════ -->
        <div class="sm-section">
            <div class="sm-section-header" onclick="toggleSection(this)">
                <div class="sm-section-title">
                    <div class="sm-icon" style="background:#d1fae5;">🏫</div>
                    <h2>Colleges &amp; Cut-offs by District</h2>
                </div>
                <div style="display:flex;align-items:center;gap:0.75rem">
                    <span class="sm-badge">{len(college_entries)} pages</span>
                    <svg class="sm-chevron" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="m6 9 6 6 6-6"/></svg>
                </div>
            </div>
            <div class="sm-body">
                <div class="sm-sub">
                    <div class="sm-sub-title">Hub</div>
                    <div class="link-grid cols-2">
                        <a href="/collegeinfo/" class="sm-link hot"><span class="dot"></span>🏛️ All Maharashtra Colleges Hub</a>
                    </div>
                </div>
                <div class="sm-sub">
                    <div class="sm-sub-title">Maharashtra Districts</div>
                    <div class="link-grid cols-4">
''')
for e in college_entries:
    if e['file'] == 'CollegeInfo/index.html':
        continue
    html_parts.append(f'                        {make_link_html(e)}\n')
html_parts.append('''                    </div>
                </div>
            </div>
        </div>
''')

# 9. VIDEO COURSES
html_parts.append(f'''
        <!-- ════════ 9. VIDEO COURSES ════════ -->
        <div class="sm-section">
            <div class="sm-section-header" onclick="toggleSection(this)">
                <div class="sm-section-title">
                    <div class="sm-icon" style="background:#fee2e2;">🎥</div>
                    <h2>Video Courses &amp; Lectures</h2>
                </div>
                <div style="display:flex;align-items:center;gap:0.75rem">
                    <span class="sm-badge">{len(video_entries)} courses</span>
                    <svg class="sm-chevron" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="m6 9 6 6 6-6"/></svg>
                </div>
            </div>
            <div class="sm-body">
                <div class="link-grid cols-2">
''')
for e in video_entries:
    html_parts.append(f'                    {make_link_html(e)}\n')
html_parts.append('''                </div>
            </div>
        </div>
''')

# 10. SCHEMES & CURRICULUM
html_parts.append(f'''
        <!-- ════════ 10. CURRICULUM SCHEMES ════════ -->
        <div class="sm-section">
            <div class="sm-section-header" onclick="toggleSection(this)">
                <div class="sm-section-title">
                    <div class="sm-icon" style="background:#e0e7ff;">📋</div>
                    <h2>MSBTE Curriculum Schemes</h2>
                </div>
                <div style="display:flex;align-items:center;gap:0.75rem">
                    <span class="sm-badge">{len(schemes_entries)} pages</span>
                    <svg class="sm-chevron" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="m6 9 6 6 6-6"/></svg>
                </div>
            </div>
            <div class="sm-body">
                <div class="link-grid cols-2">
''')
for e in schemes_entries:
    html_parts.append(f'                    {make_link_html(e)}\n')
html_parts.append('''                </div>
            </div>
        </div>
''')

# 11. CAREER, JOBS, COURSES & MOCK TESTS
html_parts.append(f'''
        <!-- ════════ 11. CAREER, JOBS, COURSES & TESTS ════════ -->
        <div class="sm-section">
            <div class="sm-section-header" onclick="toggleSection(this)">
                <div class="sm-section-title">
                    <div class="sm-icon" style="background:#fef9c3;">💼</div>
                    <h2>Career, Jobs, Courses &amp; Mock Tests</h2>
                </div>
                <div style="display:flex;align-items:center;gap:0.75rem">
                    <span class="sm-badge">{len(jobs_entries) + len(courses_entries) + len(mock_entries) + len(news_entries)} pages</span>
                    <svg class="sm-chevron" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="m6 9 6 6 6-6"/></svg>
                </div>
            </div>
            <div class="sm-body">
                <div class="link-grid cols-2">
''')
for e in jobs_entries:
    html_parts.append(f'                    {make_link_html(e)}\n')
for e in courses_entries:
    html_parts.append(f'                    {make_link_html(e)}\n')
for e in mock_entries:
    html_parts.append(f'                    {make_link_html(e)}\n')
for e in news_entries:
    html_parts.append(f'                    {make_link_html(e)}\n')
html_parts.append('''                </div>
            </div>
        </div>

    </main>

    <footer>
        <p>© 2026 MSBTE Notes &amp; Info — <a href="/">Home</a> · <a href="/notes/">Notes</a> · <a href="/pyq/">PYQ</a> · <a href="/model-answer/">Model Answer</a> · <a href="/about.html">About</a> · <a href="/contact.html">Contact</a> · <a href="/privacy-policy.html">Privacy</a></p>
        <p style="margin-top:0.5rem;">Sitemap updated: November 2026 • 600+ Verified Pages</p>
    </footer>

    <script src="/whatsapp-popup.js" defer></script>

    <script>
        /* ── Toggle sections ── */
        function toggleSection(header) {
            header.classList.toggle('open');
            const body = header.nextElementSibling;
            body.classList.toggle('open');
        }

        /* ── Branch tabs ── */
        function switchBranch(branchId, tabEl) {
            document.querySelectorAll('.branch-tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.branch-panel').forEach(p => p.classList.remove('active'));
            tabEl.classList.add('active');
            const target = document.getElementById('branch-' + branchId);
            if (target) target.classList.add('active');
        }

        /* ── Sitemap search ── */
        const searchInput = document.getElementById('sitemap-search');
        const countEl = document.getElementById('search-count');

        searchInput.addEventListener('input', () => {
            const q = searchInput.value.trim().toLowerCase();
            if (!q) {
                document.querySelectorAll('.sm-link').forEach(l => l.classList.remove('hidden-search'));
                document.querySelectorAll('.sm-section').forEach(s => s.classList.remove('all-hidden'));
                countEl.textContent = '';
                return;
            }

            // Open all sections when searching
            document.querySelectorAll('.sm-section-header').forEach(h => {
                h.classList.add('open');
                if (h.nextElementSibling) h.nextElementSibling.classList.add('open');
            });
            document.querySelectorAll('.branch-panel').forEach(p => p.classList.add('active'));

            let visible = 0;
            document.querySelectorAll('.sm-link').forEach(link => {
                const text = (link.textContent || '').toLowerCase();
                const href = (link.getAttribute('href') || '').toLowerCase();
                const match = text.includes(q) || href.includes(q);
                link.classList.toggle('hidden-search', !match);
                if (match) visible++;
            });

            document.querySelectorAll('.sm-section').forEach(section => {
                const anyVisible = [...section.querySelectorAll('.sm-link')].some(l => !l.classList.contains('hidden-search'));
                section.classList.toggle('all-hidden', !anyVisible);
            });

            countEl.textContent = visible > 0 ? `Found ${visible} matching page${visible !== 1 ? 's' : ''}` : 'No matching pages found';
        });
    </script>
</body>
</html>
''')

sitemap_html_content = ''.join(html_parts)

with open('sitemap.html', 'w', encoding='utf-8') as f:
    f.write(sitemap_html_content)

print(f"Successfully generated sitemap.html with all {total_pages_count} pages and interactive sections!")
