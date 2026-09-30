#!/usr/bin/env python3
"""SEO fix for msbtenotes-info. Run from repo root:  python seo_fix.py [--dry]
1. Canonical / og:url / JSON-LD / sitemap URLs -> lowercase, no .html (the URLs Netlify actually serves with 200)
2. Sitemap: drop URLs whose files don't exist
3. Titles: title-case ALL-CAPS subject names, remove empty "()" , cap at 60 chars (Branches + Notes subject pages)
"""
import re, sys, os, glob
BASE = 'https://msbtenotes-info.netlify.app'
DRY = '--dry' in sys.argv
FOLD = r'(?:Branches|Notes|Blog|CollegeInfo|Jobs|News|Courses|MCU)'
# Root-level pages to normalise in sitemap (Netlify redirects /foo.html -> /foo)
ROOT_HTML = re.compile(
    re.escape(BASE) + r'/((?:services|videos|internships|forum|sitemap|links|privacy(?:-policy)?))\.html'
)
URL = re.compile(re.escape(BASE) + r'/(' + FOLD + r')((?:/[^"\x27\s<>)\]]*)?)', re.I)


def norm_url(m):
    full = m.group(0)
    path = full[len(BASE):]
    if path.lower().endswith('.html'):
        return BASE + path[:-5].lower()
    if path.endswith('/') or '.' not in path.rsplit('/', 1)[-1]:
        return BASE + path.lower()
    return full                       # js/png/svg/pdf resources untouched

SMALL = {'and','of','in','for','to','the','with','using','on','a','an','&'}
KEEP = {'AI','ML','IT','ICT','IoT','PLC','VLSI','RCC','HVAC','DBMS','OOP','C++','UI','UX','3D','IOT','NLP','CAD','CNC','PWP','JPR','DCN','MIC','PHP','SQL','CSS','HTML','AC','DC'}
def tcase(s):
    out = []
    for i, w in enumerate(s.split()):
        u = w.upper()
        if u in KEEP or u.strip('()') in KEEP: out.append(u if u != 'IOT' else 'IoT')
        elif w.lower() in SMALL and i: out.append(w.lower())
        elif w.isupper() or w.islower(): out.append(w.capitalize())
        else: out.append(w)
    return ' '.join(out)

def fit(cands):
    for c in cands:
        if len(c) <= 60: return c
    return cands[-1][:60].rstrip()

def esc(s): return s.replace('&', '&amp;') if '&amp;' not in s and False else s

EMPTY = re.compile(r'\s*\(\s*\)')
def _c(x): return EMPTY.sub('', x).replace(', ,', ',')
def clean_text(txt):
    """Remove empty "()" only in visible text / meta / JSON-LD strings, never in <script> code."""
    txt = re.sub(r'(content=")([^"]*)(")', lambda m: m.group(1) + _c(m.group(2)) + m.group(3), txt)
    txt = re.sub(r'("(?:name|text|description|headline)":\s*")([^"]*)(")', lambda m: m.group(1) + _c(m.group(2)) + m.group(3), txt)
    txt = re.sub(r'(<(title|h1|h2|h3|p)\b[^>]*>)(.*?)(</\2>)', lambda m: m.group(1) + _c(m.group(3)) + m.group(4), txt, flags=re.S)
    return txt

