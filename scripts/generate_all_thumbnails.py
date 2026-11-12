"""
Batch generate modern, high-converting SVG thumbnails and convert them to 1200x630 PNGs
for all Branches, Semesters, and Subjects in Branches/media/.
Matches the reference card design: deep gradients, luminous glow, modern typography,
vibrant feature pills, and layered document card mockup.
"""

import os
import glob
import re
import csv
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_DIR = os.path.join(BASE_DIR, 'Branches', 'media')
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
SUBJECTS_CSV = os.path.join(BASE_DIR, 'data', 'msbte_k_scheme_subjects.csv')

# Discipline visual palettes
THEMES = {
    'computer': {
        'bg1': '#0a192f',
        'bg2': '#0f274a',
        'bg3': '#1e40af',
        'accent': '#38bdf8',
        'glow': '#3b82f6',
        'card_bar': '#2563eb',
        'label': 'COMPUTER ENGINEERING'
    },
    'it': {
        'bg1': '#042f2e',
        'bg2': '#0f4f4a',
        'bg3': '#0d9488',
        'accent': '#2dd4bf',
        'glow': '#14b8a6',
        'card_bar': '#0d9488',
        'label': 'INFORMATION TECHNOLOGY'
    },
    'ai-ml': {
        'bg1': '#190a2e',
        'bg2': '#3b0764',
        'bg3': '#6b21a8',
        'accent': '#c084fc',
        'glow': '#a855f7',
        'card_bar': '#7c3aed',
        'label': 'AI & MACHINE LEARNING'
    },
    'civil': {
        'bg1': '#0b192c',
        'bg2': '#0c4a6e',
        'bg3': '#0284c7',
        'accent': '#38bdf8',
        'glow': '#0284c7',
        'card_bar': '#0284c7',
        'label': 'CIVIL ENGINEERING'
    },
    'electrical': {
        'bg1': '#0f172a',
        'bg2': '#422006',
        'bg3': '#854d0e',
        'accent': '#facc15',
        'glow': '#eab308',
        'card_bar': '#d97706',
        'label': 'ELECTRICAL ENGINEERING'
    },
    'etc': {
        'bg1': '#1f102e',
        'bg2': '#4c0519',
        'bg3': '#9f1239',
        'accent': '#fb7185',
        'glow': '#f43f5e',
        'card_bar': '#e11d48',
        'label': 'ELECTRONICS & TELECOMM'
    },
    'mechanical': {
        'bg1': '#1c1917',
        'bg2': '#431407',
        'bg3': '#9a3412',
        'accent': '#fb923c',
        'glow': '#f97316',
        'card_bar': '#ea580c',
        'label': 'MECHANICAL ENGINEERING'
    },
    'default': {
        'bg1': '#0a192f',
        'bg2': '#11254e',
        'bg3': '#1e40af',
        'accent': '#60a5fa',
        'glow': '#3b82f6',
        'card_bar': '#2563eb',
        'label': 'MSBTE K-SCHEME 2026'
    }
}

BRANCH_THEME_MAP = {
    'computer': 'computer',
    'information-technology': 'it',
    'ai-ml': 'ai-ml',
    'civil': 'civil',
    'electrical-engineering': 'electrical',
    'etc-engineering': 'etc',
    'mechanical-engineering': 'mechanical',
    'an6k': 'ai-ml',
    'ee6k': 'electrical'
}

# 1. Load subjects metadata
subjects_meta = {}
if os.path.exists(SUBJECTS_CSV):
    with open(SUBJECTS_CSV, encoding='utf-8') as f:
        for r in csv.DictReader(f):
            c = r.get('Subject Code', '').strip()
            if c.isdigit():
                if c not in subjects_meta:
                    subjects_meta[c] = {
                        'name': r.get('Subject Name', '').strip(),
                        'branches': set(),
                        'semesters': set()
                    }
                b_name = r.get('Branch', '').strip()
                if b_name:
                    subjects_meta[c]['branches'].add(b_name)
                s_name = r.get('Semester', '').strip()
                if 'first' in s_name.lower(): subjects_meta[c]['semesters'].add('Semester 1')
                elif 'second' in s_name.lower(): subjects_meta[c]['semesters'].add('Semester 2')
                elif 'third' in s_name.lower(): subjects_meta[c]['semesters'].add('Semester 3')
                elif 'fourth' in s_name.lower(): subjects_meta[c]['semesters'].add('Semester 4')
                elif 'fifth' in s_name.lower(): subjects_meta[c]['semesters'].add('Semester 5')
                elif 'sixth' in s_name.lower(): subjects_meta[c]['semesters'].add('Semester 6')