def retitle(txt, path):
    m = re.search(r'<title>(.*?)</title>', txt, re.S)
    if not m: return txt, None
    old = m.group(1).strip(); new = None
    if path.startswith('Branches/'):
        # Actual format: "SUBJECT NAME (CODE) K-Scheme Syllabus & Notes PDF | MSBTE Notes & Info"
        # Also handles:  "Elective: CODE-SUBJECT NAME () K-Scheme ..."
        SUFFIX = r'(?:\s*K-Scheme Syllabus &(?:amp;)? Notes PDF)?(?:\s*\|.*)?$'
        r = re.match(r'^(?:Elective:\s*)?(\d{6,7})\s*-?\s*(.+?)\s*\(\s*(\d{6,7})?\s*\)' + SUFFIX, old) \
         or re.match(r'^([A-Z0-9].+?)\s*\((\d{6,7})\)' + SUFFIX, old)
        if r:
            if r.lastindex >= 3:
                # first pattern: groups are (leading_code, name, inline_code)
                pre, name, code = r.group(1), r.group(2), r.group(3) or r.group(1)
            else:
                # second pattern: groups are (name, code)
                name, code = r.group(1), r.group(2); pre = ''
            if not code: code = re.search(r'(\d{6,7})', os.path.basename(path)).group(1) if re.search(r'\d{6,7}', os.path.basename(path)) else ''
            name = re.sub(r'^\d{6,7}\s*-?\s*', '', name); n = tcase(name); c = f' ({code})' if code else ''
            new = fit([f'{n}{c} Syllabus & Notes PDF | MSBTE K-Scheme', f'{n}{c} Syllabus & Notes | MSBTE K-Scheme',
                       f'{n}{c} Syllabus & Notes | MSBTE', f'{n}{c} Notes & Syllabus', f'{n} Notes & Syllabus'])
    elif path.startswith('Notes/'):
        r = re.match(r'^(\d{6,7})\s*-\s*(.+?)\s+Question Banks & PDFs - MSBTE K-Scheme(?:\s*\|.*)?$', old)
        if r:
            code, n = r.group(1), r.group(2)
            new = fit([f'{n} ({code}) Question Bank & Notes PDF | MSBTE', f'{n} ({code}) Question Bank PDF | MSBTE',
                       f'{n} ({code}) Question Bank | MSBTE', f'{n} Question Bank PDF | MSBTE', f'{n} Question Bank | MSBTE'])
    elif path.startswith('Branches/') and re.search(r'Semester \d', old):
        # Semester index pages: "AI & Machine Learning Semester 1 Syllabus & Notes | MSBTE" -> shorten
        r = re.match(r'^(.+?)\s+Semester\s+(\d)\s+Syllabus.*$', old)
        if r:
            branch, sem = r.group(1).strip(), r.group(2)
            new = fit([f'{branch} Sem {sem} Notes | MSBTE K-Scheme',
                       f'{branch} Sem {sem} | MSBTE K-Scheme',
                       f'{branch} Sem {sem} | MSBTE'])
    if not new or new == old: return txt, None
    txt = txt.replace(m.group(0), f'<title>{new}</title>', 1)
    txt = re.sub(r'(<meta property="og:title" content=")[^"]*"', lambda x: f'{x.group(1)}{new}"', txt, count=1)
    txt = re.sub(r'(<meta name="twitter:title" content=")[^"]*"', lambda x: f'{x.group(1)}{new}"', txt, count=1)
    txt = clean_text(txt)
    return txt, new

stats = dict(files=0, url_changed=0, titles=0)
for f in glob.glob('**/*.html', recursive=True):
    fp = f.replace('\\', '/')   # normalise for Windows
    if any(fp.startswith(p) for p in ('.git/', 'brain/', 'python/', 'scripts/')): continue
    t = open(f, encoding='utf-8', newline='').read(); o = t
    before = t
    t = URL.sub(norm_url, t)
    if t != before: stats['url_changed'] += 1
    t, nt = retitle(t, fp)
    if nt: stats['titles'] += 1
    if t != o:
        stats['files'] += 1
        if not DRY: open(f, 'w', encoding='utf-8', newline='').write(t)

# sitemap
s = open('sitemap.xml', encoding='utf-8', newline='').read(); o = s
s = URL.sub(norm_url, s)
# Also normalise root-level .html pages in sitemap
s = ROOT_HTML.sub(lambda m: BASE + '/' + m.group(1), s)
def exists(loc):
    p = loc[len(BASE):].strip('/')
    if not p: return True
    low = {x.replace('\\', '/').lower() for x in glob.glob('**/*', recursive=True)}
    return any(c.lower() in low for c in (p, p + '.html', p + '/index.html'))
low = {x.replace('\\', '/').lower() for x in glob.glob('**/*', recursive=True)}
def keep(m):
    loc = re.search(r'<loc>(.*?)</loc>', m.group(0)).group(1)
    p = loc[len(BASE):].strip('/').lower()
    return m.group(0) if (not p or p in low or p + '.html' in low or p + '/index.html' in low) else ''
s = re.sub(r'\s*<url>.*?</url>', lambda m: ('\n  ' + keep(m).strip()) if keep(m) else '', s, flags=re.S)
locs = re.findall(r'<loc>(.*?)</loc>', s); dup = len(locs) - len(set(locs))
print('sitemap urls now:', len(locs), 'duplicates:', dup)
if not DRY: open('sitemap.xml', 'w', encoding='utf-8', newline='').write(s)
print(stats)