def detect_theme(filename, branches_set=None):
    fn = filename.lower()
    for k, t in BRANCH_THEME_MAP.items():
        if k in fn:
            return THEMES[t]
    if branches_set:
        b_str = ' '.join(branches_set).lower()
        if 'computer' in b_str: return THEMES['computer']
        if 'information' in b_str: return THEMES['it']
        if 'artificial' in b_str or 'ai' in b_str: return THEMES['ai-ml']
        if 'civil' in b_str: return THEMES['civil']
        if 'electrical' in b_str: return THEMES['electrical']
        if 'telecommunication' in b_str or 'electronics' in b_str: return THEMES['etc']
        if 'mechanical' in b_str: return THEMES['mechanical']
    return THEMES['default']

def escape_xml(s):
    return (s.replace('&', '&amp;')
             .replace('<', '&lt;')
             .replace('>', '&gt;')
             .replace('"', '&quot;')
             .replace("'", '&apos;'))

def wrap_text(text, max_chars=28):
    words = text.split()
    if not words:
        return [""]
    lines = []
    cur = []
    cur_len = 0
    for w in words:
        add_len = len(w) + (1 if cur else 0)
        if cur_len + add_len <= max_chars:
            cur.append(w)
            cur_len += add_len
        else:
            if cur:
                lines.append(" ".join(cur))
            cur = [w]
            cur_len = len(w)
    if cur:
        lines.append(" ".join(cur))
    return lines

def generate_svg_markup(title, code=None, subtitle=None, sem_label=None, theme=None):
    if not theme:
        theme = THEMES['default']
        
    # Text wrapping and dynamic typography calculation
    lines = wrap_text(title, max_chars=28)
    line_count = len(lines)
    
    if line_count == 1:
        font_size = 50
        y_lines = [88]
        sub_y = 142
        tagline_y = 180
        pills_y1 = 236
        pills_y2 = 296
    elif line_count == 2:
        font_size = 42
        y_lines = [78, 126]
        sub_y = 172
        tagline_y = 208
        pills_y1 = 256
        pills_y2 = 314
    else:
        # 3 lines
        lines = lines[:3]
        font_size = 36
        y_lines = [68, 110, 152]
        sub_y = 194
        tagline_y = 228
        pills_y1 = 274
        pills_y2 = 330

    # Pill tag text
    if code and sem_label:
        pill_text = f"COURSE CODE: {code} • {sem_label.upper()}"
    elif code:
        pill_text = f"COURSE CODE: {code} • K-SCHEME"
    elif sem_label and 'Semester' in sem_label:
        pill_text = f"DIPLOMA IN ENGINEERING • {sem_label.upper()}"
    elif sem_label:
        pill_text = f"DIPLOMA CURRICULUM • {sem_label.upper()}"
    else:
        pill_text = "DIPLOMA IN ENGINEERING • ALL SEMESTERS"

    if not subtitle:
        subtitle = "Full K-Scheme Curriculum, Notes & Solved Papers"
    
    tagline = "All MSBTE resources in one place. Pick your branch. Find everything."

    # Pill width calculation
    pill_w = max(240, min(500, len(pill_text) * 10 + 36))

    svg = f'''<svg width="1200" height="630" viewBox="0 0 1200 630" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{theme['bg1']}" />
      <stop offset="45%" stop-color="{theme['bg2']}" />
      <stop offset="100%" stop-color="{theme['bg3']}" />
    </linearGradient>
    <radialGradient id="bgGlow" cx="80%" cy="20%" r="60%">
      <stop offset="0%" stop-color="{theme['glow']}" stop-opacity="0.38" />
      <stop offset="100%" stop-color="{theme['glow']}" stop-opacity="0" />
    </radialGradient>
    <radialGradient id="cardGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{theme['accent']}" stop-opacity="0.32" />
      <stop offset="100%" stop-color="{theme['accent']}" stop-opacity="0" />
    </radialGradient>
    <filter id="dropShadow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="14" stdDeviation="18" flood-color="#000000" flood-opacity="0.32" />
    </filter>
  </defs>

  <!-- Background Base -->
  <rect width="1200" height="630" fill="url(#bgGrad)" />
  <rect width="1200" height="630" fill="url(#bgGlow)" />

  <!-- Top Left Pill Badge -->
  <g transform="translate(70, 54)">
    <rect width="270" height="36" rx="18" fill="rgba(255, 255, 255, 0.12)" stroke="rgba(255, 255, 255, 0.2)" stroke-width="1" />
    <text x="135" y="23" font-family="'Segoe UI', Inter, -apple-system, sans-serif" font-size="12" font-weight="700" fill="#ffffff" letter-spacing="0.08em" text-anchor="middle">MSBTE NOTES &amp; INFORMATION</text>
  </g>

  <!-- Main Hero Titles -->
  <g transform="translate(70, 140)">
    <!-- Metadata Pill Tag -->
    <rect width="{pill_w}" height="32" rx="8" fill="rgba(255, 255, 255, 0.1)" stroke="{theme['accent']}" stroke-width="1.2" />
    <text x="{pill_w // 2}" y="21" font-family="'Segoe UI', Inter, monospace" font-size="12" font-weight="700" fill="{theme['accent']}" letter-spacing="0.07em" text-anchor="middle">{escape_xml(pill_text)}</text>'''

    # Title Lines
    for idx, l_text in enumerate(lines):
        y_pos = y_lines[idx]
        svg += f'''
    <!-- Title Line {idx + 1} -->
    <text x="0" y="{y_pos}" font-family="'Segoe UI', Inter, -apple-system, sans-serif" font-size="{font_size}" font-weight="800" fill="#ffffff" letter-spacing="-0.02em">
      {escape_xml(l_text)}
    </text>'''

    # Subtitle and Tagline
    svg += f'''
    <!-- Subtitle -->
    <text x="0" y="{sub_y}" font-family="'Segoe UI', Inter, -apple-system, sans-serif" font-size="23" font-weight="600" fill="#e2e8f0">
      {escape_xml(subtitle)}
    </text>

    <!-- Tertiary Tagline -->
    <text x="0" y="{tagline_y}" font-family="'Segoe UI', Inter, -apple-system, sans-serif" font-size="16" font-weight="400" fill="#94a3b8">
      {escape_xml(tagline)}
    </text>

    <!-- Bottom Feature Pills Row 1 -->
    <g transform="translate(0, {pills_y1})">
      <!-- Notes (Yellow) -->
      <g transform="translate(0, 0)">
        <rect width="125" height="42" rx="21" fill="#facc15" />
        <text x="62" y="26" font-family="'Segoe UI', Inter, sans-serif" font-size="14" font-weight="700" fill="#0f172a" text-anchor="middle">Notes</text>
      </g>
      <!-- PYQ (Mint Green) -->
      <g transform="translate(138, 0)">
        <rect width="105" height="42" rx="21" fill="#34d399" />
        <text x="52" y="26" font-family="'Segoe UI', Inter, sans-serif" font-size="14" font-weight="700" fill="#064e3b" text-anchor="middle">PYQ</text>
      </g>
      <!-- Model Answers (Coral) -->
      <g transform="translate(256, 0)">
        <rect width="185" height="42" rx="21" fill="#f87171" />
        <text x="92" y="26" font-family="'Segoe UI', Inter, sans-serif" font-size="14" font-weight="700" fill="#450a0a" text-anchor="middle">Model Answers</text>
      </g>
      <!-- Mock Tests (Lavender) -->
      <g transform="translate(454, 0)">
        <rect width="155" height="42" rx="21" fill="#c084fc" />
        <text x="77" y="26" font-family="'Segoe UI', Inter, sans-serif" font-size="14" font-weight="700" fill="#3b0764" text-anchor="middle">Mock Tests</text>
      </g>
      <!-- Lab Manuals (Warm Orange) -->
      <g transform="translate(622, 0)">
        <rect width="165" height="42" rx="21" fill="#fb923c" />
        <text x="82" y="26" font-family="'Segoe UI', Inter, sans-serif" font-size="14" font-weight="700" fill="#431407" text-anchor="middle">Lab Manuals</text>
      </g>
    </g>

    <!-- Bottom Feature Pills Row 2 -->
    <g transform="translate(0, {pills_y2})">
      <!-- Videos (Cyan) -->
      <g transform="translate(0, 0)">
        <rect width="115" height="38" rx="19" fill="#38bdf8" />
        <text x="57" y="24" font-family="'Segoe UI', Inter, sans-serif" font-size="13" font-weight="700" fill="#0c4a6e" text-anchor="middle">Videos</text>
      </g>
      <!-- Syllabus (Pink) -->
      <g transform="translate(128, 0)">
        <rect width="125" height="38" rx="19" fill="#f472b6" />
        <text x="62" y="24" font-family="'Segoe UI', Inter, sans-serif" font-size="13" font-weight="700" fill="#500724" text-anchor="middle">Syllabus</text>
      </g>
      <!-- Question Bank (Emerald) -->
      <g transform="translate(266, 0)">
        <rect width="175" height="38" rx="19" fill="#6ee7b7" />
        <text x="87" y="24" font-family="'Segoe UI', Inter, sans-serif" font-size="13" font-weight="700" fill="#064e3b" text-anchor="middle">Question Bank</text>
      </g>
    </g>
  </g>

  <!-- Right Graphic: Layered Card / Document Mockup -->
  <g transform="translate(885, 145)">
    <!-- Radial Glow Behind Card -->
    <circle cx="140" cy="150" r="170" fill="url(#cardGlow)" />

    <!-- Back Card 1 (Translucent Outline) -->
    <rect x="-30" y="-15" width="250" height="295" rx="32" fill="rgba(255, 255, 255, 0.08)" stroke="rgba(255, 255, 255, 0.22)" stroke-width="1.5" />

    <!-- Middle Card 2 (Semi-Opaque) -->
    <rect x="-15" y="0" width="250" height="295" rx="32" fill="rgba(255, 255, 255, 0.16)" stroke="rgba(255, 255, 255, 0.32)" stroke-width="1.5" />

    <!-- Front Card 3 (Solid White with Drop Shadow) -->
    <rect x="0" y="15" width="250" height="295" rx="32" fill="#ffffff" filter="url(#dropShadow)" />

    <!-- Card Inner Elements -->
    <!-- Primary Colored Accent Bar -->
    <rect x="28" y="52" width="150" height="22" rx="11" fill="{theme['card_bar']}" />

    <!-- Text Placeholder Bars -->
    <rect x="28" y="94" width="190" height="14" rx="7" fill="#94a3b8" />
    <rect x="28" y="124" width="140" height="14" rx="7" fill="#cbd5e1" />
    <rect x="28" y="154" width="180" height="14" rx="7" fill="#94a3b8" />
    <rect x="28" y="184" width="120" height="14" rx="7" fill="#cbd5e1" />
  </g>

  <!-- Footer Watermark Bar -->
  <g transform="translate(70, 580)">
    <text x="0" y="0" font-family="'Segoe UI', Inter, sans-serif" font-size="13" font-weight="500" fill="#64748b">
      Maharashtra State Board of Technical Education • K-Scheme 2026
    </text>
    <text x="1060" y="0" font-family="'Segoe UI', Inter, sans-serif" font-size="13" font-weight="600" fill="{theme['accent']}" text-anchor="end">
      msbtenotes-info.netlify.app
    </text>
  </g>
</svg>'''
    return svg

def convert_single_svg_to_png(svg_path):
    base = os.path.basename(svg_path)
    png_name = base[:-4] + '.png'
    png_path = os.path.join(MEDIA_DIR, png_name)
    uri = 'file:///' + os.path.abspath(svg_path).replace('\\', '/')
    cmd = [
        CHROME_PATH,
        '--headless',
        '--disable-gpu',
        f'--screenshot={png_path}',
        '--window-size=1200,630',
        uri
    ]
    res = subprocess.run(cmd, capture_output=True)
    if res.returncode == 0 and os.path.exists(png_path) and os.path.getsize(png_path) > 10000:
        return png_name, os.path.getsize(png_path)
    return None, 0

def process_all_thumbnails():
    svg_files = glob.glob(os.path.join(MEDIA_DIR, '*.svg'))
    # Filter out test files
    svg_files = [f for f in svg_files if not os.path.basename(f).startswith('test_')]
    print(f"Total SVGs to process in {MEDIA_DIR}: {len(svg_files)}")
    
    generated_count = 0
    
    for fpath in svg_files:
        base = os.path.basename(fpath)
        stem = base[:-4]
        
        # Determine Title, Code, Subtitle, Sem, Theme
        if '-Semester-' in stem:
            # Branch Semester, e.g. Computer-Semester-1
            parts = stem.split('-Semester-')
            branch_part = parts[0].replace('-', ' ')
            sem_num = parts[1]
            title = f"{branch_part.title()} Semester {sem_num}"
            code = None
            sem_label = f"Semester {sem_num}"
            subtitle = f"{branch_part.title()} Engineering • K-Scheme Curriculum"
            theme = detect_theme(stem)
        elif stem in ['Computer', 'Information-Technology', 'AI-ML', 'Civil', 'Electrical-Engineering', 'ETC-Engineering', 'Mechanical-Engineering', 'an6k', 'ee6k']:
            # Branch Main Landing
            clean_name = stem.replace('-Engineering', ' Engg').replace('-', ' ').title()
            title = f"{clean_name} Diploma"
            code = None
            sem_label = "Sem 1 to 6"
            subtitle = "Complete MSBTE Diploma Study Portal"
            theme = detect_theme(stem)
        else:
            # Subject file, e.g. 313301-data-structure-using-c or elective-315316-...
            m_code = re.search(r'(\d{5,6})', stem)
            code = m_code.group(1) if m_code else None
            if code == '331632':
                code = '316326'
            
            meta = subjects_meta.get(code, {})
            raw_name = meta.get('name')
            if not raw_name:
                slug_part = re.sub(r'^(elective-)?(\d{5,6})-?', '', stem)
                raw_name = slug_part.replace('-', ' ').title()
            
            title = raw_name.title() if raw_name else f"Subject {code}"
            
            branches = meta.get('branches', set())
            semesters = meta.get('semesters', set())
            sem_label = list(semesters)[0] if semesters else "K-Scheme"
            
            if branches:
                subtitle = " • ".join(sorted(list(branches))[:2]) + f" • {sem_label}"
            else:
                subtitle = f"Diploma Engineering • {sem_label}"
                
            theme = detect_theme(stem, branches)

        # Generate modern SVG
        svg_content = generate_svg_markup(title, code, subtitle, sem_label, theme)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        generated_count += 1

    print(f"Generated and upgraded {generated_count} vector SVGs.")

    # Convert SVGs to PNGs using Chrome headless in parallel
    print("Converting SVGs to 1200x630 high-resolution PNGs with parallel Chrome headless...")
    t0 = time.time()
    converted_count = 0
    with ThreadPoolExecutor(max_workers=6) as executor:
        results = list(executor.map(convert_single_svg_to_png, svg_files))
    
    for name, sz in results:
        if name:
            converted_count += 1
            
    elapsed = round(time.time() - t0, 1)
    print(f"\n==========================================")
    print(f"SUCCESS! {generated_count} SVGs updated, {converted_count}/{len(svg_files)} PNGs generated in {elapsed}s.")
    print(f"==========================================")

if __name__ == '__main__':
    process_all_thumbnails()
