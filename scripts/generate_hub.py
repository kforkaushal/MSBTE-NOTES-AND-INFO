#!/usr/bin/env python3
"""
Generate start.html - The Master Student "Start Here" Resource Hub
MSBTE Notes & Information
Reads data/msbte_k_scheme_subjects.csv, Branches/, Notes/, pyq/, and model-answer/
and generates a single, unified, additive start.html portal.
"""

import os
import glob
import re
import csv
import json

def collect_subject_hub_data():
    subjects = {} # code -> dict
    
    # 1. Read data/msbte_k_scheme_subjects.csv for accurate metadata
    if os.path.exists('data/msbte_k_scheme_subjects.csv'):
        with open('data/msbte_k_scheme_subjects.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                code = row.get('Subject Code', '').strip()
                name = row.get('Subject Name', '').strip()
                branch = row.get('Branch', '').strip()
                sem = row.get('Semester', '').strip()
                pdf = row.get('PDF Link', '').strip()
                
                if code and re.match(r'^\d{5,6}$', code):
                    if code not in subjects:
                        clean_name = name.title() if name else f"Subject {code}"
                        subjects[code] = {
                            'code': code,
                            'name': clean_name,
                            'branches': set(),
                            'semesters': set(),
                            'links': {}
                        }
                    if branch: subjects[code]['branches'].add(branch)
                    
                    # MSBTE K-Scheme course codes 31X... encode semester directly as the 3rd digit
                    if code.startswith('31') and len(code) == 6 and code[2] in '123456':
                        subjects[code]['semesters'].add(int(code[2]))
                    elif sem:
                        m_sem = re.search(r'(?:Semester|Sem|Semester\s*)(\d+)', sem, re.IGNORECASE)
                        if m_sem:
                            subjects[code]['semesters'].add(int(m_sem.group(1)))
                        elif 'first' in sem.lower(): subjects[code]['semesters'].add(1)
                        elif 'second' in sem.lower(): subjects[code]['semesters'].add(2)
                        elif 'third' in sem.lower(): subjects[code]['semesters'].add(3)
                        elif 'fourth' in sem.lower(): subjects[code]['semesters'].add(4)
                        elif 'fifth' in sem.lower(): subjects[code]['semesters'].add(5)
                        elif 'sixth' in sem.lower(): subjects[code]['semesters'].add(6)
                    if pdf:
                        subjects[code]['links']['syllabus_pdf'] = pdf

    # 2. Check Branches/*.html (Syllabus & Subject Guides)
    for f in glob.glob('Branches/*.html'):
        base = os.path.basename(f)
        m = re.match(r'^(\d{5,6})-(.+)\.html$', base)
        if m:
            code, slug = m.groups()
            if code not in subjects:
                subjects[code] = {
                    'code': code,
                    'name': slug.replace('-', ' ').title(),
                    'branches': set(),
                    'semesters': set(),
                    'links': {}
                }
            subjects[code]['links']['syllabus'] = f'/Branches/{base}'

    # 3. Check Notes/*.html (Unit Notes & IMPs)
    for f in glob.glob('Notes/*.html'):
        base = os.path.basename(f)
        m = re.match(r'^(\d{5,6})-(.+)\.html$', base)
        if m:
            code, slug = m.groups()
            if code not in subjects:
                subjects[code] = {
                    'code': code,
                    'name': slug.replace('-', ' ').title(),
                    'branches': set(),
                    'semesters': set(),
                    'links': {}
                }
            subjects[code]['links']['notes'] = f'/Notes/{base}'

    # 4. Check pyq/ (Previous Year Question Papers)
    for f in glob.glob('pyq/*.html'):
        base = os.path.basename(f)
        m = re.match(r'^(\d{5,6})-(.+)\.html$', base)
        if m:
            code, slug = m.groups()
            if code not in subjects:
                subjects[code] = {
                    'code': code,
                    'name': slug.replace('-', ' ').title(),
                    'branches': set(),
                    'semesters': set(),
                    'links': {}
                }
            folder_form = f'pyq/{code}-{slug}/index.html'
            if os.path.exists(folder_form):
                subjects[code]['links']['pyq'] = f'/pyq/{code}-{slug}/'
            else:
                subjects[code]['links']['pyq'] = f'/pyq/{base}'

    # 5. Check model-answer/ (Solved Model Answer Papers)
    for f in glob.glob('model-answer/*.html'):
        base = os.path.basename(f)
        m = re.match(r'^(\d{5,6})-(.+)\.html$', base)
        if m:
            code, slug = m.groups()
            if code not in subjects:
                subjects[code] = {
                    'code': code,
                    'name': slug.replace('-', ' ').title(),
                    'branches': set(),
                    'semesters': set(),
                    'links': {}
                }
            folder_form = f'model-answer/{code}-{slug}/index.html'
            if os.path.exists(folder_form):
                subjects[code]['links']['model_answer'] = f'/model-answer/{code}-{slug}/'
            else:
                subjects[code]['links']['model_answer'] = f'/model-answer/{base}'

    # 6. Check Notes/Manual/ (Lab Manuals)
    manual_files = glob.glob('Notes/Manual/*.html')
    for mf in manual_files:
        m_base = os.path.basename(mf)
        m_code = re.match(r'^(\d{5,6})-(.+)\.html$', m_base)
        if m_code:
            code = m_code.group(1)
            if code in subjects:
                subjects[code]['links']['lab_manual'] = f'/Notes/Manual/{m_base}'

    # Convert sets to sorted lists for serialization
    subject_list = []
    for code, data in sorted(subjects.items(), key=lambda x: x[0]):
        sem_sorted = sorted(list(data['semesters']))
        sem_str = f"Sem {', '.join(str(s) for s in sem_sorted)}" if sem_sorted else "K-Scheme"
        
        # Abbreviate branch names for clean UI display
        branch_abbrs = []
        for b in sorted(list(data['branches'])):
            b_low = b.lower()
            if 'computer' in b_low or 'co' in b_low: branch_abbrs.append('CO')
            elif 'information' in b_low or 'it' in b_low: branch_abbrs.append('IF')
            elif 'ai' in b_low or 'artificial' in b_low: branch_abbrs.append('AN')
            elif 'mechanical' in b_low or 'me' in b_low: branch_abbrs.append('ME')
            elif 'civil' in b_low or 'ce' in b_low: branch_abbrs.append('CE')
            elif 'electrical' in b_low or 'ee' in b_low: branch_abbrs.append('EE')
            elif 'electronics' in b_low or 'etc' in b_low: branch_abbrs.append('EJ')
        
        branch_display = " • ".join(sorted(list(set(branch_abbrs)))) if branch_abbrs else "All Branches"
        
        subject_list.append({
            'code': code,
            'name': data['name'],
            'semester': sem_str,
            'semesters': sem_sorted,
            'branches': branch_display,
            'links': data['links']
        })

    return subject_list

def generate_start_html():
    subjects = collect_subject_hub_data()
    subjects_json = json.dumps(subjects, ensure_ascii=False)
    
    html_content = f"""<!DOCTYPE html>
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
    
    <!-- Meta Configuration -->
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>MSBTE Start Here Hub – Master Diploma Resource Directory 2026</title>
    <meta name="description"
        content="The official start-here portal for MSBTE diploma students. One clean reference for verified K-Scheme notes, PYQ question papers, model answers, syllabus, and lab manuals organized by branch and semester." />
    <meta name="keywords"
        content="MSBTE start here, MSBTE directory, MSBTE notes, MSBTE PYQ, MSBTE model answer, MSBTE K scheme syllabus, MSBTE diploma engineering, Computer engineering MSBTE, Mechanical MSBTE, Civil MSBTE, Electrical MSBTE" />
    <meta name="author" content="MSBTE Notes & Info Team" />
    <meta name="robots" content="index, follow" />
    <link rel="canonical" href="https://msbtenotes-info.netlify.app/start.html" />

    <!-- Open Graph / Social Sharing -->
    <meta property="og:type" content="website" />
    <meta property="og:title" content="MSBTE Start Here Hub – Master Diploma Resource Directory 2026" />
    <meta property="og:description"
        content="Never hunt across the site. Instant access to MSBTE notes, PYQs, model answers, syllabus, lab manuals, and exam updates for all engineering branches." />
    <meta property="og:url" content="https://msbtenotes-info.netlify.app/start.html" />
    <meta property="og:site_name" content="MSBTE Notes & Info" />
    <meta property="og:image" content="https://msbtenotes-info.netlify.app/resourse/MSBTE%20NOTES%20AND%20INFORMATION.png" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:locale" content="en_IN" />

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="MSBTE Start Here Hub – Master Diploma Resource Directory 2026" />
    <meta name="twitter:description"
        content="One clean reference of where every student resource lives: notes, PYQs, model answers, syllabus and results." />
    <meta name="twitter:image" content="https://msbtenotes-info.netlify.app/resourse/MSBTE%20NOTES%20AND%20INFORMATION.png" />
    <meta name="twitter:site" content="@msbtenotes" />

    <!-- Favicon -->
    <link rel="apple-touch-icon" sizes="180x180" href="/resourse/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/resourse/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/resourse/favicon-16x16.png">
    <link rel="manifest" href="/resourse/site.webmanifest">
    <link rel="icon" href="/resourse/favicon.ico" type="image/x-icon">
    <link rel="shortcut icon" href="/resourse/favicon.ico">

    <!-- Fonts & Styles -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="preconnect" href="https://api.fontshare.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link href="https://api.fontshare.com/v2/css?f[]=clash-display@600,700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/style.css">
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">

    <!-- Google AdSense -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9227354288966999" crossorigin="anonymous"></script>

    <!-- Structured Data -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "WebPage",
      "name": "MSBTE Start Here Hub – Master Diploma Resource Directory",
      "description": "Comprehensive resource directory for MSBTE diploma engineering students covering branches, semesters, PYQs, notes, model answers, and syllabus.",
      "url": "https://msbtenotes-info.netlify.app/start.html",
      "breadcrumb": {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{
            "@type": "ListItem",
            "position": 1,
            "name": "Home",
            "item": "https://msbtenotes-info.netlify.app/"
          }},
          {{
            "@type": "ListItem",
            "position": 2,
            "name": "Start Here Hub",
            "item": "https://msbtenotes-info.netlify.app/start.html"
          }}
        ]
      }}
    }}
    </script>

    <style>
        :root {{
            --primary-gradient: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
            --card-hover: 0 14px 30px -4px rgba(37, 99, 235, 0.12);
        }}

        body {{
            background-color: #f8fafc;
            background-image: radial-gradient(#e2e8f0 1.2px, transparent 1.2px);
            background-size: 24px 24px;
            font-family: 'Inter', sans-serif;
            -webkit-font-smoothing: antialiased;
        }}

        h1, h2, h3, h4, .font-display {{
            font-family: 'Clash Display', sans-serif;
            letter-spacing: -0.015em;
        }}

        /* Navbar Solid Elevation */
        nav.fixed, header.fixed {{
            background-color: #ffffff !important;
            border-bottom: 1px solid rgba(229, 231, 235, 0.95) !important;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05) !important;
        }}

        #mobileNav {{
            background-color: #ffffff !important;
            z-index: 9999 !important;
        }}

        .nav-dropdown.is-open .dropdown-menu {{
            display: block !important;
        }}

        .nav-dropdown.is-open .dropdown-arrow {{
            transform: rotate(180deg);
        }}

        .gradient-text {{
            background: var(--primary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        /* Interactive Directory Cards */
        .hub-card {{
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 1.25rem;
            padding: 1.5rem;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        .hub-card:hover {{
            transform: translateY(-3px);
            border-color: #93c5fd;
            box-shadow: var(--card-hover);
        }}

        .hub-card:active {{
            transform: scale(0.99);
        }}

        /* Quick Action Pill */
        .action-pill {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            min-height: 44px;
            padding: 0.5rem 1.15rem;
            border-radius: 0.875rem;
            font-weight: 600;
            font-size: 0.875rem;
            transition: all 0.2s ease;
            user-select: none;
        }}

        /* Semester Selector Buttons */
        .sem-btn {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-height: 44px;
            padding: 0.5rem 1rem;
            border-radius: 0.85rem;
            font-weight: 600;
            font-size: 0.875rem;
            background: #ffffff;
            border: 1px solid #e2e8f0;
            color: #4b5563;
            transition: all 0.2s ease;
            cursor: pointer;
        }}

        .sem-btn:hover {{
            background: #eff6ff;
            color: #2563eb;
            border-color: #bfdbfe;
        }}

        .sem-btn.active {{
            background: var(--primary-gradient);
            color: #ffffff;
            border-color: transparent;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
        }}

        /* Search Input */
        .search-box {{
            background: #ffffff;
            border: 1.5px solid #cbd5e1;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
            transition: all 0.2s ease;
        }}

        .search-box:focus-within {{
            border-color: #2563eb;
            box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.12), 0 10px 25px -5px rgba(37, 99, 235, 0.08);
        }}

        mark {{
            background-color: #fef08a;
            color: #111827;
            padding: 0 2px;
            border-radius: 2px;
        }}
    </style>
</head>

<body class="bg-gray-50 text-gray-900 pt-20 overflow-x-hidden w-full max-w-full">

    <!-- Header Navigation (Solid White, Elevated, Non-overlapping) -->
    <nav class="bg-white shadow fixed top-0 left-0 right-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <!-- Left: Logo -->
                <div class="flex items-center">
                    <a href="/" class="flex items-center text-blue-600 font-bold text-lg sm:text-xl font-display">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 sm:h-7 sm:w-7 mr-2 text-blue-600 flex-shrink-0" viewBox="0 0 576 512" fill="currentColor">
                            <path d="M249.6 471.5c10.8 3.8 22.4-4.1 22.4-15.5V78.6c0-4.2-1.6-8.4-5-11C247.4 52 202.4 32 144 32C93.5 32 46.3 45.3 18.1 56.1C6.8 60.5 0 71.7 0 83.8V454.1c0 11.9 12.8 20.2 24.1 16.5C55.6 460.1 105.5 448 144 448c33.9 0 79 14 105.6 23.5zm76.8 0C353 462 398.1 448 432 448c38.5 0 88.4 12.1 119.9 22.6c11.3 3.8 24.1-4.6 24.1-16.5V83.8c0-12.1-6.8-23.3-18.1-27.6C529.7 45.3 482.5 32 432 32c-58.4 0-103.4 20-123 35.6c-3.3 2.6-5 6.8-5 11V456c0 11.4 11.7 19.3 22.4 15.5z"/>
                        </svg>
                        <span>MSBTE Notes &amp; Info</span>
                    </a>
                </div>

                <!-- Middle: Desktop Nav -->
                <div class="hidden md:flex space-x-6 items-center">
                    <a href="/" class="hover:text-blue-500 font-medium text-gray-700">Home</a>
                    <a href="/start.html" class="text-blue-600 font-bold bg-blue-50 px-3 py-1.5 rounded-lg border border-blue-200">Start Here</a>

                    <!-- Notes & Study Dropdown -->
                    <div class="relative group py-2 nav-dropdown">
                        <button type="button" onclick="toggleDropdown(this, event)" class="flex items-center gap-1 hover:text-blue-500 font-medium text-gray-700 focus:outline-none" aria-haspopup="true" aria-expanded="false">
                            <span>Study Materials</span>
                            <svg class="w-4 h-4 transition-transform duration-200 dropdown-arrow" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                        </button>
                        <div class="dropdown-menu absolute left-0 top-full -mt-1 w-64 bg-white rounded-xl shadow-xl border border-gray-100 py-2 hidden group-hover:block transition-all z-50">
                            <a href="/notes/" class="flex items-center gap-2.5 px-4 py-2.5 text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-600 font-medium transition">
                                <span class="w-2 h-2 rounded-full bg-blue-600 flex-shrink-0"></span>
                                <div>
                                    <div class="font-bold text-gray-900">Notes &amp; Study Library</div>
                                    <div class="text-xs text-gray-500">470+ verified K-Scheme study materials</div>
                                </div>
                            </a>
                            <a href="/pyq/" class="flex items-center gap-2.5 px-4 py-2.5 text-sm text-gray-700 hover:bg-rose-50 hover:text-rose-600 font-medium transition">
                                <span class="w-2 h-2 rounded-full bg-rose-500 flex-shrink-0"></span>
                                <div>
                                    <div class="font-semibold text-gray-900">Question Papers (PYQ)</div>
                                    <div class="text-xs text-gray-500">117+ subjects summer &amp; winter papers</div>
                                </div>
                            </a>
                            <a href="/model-answer/" class="flex items-center gap-2.5 px-4 py-2.5 text-sm text-gray-700 hover:bg-emerald-50 hover:text-emerald-600 font-medium transition">
                                <span class="w-2 h-2 rounded-full bg-emerald-500 flex-shrink-0"></span>
                                <div>
                                    <div class="font-semibold text-gray-900">Model Answer Papers</div>
                                    <div class="text-xs text-gray-500">Official solved papers &amp; marking schemes</div>
                                </div>
                            </a>
                            <a href="/video-course/" class="flex items-center gap-2.5 px-4 py-2.5 text-sm text-gray-700 hover:bg-purple-50 hover:text-purple-600 font-medium transition">
                                <span class="w-2 h-2 rounded-full bg-purple-500 flex-shrink-0"></span>
                                <div>
                                    <div class="font-semibold text-gray-900">Video Courses</div>
                                    <div class="text-xs text-gray-500">Engineering tutorials &amp; lectures</div>
                                </div>
                            </a>
                        </div>
                    </div>

                    <a href="/pyq/" class="hover:text-blue-500 font-medium text-gray-700">PYQ Papers</a>
                    <a href="/model-answer/" class="hover:text-blue-500 font-medium text-gray-700">Model Answers</a>
                    <a href="/blog/" class="hover:text-blue-500 font-medium text-gray-700">Blog</a>
                    <a href="/news/" class="hover:text-red-500 font-medium text-gray-700 flex items-center gap-1.5">
                        <span class="inline-block w-2 h-2 rounded-full bg-red-500 animate-pulse"></span>
                        <span>News</span>
                    </a>

                    <!-- Jobs Dropdown -->
                    <div class="relative group py-2 nav-dropdown">
                        <button type="button" onclick="toggleDropdown(this, event)" class="flex items-center gap-1 hover:text-blue-500 font-medium text-gray-700 focus:outline-none" aria-haspopup="true" aria-expanded="false">
                            <span>Jobs</span>
                            <svg class="w-4 h-4 transition-transform duration-200 dropdown-arrow" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                        </button>
                        <div class="dropdown-menu absolute left-0 top-full -mt-1 w-52 bg-white rounded-xl shadow-xl border border-gray-100 py-2 hidden group-hover:block transition-all z-50">
                            <a href="/Jobs/index.html" class="flex items-center gap-2.5 px-4 py-2.5 text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-600 font-medium transition">
                                <span class="w-2 h-2 rounded-full bg-amber-500"></span>
                                <span>Jobs Portal</span>
                            </a>
                            <a href="/internships.html" class="flex items-center gap-2.5 px-4 py-2.5 text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-600 font-medium transition">
                                <span class="w-2 h-2 rounded-full bg-indigo-500"></span>
                                <span>Internships</span>
                            </a>
                        </div>
                    </div>

                    <a href="/contact.html" class="hover:text-blue-500 font-medium text-gray-700">Contact</a>
                </div>

                <!-- Right: Mobile Menu Toggle Button -->
                <div class="flex items-center md:hidden">
                    <button onclick="toggleMobileMenu()" class="mobile-menu-button p-2 text-gray-600 hover:text-blue-600 focus:outline-none min-h-[44px] min-w-[44px] flex items-center justify-center" aria-controls="mobileNav" aria-expanded="false" aria-label="Toggle menu">
                        <svg id="menuIcon" class="h-6 w-6 transition-transform duration-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7"/>
                        </svg>
                        <svg id="closeIcon" class="h-6 w-6 hidden transition-transform duration-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                        </svg>
                    </button>
                </div>
            </div>
        </div>

        <!-- Modern Mobile Navigation Drawer -->
        <div id="mobileNav" class="fixed inset-0 bg-white z-50 transform translate-x-full transition-transform duration-300 ease-in-out md:hidden overflow-y-auto pt-20 px-6" style="z-index: 9999 !important;">
            <button onclick="toggleMobileMenu()" class="absolute top-5 right-5 p-2 text-gray-600 hover:text-blue-600 focus:outline-none min-h-[44px] min-w-[44px] flex items-center justify-center" aria-label="Close menu">
                <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
            </button>

            <div class="flex flex-col space-y-4">
                <a href="/" onclick="toggleMobileMenu()" class="text-lg font-display font-bold text-gray-900 border-b border-gray-100 pb-2">Home</a>
                <a href="/start.html" onclick="toggleMobileMenu()" class="text-lg font-display font-bold text-blue-600 border-b border-gray-100 pb-2">Start Here Hub</a>

                <!-- Notes Mobile Submenu (Accordion) -->
                <div class="border-b border-gray-100 pb-2">
                    <button type="button" onclick="toggleMobileSubmenu('mobileNotesSubmenu', 'mobileNotesArrow')" class="w-full flex items-center justify-between text-lg font-display font-bold text-gray-900 py-1.5 focus:outline-none">
                        <span class="flex items-center gap-2">
                            <span>Study Materials</span>
                            <span class="text-xs font-sans font-semibold px-2 py-0.5 rounded-full bg-blue-100 text-blue-700">4 Links</span>
                        </span>
                        <svg id="mobileNotesArrow" class="w-5 h-5 text-gray-500 transition-transform duration-200 transform rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                        </svg>
                    </button>
                    <div id="mobileNotesSubmenu" class="space-y-1 pl-2 pt-1 pb-1 transition-all">
                        <a href="/notes/" onclick="toggleMobileMenu()" class="flex items-center gap-2.5 py-2 px-3 rounded-lg text-sm font-medium text-gray-700 hover:bg-blue-50 transition">
                            <span class="w-2 h-2 rounded-full bg-blue-600 flex-shrink-0"></span>
                            <div>
                                <div class="font-bold text-gray-900">Notes &amp; Study Library</div>
                                <div class="text-xs text-gray-500">470+ verified study materials &amp; notes</div>
                            </div>
                        </a>
                        <a href="/pyq/" onclick="toggleMobileMenu()" class="flex items-center gap-2.5 py-2 px-3 rounded-lg text-sm font-medium text-gray-700 hover:bg-rose-50 transition">
                            <span class="w-2 h-2 rounded-full bg-rose-500 flex-shrink-0"></span>
                            <div>
                                <div class="font-semibold text-gray-900">Question Papers (PYQ)</div>
                                <div class="text-xs text-gray-500">117+ subjects summer &amp; winter papers</div>
                            </div>
                        </a>
                        <a href="/model-answer/" onclick="toggleMobileMenu()" class="flex items-center gap-2.5 py-2 px-3 rounded-lg text-sm font-medium text-gray-700 hover:bg-emerald-50 transition">
                            <span class="w-2 h-2 rounded-full bg-emerald-500 flex-shrink-0"></span>
                            <div>
                                <div class="font-semibold text-gray-900">Model Answer Papers</div>
                                <div class="text-xs text-gray-500">Official solved papers &amp; marking schemes</div>
                            </div>
                        </a>
                        <a href="/video-course/" onclick="toggleMobileMenu()" class="flex items-center gap-2.5 py-2 px-3 rounded-lg text-sm font-medium text-gray-700 hover:bg-purple-50 transition">
                            <span class="w-2 h-2 rounded-full bg-purple-500 flex-shrink-0"></span>
                            <div>
                                <div class="font-semibold text-gray-900">Video Courses</div>
                                <div class="text-xs text-gray-500">Engineering tutorials &amp; concept walkthroughs</div>
                            </div>
                        </a>
                    </div>
                </div>

                <a href="/pyq/" onclick="toggleMobileMenu()" class="text-lg font-display font-bold text-gray-900 border-b border-gray-100 pb-2">PYQ Papers</a>
                <a href="/model-answer/" onclick="toggleMobileMenu()" class="text-lg font-display font-bold text-gray-900 border-b border-gray-100 pb-2">Model Answers</a>
                <a href="/blog/" onclick="toggleMobileMenu()" class="text-lg font-display font-bold text-gray-900 border-b border-gray-100 pb-2">Blog</a>
                <a href="/news/" onclick="toggleMobileMenu()" class="text-lg font-display font-bold text-red-600 border-b border-gray-100 pb-2 flex items-center justify-between">
                    <span>News Updates</span>
                    <span class="text-xs bg-red-100 text-red-600 font-semibold px-2 py-0.5 rounded-full uppercase tracking-wider">Live</span>
                </a>

                <!-- Jobs Submenu -->
                <div class="border-b border-gray-100 pb-2">
                    <button type="button" onclick="toggleMobileSubmenu('mobileJobsSubmenu', 'mobileJobsArrow')" class="w-full flex items-center justify-between text-lg font-display font-bold text-gray-900 py-1.5 focus:outline-none">
                        <span class="flex items-center gap-2">
                            <span>Jobs &amp; Career</span>
                            <span class="text-xs font-sans font-semibold px-2 py-0.5 rounded-full bg-blue-100 text-blue-700">2 Links</span>
                        </span>
                        <svg id="mobileJobsArrow" class="w-5 h-5 text-gray-500 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                        </svg>
                    </button>
                    <div id="mobileJobsSubmenu" class="hidden space-y-1 pl-2 pt-1 pb-1 transition-all">
                        <a href="/Jobs/index.html" onclick="toggleMobileMenu()" class="flex items-center gap-2.5 py-2 px-3 rounded-lg text-sm font-medium text-gray-700 hover:bg-blue-50 hover:text-blue-600 transition">
                            <span class="w-2 h-2 rounded-full bg-amber-500"></span>
                            <div>
                                <div class="font-semibold text-gray-900">Jobs Portal</div>
                                <div class="text-xs text-gray-500">MSBTE diploma jobs &amp; freshers hiring</div>
                            </div>
                        </a>
                        <a href="/internships.html" onclick="toggleMobileMenu()" class="flex items-center gap-2.5 py-2 px-3 rounded-lg text-sm font-medium text-gray-700 hover:bg-blue-50 hover:text-blue-600 transition">
                            <span class="w-2 h-2 rounded-full bg-indigo-500"></span>
                            <div>
                                <div class="font-semibold text-gray-900">Internships</div>
                                <div class="text-xs text-gray-500">Paid &amp; verified summer engineering internships</div>
                            </div>
                        </a>
                    </div>
                </div>

                <a href="/about.html" onclick="toggleMobileMenu()" class="text-lg font-display font-bold text-gray-900 border-b border-gray-100 pb-2">About</a>
                <a href="/contact.html" onclick="toggleMobileMenu()" class="text-lg font-display font-bold text-gray-900 border-b border-gray-100 pb-2">Contact</a>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12">

        <!-- Top Breadcrumbs Bar -->
        <nav aria-label="Breadcrumb" class="mb-6 flex items-center space-x-2 text-xs md:text-sm text-gray-500 overflow-x-auto whitespace-nowrap py-1 no-scrollbar">
            <a href="/" class="hover:text-blue-600 transition-colors flex items-center gap-1 font-medium">
                <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
                </svg>
                Home
            </a>
            <span class="text-gray-300">/</span>
            <span class="font-semibold text-gray-800">Start Here Hub</span>
        </nav>

        <!-- Hero Section -->
        <header class="text-center mb-12">
            <div class="inline-flex items-center gap-2 py-1 px-4 rounded-full bg-blue-50 border border-blue-200/80 text-blue-700 text-xs font-semibold tracking-wide uppercase mb-4 shadow-sm">
                <span class="w-2 h-2 rounded-full bg-blue-600 animate-pulse"></span>
                Official MSBTE Student Navigation Map
            </div>

            <h1 class="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold font-display tracking-tight text-gray-900 mb-4 leading-tight">
                One Hub, Every <span class="gradient-text">MSBTE Resource</span>
            </h1>

            <p class="max-w-3xl mx-auto text-base sm:text-lg text-gray-600 leading-relaxed mb-6">
                Never hunt across the site. Find your engineering branch, semester syllabus, unit notes, previous year question papers (PYQ), solved model answers, and career portals in one place.
            </p>

            <!-- Value Stat Badges -->
            <div class="flex flex-wrap items-center justify-center gap-2 sm:gap-3 text-xs font-semibold text-gray-700">
                <div class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-white border border-gray-200/90 shadow-sm">
                    <span class="w-2 h-2 rounded-full bg-blue-600"></span>
                    <span>7 Engineering Branches</span>
                </div>
                <div class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-white border border-rose-200/90 shadow-sm text-rose-700">
                    <span class="w-2 h-2 rounded-full bg-rose-500"></span>
                    <span>117 PYQ Papers</span>
                </div>
                <div class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-white border border-emerald-200/90 shadow-sm text-emerald-700">
                    <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
                    <span>15 Model Answers</span>
                </div>
                <div class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-white border border-purple-200/90 shadow-sm text-purple-700">
                    <span class="w-2 h-2 rounded-full bg-purple-500"></span>
                    <span>Sem 1 to Sem 6</span>
                </div>
            </div>
        </header>

        <!-- SECTION 1: Subject Finder Search Box -->
        <section class="max-w-4xl mx-auto mb-16">
            <div class="bg-white rounded-2xl md:rounded-3xl p-5 sm:p-7 border border-gray-200/90 shadow-sm">
                <div class="flex items-center gap-3 mb-4">
                    <div class="p-2 rounded-xl bg-blue-50 text-blue-600">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                        </svg>
                    </div>
                    <div>
                        <h2 class="text-xl font-bold font-display text-gray-900">Instant Subject Finder</h2>
                        <p class="text-xs text-gray-500">Type subject name or 6-digit code (e.g. 313301, OSY, Java, DSU, Mechanics)</p>
                    </div>
                </div>

                <div class="relative search-box rounded-xl overflow-hidden flex items-center mb-4">
                    <input type="text" id="subject-search-input"
                        class="block w-full px-4 py-3.5 bg-transparent text-gray-900 placeholder-gray-400 focus:outline-none text-base"
                        placeholder="Search 170+ subjects (e.g. Data Structure, 314317, Operating System)..."
                        autocomplete="off">
                    <button type="button" id="subject-search-clear" class="hidden pr-4 text-gray-400 hover:text-gray-600 min-h-[44px] min-w-[44px] flex items-center justify-center" aria-label="Clear search">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
                    </button>
                </div>

                <!-- Quick Query Chips -->
                <div class="flex flex-wrap items-center gap-2 mb-4">
                    <span class="text-xs font-semibold text-gray-400">Popular:</span>
                    <button type="button" class="quick-chip text-xs bg-gray-100 hover:bg-blue-50 hover:text-blue-600 text-gray-700 px-2.5 py-1 rounded-lg border border-gray-200 transition font-medium" data-term="313301">DSU (313301)</button>
                    <button type="button" class="quick-chip text-xs bg-gray-100 hover:bg-blue-50 hover:text-blue-600 text-gray-700 px-2.5 py-1 rounded-lg border border-gray-200 transition font-medium" data-term="314317">Java (314317)</button>
                    <button type="button" class="quick-chip text-xs bg-gray-100 hover:bg-blue-50 hover:text-blue-600 text-gray-700 px-2.5 py-1 rounded-lg border border-gray-200 transition font-medium" data-term="314319">OS (314319)</button>
                    <button type="button" class="quick-chip text-xs bg-gray-100 hover:bg-blue-50 hover:text-blue-600 text-gray-700 px-2.5 py-1 rounded-lg border border-gray-200 transition font-medium" data-term="313302">DBMS (313302)</button>
                    <button type="button" class="quick-chip text-xs bg-gray-100 hover:bg-blue-50 hover:text-blue-600 text-gray-700 px-2.5 py-1 rounded-lg border border-gray-200 transition font-medium" data-term="312312">Mechanics</button>
                </div>

                <!-- Search Results Live Container -->
                <div id="search-results-box" class="hidden border-t border-gray-100 pt-4 space-y-3">
                    <div id="search-results-count" class="text-xs font-bold text-gray-500"></div>
                    <div id="search-results-list" class="space-y-2.5 max-h-96 overflow-y-auto pr-1"></div>
                </div>
            </div>
        </section>

        <!-- SECTION 2: Pick Your Branch -->
        <section id="branches" class="mb-16">
            <div class="flex items-center justify-between mb-6">
                <div>
                    <h2 class="text-2xl md:text-3xl font-bold font-display text-gray-900 flex items-center gap-2">
                        <span class="p-1.5 rounded-xl bg-blue-50 text-blue-600">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
                        </span>
                        1. Pick Your Engineering Branch
                    </h2>
                    <p class="text-sm text-gray-500 mt-1">Select your diploma department to see branch syllabus, curriculum, and semester roadmaps.</p>
                </div>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 sm:gap-5">
                <!-- Computer Engineering -->
                <a href="/Branches/Computer.html" class="hub-card group">
                    <div>
                        <div class="w-12 h-12 rounded-2xl bg-indigo-50 border border-indigo-100 flex items-center justify-center text-indigo-600 mb-4 group-hover:bg-indigo-600 group-hover:text-white transition-colors">
                            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20"><path d="M2 6a2 2 0 012-2h5l2 2h5a2 2 0 012 2v6a2 2 0 01-2 2H4a2 2 0 01-2-2V6z"/></svg>
                        </div>
                        <span class="text-xs font-bold text-indigo-600 uppercase tracking-wider block mb-1">Code: CO</span>
                        <h3 class="text-lg font-bold font-display text-gray-900 group-hover:text-indigo-600 transition-colors">Computer Engineering</h3>
                        <p class="text-xs text-gray-500 mt-1 line-clamp-2">Sem 1 to 6 complete K-Scheme curriculum, notes, PYQs, and microprojects.</p>
                    </div>
                    <div class="mt-4 pt-3 border-t border-gray-100 flex items-center justify-between text-xs font-semibold text-indigo-600">
                        <span>View Branch &rarr;</span>
                        <span class="text-gray-400 font-normal">Sem 1-6</span>
                    </div>
                </a>

                <!-- Information Technology -->
                <a href="/Branches/Information-Technology.html" class="hub-card group">
                    <div>
                        <div class="w-12 h-12 rounded-2xl bg-purple-50 border border-purple-100 flex items-center justify-center text-purple-600 mb-4 group-hover:bg-purple-600 group-hover:text-white transition-colors">
                            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20"><path d="M2 6a2 2 0 012-2h5l2 2h5a2 2 0 012 2v6a2 2 0 01-2 2H4a2 2 0 01-2-2V6z"/></svg>
                        </div>
                        <span class="text-xs font-bold text-purple-600 uppercase tracking-wider block mb-1">Code: IF</span>
                        <h3 class="text-lg font-bold font-display text-gray-900 group-hover:text-purple-600 transition-colors">Information Technology</h3>
                        <p class="text-xs text-gray-500 mt-1 line-clamp-2">IT diploma notes, database systems, networking, web development, and papers.</p>
                    </div>
                    <div class="mt-4 pt-3 border-t border-gray-100 flex items-center justify-between text-xs font-semibold text-purple-600">
                        <span>View Branch &rarr;</span>
                        <span class="text-gray-400 font-normal">Sem 1-6</span>
                    </div>
                </a>

                <!-- AI & Machine Learning -->
                <a href="/Branches/AI-ML.html" class="hub-card group">
                    <div>
                        <div class="w-12 h-12 rounded-2xl bg-pink-50 border border-pink-100 flex items-center justify-center text-pink-600 mb-4 group-hover:bg-pink-600 group-hover:text-white transition-colors">
                            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20"><path d="M2 6a2 2 0 012-2h5l2 2h5a2 2 0 012 2v6a2 2 0 01-2 2H4a2 2 0 01-2-2V6z"/></svg>
                        </div>
                        <span class="text-xs font-bold text-pink-600 uppercase tracking-wider block mb-1">Code: AN</span>
                        <h3 class="text-lg font-bold font-display text-gray-900 group-hover:text-pink-600 transition-colors">AI &amp; Machine Learning</h3>
                        <p class="text-xs text-gray-500 mt-1 line-clamp-2">Python, ML algorithms, cloud computing for data science, and NLP resources.</p>
                    </div>
                    <div class="mt-4 pt-3 border-t border-gray-100 flex items-center justify-between text-xs font-semibold text-pink-600">
                        <span>View Branch &rarr;</span>
                        <span class="text-gray-400 font-normal">Sem 1-6</span>
                    </div>
                </a>

                <!-- Mechanical Engineering -->
                <a href="/Branches/Mechanical-Engineering.html" class="hub-card group">
                    <div>
                        <div class="w-12 h-12 rounded-2xl bg-amber-50 border border-amber-100 flex items-center justify-center text-amber-600 mb-4 group-hover:bg-amber-600 group-hover:text-white transition-colors">
                            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20"><path d="M2 6a2 2 0 012-2h5l2 2h5a2 2 0 012 2v6a2 2 0 01-2 2H4a2 2 0 01-2-2V6z"/></svg>
                        </div>
                        <span class="text-xs font-bold text-amber-600 uppercase tracking-wider block mb-1">Code: ME</span>
                        <h3 class="text-lg font-bold font-display text-gray-900 group-hover:text-amber-600 transition-colors">Mechanical Engineering</h3>
                        <p class="text-xs text-gray-500 mt-1 line-clamp-2">Thermodynamics, theory of machines, CAD/CAM, hydraulics, and manual copies.</p>
                    </div>
                    <div class="mt-4 pt-3 border-t border-gray-100 flex items-center justify-between text-xs font-semibold text-amber-600">
                        <span>View Branch &rarr;</span>
                        <span class="text-gray-400 font-normal">Sem 1-6</span>
                    </div>
                </a>

                <!-- Civil Engineering -->
                <a href="/Branches/Civil.html" class="hub-card group">
                    <div>
                        <div class="w-12 h-12 rounded-2xl bg-emerald-50 border border-emerald-100 flex items-center justify-center text-emerald-600 mb-4 group-hover:bg-emerald-600 group-hover:text-white transition-colors">
                            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20"><path d="M2 6a2 2 0 012-2h5l2 2h5a2 2 0 012 2v6a2 2 0 01-2 2H4a2 2 0 01-2-2V6z"/></svg>
                        </div>
                        <span class="text-xs font-bold text-emerald-600 uppercase tracking-wider block mb-1">Code: CE</span>
                        <h3 class="text-lg font-bold font-display text-gray-900 group-hover:text-emerald-600 transition-colors">Civil Engineering</h3>
                        <p class="text-xs text-gray-500 mt-1 line-clamp-2">Surveying, concrete technology, structural mechanics, and building construction.</p>
                    </div>
                    <div class="mt-4 pt-3 border-t border-gray-100 flex items-center justify-between text-xs font-semibold text-emerald-600">
                        <span>View Branch &rarr;</span>
                        <span class="text-gray-400 font-normal">Sem 1-6</span>
                    </div>
                </a>

                <!-- Electrical Engineering -->
                <a href="/Branches/Electrical-Engineering.html" class="hub-card group">
                    <div>
                        <div class="w-12 h-12 rounded-2xl bg-yellow-50 border border-yellow-200 flex items-center justify-center text-yellow-700 mb-4 group-hover:bg-yellow-500 group-hover:text-white transition-colors">
                            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20"><path d="M2 6a2 2 0 012-2h5l2 2h5a2 2 0 012 2v6a2 2 0 01-2 2H4a2 2 0 01-2-2V6z"/></svg>
                        </div>
                        <span class="text-xs font-bold text-yellow-800 uppercase tracking-wider block mb-1">Code: EE</span>
                        <h3 class="text-lg font-bold font-display text-gray-900 group-hover:text-yellow-600 transition-colors">Electrical Engineering</h3>
                        <p class="text-xs text-gray-500 mt-1 line-clamp-2">Circuits, AC/DC machines, power systems, transmission, and electrical formulas.</p>
                    </div>
                    <div class="mt-4 pt-3 border-t border-gray-100 flex items-center justify-between text-xs font-semibold text-yellow-700">
                        <span>View Branch &rarr;</span>
                        <span class="text-gray-400 font-normal">Sem 1-6</span>
                    </div>
                </a>

                <!-- Electronics & Telecommunication -->
                <a href="/Branches/ETC-Engineering.html" class="hub-card group">
                    <div>
                        <div class="w-12 h-12 rounded-2xl bg-teal-50 border border-teal-100 flex items-center justify-center text-teal-600 mb-4 group-hover:bg-teal-600 group-hover:text-white transition-colors">
                            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20"><path d="M2 6a2 2 0 012-2h5l2 2h5a2 2 0 012 2v6a2 2 0 01-2 2H4a2 2 0 01-2-2V6z"/></svg>
                        </div>
                        <span class="text-xs font-bold text-teal-600 uppercase tracking-wider block mb-1">Code: EJ</span>
                        <h3 class="text-lg font-bold font-display text-gray-900 group-hover:text-teal-600 transition-colors">Electronics &amp; TC</h3>
                        <p class="text-xs text-gray-500 mt-1 line-clamp-2">Digital techniques, microprocessors, communication protocols, and VLSI.</p>
                    </div>
                    <div class="mt-4 pt-3 border-t border-gray-100 flex items-center justify-between text-xs font-semibold text-teal-600">
                        <span>View Branch &rarr;</span>
                        <span class="text-gray-400 font-normal">Sem 1-6</span>
                    </div>
                </a>

                <!-- Master Notes Library -->
                <a href="/notes/" class="hub-card group border-blue-200 bg-blue-50/30">
                    <div>
                        <div class="w-12 h-12 rounded-2xl bg-blue-600 text-white flex items-center justify-center mb-4 group-hover:scale-105 transition-transform shadow-md">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>
                        </div>
                        <span class="text-xs font-bold text-blue-700 uppercase tracking-wider block mb-1">Master Archive</span>
                        <h3 class="text-lg font-bold font-display text-blue-900 group-hover:text-blue-700 transition-colors">All Study Materials</h3>
                        <p class="text-xs text-blue-700/80 mt-1 line-clamp-2">Search 470+ verified resources with branch, semester, and year filters.</p>
                    </div>
                    <div class="mt-4 pt-3 border-t border-blue-200/60 flex items-center justify-between text-xs font-semibold text-blue-700">
                        <span>Open Notes Portal &rarr;</span>
                        <span class="bg-blue-200/60 text-blue-800 px-2 py-0.5 rounded">470+ Items</span>
                    </div>
                </a>
            </div>
        </section>

        <!-- SECTION 3: Pick Your Semester -->
        <section id="semesters" class="mb-16">
            <div class="bg-white rounded-2xl md:rounded-3xl p-6 sm:p-8 border border-gray-200/90 shadow-sm">
                <div class="mb-6">
                    <h2 class="text-2xl md:text-3xl font-bold font-display text-gray-900 flex items-center gap-2">
                        <span class="p-1.5 rounded-xl bg-purple-50 text-purple-600">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                        </span>
                        2. Pick Your Semester
                    </h2>
                    <p class="text-sm text-gray-500 mt-1">Tap a semester to quickly open branch landing pages for that specific academic term.</p>
                </div>

                <!-- Semester Selector Buttons -->
                <div class="flex flex-wrap gap-2.5 sm:gap-3 mb-6" id="semester-selector-bar">
                    <button type="button" class="sem-btn active" data-sem="1">Semester 1 (FY)</button>
                    <button type="button" class="sem-btn" data-sem="2">Semester 2 (FY)</button>
                    <button type="button" class="sem-btn" data-sem="3">Semester 3 (SY)</button>
                    <button type="button" class="sem-btn" data-sem="4">Semester 4 (SY)</button>
                    <button type="button" class="sem-btn" data-sem="5">Semester 5 (TY)</button>
                    <button type="button" class="sem-btn" data-sem="6">Semester 6 (TY)</button>
                </div>

                <!-- Dynamic Semester Links Container -->
                <div id="semester-links-grid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                    <!-- Populated via client JS -->
                </div>
            </div>
        </section>

        <!-- SECTION 4: What Do You Need? (All Study Material Hubs) -->
        <section id="materials" class="mb-16">
            <div class="mb-6">
                <h2 class="text-2xl md:text-3xl font-bold font-display text-gray-900 flex items-center gap-2">
                    <span class="p-1.5 rounded-xl bg-emerald-50 text-emerald-600">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
                    </span>
                    3. What Do You Need?
                </h2>
                <p class="text-sm text-gray-500 mt-1">Direct master directories for question papers, solved model answers, question banks, and video lectures.</p>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
                <!-- PYQ Papers -->
                <a href="/pyq/" class="hub-card group border-rose-100 hover:border-rose-300">
                    <div class="flex items-start gap-4">
                        <div class="w-12 h-12 rounded-2xl bg-rose-50 border border-rose-100 flex items-center justify-center text-rose-600 flex-shrink-0 group-hover:bg-rose-600 group-hover:text-white transition-colors">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
                        </div>
                        <div>
                            <span class="text-xs font-bold text-rose-600 uppercase">117 Subjects</span>
                            <h3 class="text-lg font-bold font-display text-gray-900 group-hover:text-rose-600 transition-colors">Previous Year Papers (PYQ)</h3>
                            <p class="text-xs text-gray-500 mt-1">Official Summer &amp; Winter board question papers with Google Drive PDFs.</p>
                        </div>
                    </div>
                </a>

                <!-- Model Answers -->
                <a href="/model-answer/" class="hub-card group border-emerald-100 hover:border-emerald-300">
                    <div class="flex items-start gap-4">
                        <div class="w-12 h-12 rounded-2xl bg-emerald-50 border border-emerald-100 flex items-center justify-center text-emerald-600 flex-shrink-0 group-hover:bg-emerald-600 group-hover:text-white transition-colors">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                        </div>
                        <div>
                            <span class="text-xs font-bold text-emerald-600 uppercase">Official Solutions</span>
                            <h3 class="text-lg font-bold font-display text-gray-900 group-hover:text-emerald-600 transition-colors">Model Answer Papers</h3>
                            <p class="text-xs text-gray-500 mt-1">Solved question papers with question-wise MSBTE marking scheme breakdowns.</p>
                        </div>
                    </div>
                </a>

                <!-- Question Banks -->
                <a href="/Notes/msbte-k-scheme-question-banks.html" class="hub-card group border-amber-100 hover:border-amber-300">
                    <div class="flex items-start gap-4">
                        <div class="w-12 h-12 rounded-2xl bg-amber-50 border border-amber-100 flex items-center justify-center text-amber-600 flex-shrink-0 group-hover:bg-amber-600 group-hover:text-white transition-colors">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                        </div>
                        <div>
                            <span class="text-xs font-bold text-amber-600 uppercase">Super 25 IMPs</span>
                            <h3 class="text-lg font-bold font-display text-gray-900 group-hover:text-amber-600 transition-colors">Question Banks</h3>
                            <p class="text-xs text-gray-500 mt-1">High-yield unit-wise question banks for Unit Tests and Board Exam revision.</p>
                        </div>
                    </div>
                </a>

                <!-- Lab Manuals & Answers -->
                <a href="/notes/?type=lab-manual" class="hub-card group border-purple-100 hover:border-purple-300">
                    <div class="flex items-start gap-4">
                        <div class="w-12 h-12 rounded-2xl bg-purple-50 border border-purple-100 flex items-center justify-center text-purple-600 flex-shrink-0 group-hover:bg-purple-600 group-hover:text-white transition-colors">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.977l-.51.342a6 6 0 01-3.86.977l-2.387.477a2 2 0 00-1.022.547m3.234-1.234a6 6 0 013.86-.977l1.022.204a2 2 0 011.022.547m-3.234-1.234a6 6 0 00-3.86.977l-1.022.204a2 2 0 00-1.022.547m10.234-4.234a6 6 0 01-3.86-.977l-.51-.342a6 6 0 00-3.86-.977l-2.387-.477a2 2 0 00-1.022.547m3.234-1.234a6 6 0 013.86-.977l1.022.204a2 2 0 011.022.547m-3.234-1.234a6 6 0 00-3.86.977l-1.022.204a2 2 0 00-1.022.547"/></svg>
                        </div>
                        <div>
                            <span class="text-xs font-bold text-purple-600 uppercase">Practical Answers</span>
                            <h3 class="text-lg font-bold font-display text-gray-900 group-hover:text-purple-600 transition-colors">Lab Manuals &amp; Practicals</h3>
                            <p class="text-xs text-gray-500 mt-1">Solved manual answers, practical test viva questions, and observation tables.</p>
                        </div>
                    </div>
                </a>

                <!-- Micro-Project Ideas -->
                <a href="/Notes/4th-sem-computer-microprojects.html" class="hub-card group border-blue-100 hover:border-blue-300">
                    <div class="flex items-start gap-4">
                        <div class="w-12 h-12 rounded-2xl bg-blue-50 border border-blue-100 flex items-center justify-center text-blue-600 flex-shrink-0 group-hover:bg-blue-600 group-hover:text-white transition-colors">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/></svg>
                        </div>
                        <div>
                            <span class="text-xs font-bold text-blue-600 uppercase">Approved Topics</span>
                            <h3 class="text-lg font-bold font-display text-gray-900 group-hover:text-blue-600 transition-colors">Micro-Project Ideas</h3>
                            <p class="text-xs text-gray-500 mt-1">20+ ready topics, project reports, flowcharts, and source code templates.</p>
                        </div>
                    </div>
                </a>

                <!-- Video Courses -->
                <a href="/video-course/" class="hub-card group border-red-100 hover:border-red-300">
                    <div class="flex items-start gap-4">
                        <div class="w-12 h-12 rounded-2xl bg-red-50 border border-red-100 flex items-center justify-center text-red-600 flex-shrink-0 group-hover:bg-red-600 group-hover:text-white transition-colors">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                        </div>
                        <div>
                            <span class="text-xs font-bold text-red-600 uppercase">19 Lectures</span>
                            <h3 class="text-lg font-bold font-display text-gray-900 group-hover:text-red-600 transition-colors">Video Courses</h3>
                            <p class="text-xs text-gray-500 mt-1">Curated concept explanations, DSA walkthroughs, and practical demonstrations.</p>
                        </div>
                    </div>
                </a>

                <!-- MSBTE Syllabus & Scheme -->
                <a href="/scheme/" class="hub-card group border-teal-100 hover:border-teal-300">
                    <div class="flex items-start gap-4">
                        <div class="w-12 h-12 rounded-2xl bg-teal-50 border border-teal-100 flex items-center justify-center text-teal-600 flex-shrink-0 group-hover:bg-teal-600 group-hover:text-white transition-colors">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
                        </div>
                        <div>
                            <span class="text-xs font-bold text-teal-600 uppercase">Curriculum</span>
                            <h3 class="text-lg font-bold font-display text-gray-900 group-hover:text-teal-600 transition-colors">Syllabus &amp; Schemes</h3>
                            <p class="text-xs text-gray-500 mt-1">Official K-Scheme teaching plans, examination scheme, credits, and rules.</p>
                        </div>
                    </div>
                </a>

                <!-- Free Courses & Certifications -->
                <a href="/Courses/DSA-Basic.html" class="hub-card group border-indigo-100 hover:border-indigo-300">
                    <div class="flex items-start gap-4">
                        <div class="w-12 h-12 rounded-2xl bg-indigo-50 border border-indigo-100 flex items-center justify-center text-indigo-600 flex-shrink-0 group-hover:bg-indigo-600 group-hover:text-white transition-colors">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z"/></svg>
                        </div>
                        <div>
                            <span class="text-xs font-bold text-indigo-600 uppercase">Free Certs</span>
                            <h3 class="text-lg font-bold font-display text-gray-900 group-hover:text-indigo-600 transition-colors">Courses &amp; Certificates</h3>
                            <p class="text-xs text-gray-500 mt-1">Data structures beginner bootcamps, certificates, and coding practice.</p>
                        </div>
                    </div>
                </a>

                <!-- Mock Tests Exam Simulation -->
                <a href="/mock-tests/" class="hub-card group border-cyan-100 hover:border-cyan-300">
                    <div class="flex items-start gap-4">
                        <div class="w-12 h-12 rounded-2xl bg-cyan-50 border border-cyan-100 flex items-center justify-center text-cyan-600 flex-shrink-0 group-hover:bg-cyan-600 group-hover:text-white transition-colors">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>
                        </div>
                        <div>
                            <span class="text-xs font-bold text-cyan-600 uppercase">Test Series</span>
                            <h3 class="text-lg font-bold font-display text-gray-900 group-hover:text-cyan-600 transition-colors">Mock Tests Portal</h3>
                            <p class="text-xs text-gray-500 mt-1">MCQ test practice, unit self-assessment, and automated score evaluations.</p>
                        </div>
                    </div>
                </a>
            </div>
        </section>

        <!-- SECTION 5: Exam Assistance & Academic Tools -->
        <section id="exam-tools" class="mb-16">
            <div class="mb-6">
                <h2 class="text-2xl md:text-3xl font-bold font-display text-gray-900 flex items-center gap-2">
                    <span class="p-1.5 rounded-xl bg-rose-50 text-rose-600">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
                    </span>
                    4. Exam Help &amp; Live Updates
                </h2>
                <p class="text-sm text-gray-500 mt-1">Official timetable notifications, result release links, and student discussions.</p>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <a href="/news/" class="p-5 bg-white rounded-2xl border border-gray-200/90 shadow-sm hover:shadow-md transition group block">
                    <span class="text-xs font-bold text-red-600 uppercase flex items-center gap-1.5 mb-2">
                        <span class="w-2 h-2 rounded-full bg-red-500 animate-ping"></span>
                        Live Portal
                    </span>
                    <h3 class="text-base font-bold font-display text-gray-900 group-hover:text-red-600 transition">MSBTE News Updates</h3>
                    <p class="text-xs text-gray-500 mt-1">Circulars, exam schedule releases, and academic calendars.</p>
                </a>

                <a href="/blog/" class="p-5 bg-white rounded-2xl border border-gray-200/90 shadow-sm hover:shadow-md transition group block">
                    <span class="text-xs font-bold text-blue-600 uppercase block mb-2">Study Strategy</span>
                    <h3 class="text-base font-bold font-display text-gray-900 group-hover:text-blue-600 transition">Blog &amp; Exam Tips</h3>
                    <p class="text-xs text-gray-500 mt-1">Passing strategy, timetable analysis, and how to write answers.</p>
                </a>

                <a href="/forum.html" class="p-5 bg-white rounded-2xl border border-gray-200/90 shadow-sm hover:shadow-md transition group block">
                    <span class="text-xs font-bold text-purple-600 uppercase block mb-2">Q&amp;A Community</span>
                    <h3 class="text-base font-bold font-display text-gray-900 group-hover:text-purple-600 transition">Student Forum</h3>
                    <p class="text-xs text-gray-500 mt-1">Ask questions, discuss question paper doubts, and connect with peers.</p>
                </a>

                <a href="https://chat.whatsapp.com/KFcI5VeJOpjLPgp30NXMfQ" target="_blank" rel="noopener noreferrer" class="p-5 bg-white rounded-2xl border border-green-200 shadow-sm hover:shadow-md transition group block">
                    <span class="text-xs font-bold text-green-600 uppercase block mb-2">Direct Help</span>
                    <h3 class="text-base font-bold font-display text-gray-900 group-hover:text-green-600 transition">WhatsApp Support</h3>
                    <p class="text-xs text-gray-500 mt-1">Join 10,000+ diploma students on official WhatsApp groups.</p>
                </a>
            </div>
        </section>

        <!-- SECTION 6: After Diploma (Higher Studies & Careers) -->
        <section id="career" class="mb-16">
            <div class="mb-6">
                <h2 class="text-2xl md:text-3xl font-bold font-display text-gray-900 flex items-center gap-2">
                    <span class="p-1.5 rounded-xl bg-amber-50 text-amber-600">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
                    </span>
                    5. After Diploma: Degrees, Colleges &amp; Jobs
                </h2>
                <p class="text-sm text-gray-500 mt-1">Everything you need for Direct Second Year (DSE) engineering admissions and placement opportunities.</p>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <a href="/CollegeInfo/" class="hub-card group border-gray-200">
                    <span class="text-xs font-bold text-indigo-600 uppercase mb-1">District Directory</span>
                    <h3 class="text-base font-bold font-display text-gray-900 group-hover:text-indigo-600 transition">College Directory</h3>
                    <p class="text-xs text-gray-500 mt-1">Explore engineering colleges across Pune, Mumbai, Nashik, and Nagpur.</p>
                </a>

                <a href="/blog/msbte-summer-2026-exam-result-date-and-link.html" class="hub-card group border-gray-200">
                    <span class="text-xs font-bold text-blue-600 uppercase mb-1">DSE 2026 Guide</span>
                    <h3 class="text-base font-bold font-display text-gray-900 group-hover:text-blue-600 transition">DSE Engineering Admissions</h3>
                    <p class="text-xs text-gray-500 mt-1">CAP rounds, cut-off ranks, document checklist, and merit lists.</p>
                </a>

                <a href="/Jobs/index.html" class="hub-card group border-gray-200">
                    <span class="text-xs font-bold text-amber-600 uppercase mb-1">Fresher Jobs</span>
                    <h3 class="text-base font-bold font-display text-gray-900 group-hover:text-amber-600 transition">Diploma Jobs Portal</h3>
                    <p class="text-xs text-gray-500 mt-1">Off-campus drives, apprentice openings, and technical hiring notices.</p>
                </a>

                <a href="/internships.html" class="hub-card group border-gray-200">
                    <span class="text-xs font-bold text-emerald-600 uppercase mb-1">Industry Training</span>
                    <h3 class="text-base font-bold font-display text-gray-900 group-hover:text-emerald-600 transition">Summer Internships</h3>
                    <p class="text-xs text-gray-500 mt-1">Verified mandatory 6-week summer diploma engineering internships.</p>
                </a>
            </div>
        </section>

        <!-- Ad Slot -->
        <div class="max-w-4xl mx-auto my-12">
            <ins class="adsbygoogle" style="display:block; text-align:center;" data-ad-layout="in-article"
                data-ad-format="fluid" data-ad-client="ca-pub-9227354288966999" data-ad-slot="7917907402"></ins>
            <script> (adsbygoogle = window.adsbygoogle || []).push({{}}); </script>
        </div>

    </main>

    <!-- Footer -->
    <footer class="bg-indigo-950 text-blue-100 py-16 border-t border-indigo-900">
        <div class="max-w-6xl mx-auto px-4 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-10">
            <div>
                <a href="/" class="flex items-center gap-3 mb-5">
                    <div class="p-2 bg-white/10 rounded-lg text-white">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" viewBox="0 0 576 512" fill="currentColor">
                            <path d="M249.6 471.5c10.8 3.8 22.4-4.1 22.4-15.5V78.6c0-4.2-1.6-8.4-5-11C247.4 52 202.4 32 144 32C93.5 32 46.3 45.3 18.1 56.1C6.8 60.5 0 71.7 0 83.8V454.1c0 11.9 12.8 20.2 24.1 16.5C55.6 460.1 105.5 448 144 448c33.9 0 79 14 105.6 23.5zm76.8 0C353 462 398.1 448 432 448c38.5 0 88.4 12.1 119.9 22.6c11.3 3.8 24.1-4.6 24.1-16.5V83.8c0-12.1-6.8-23.3-18.1-27.6C529.7 45.3 482.5 32 432 32c-58.4 0-103.4 20-123 35.6c-3.3 2.6-5 6.8-5 11V456c0 11.4 11.7 19.3 22.4 15.5z"/>
                        </svg>
                    </div>
                    <span class="font-bold text-xl text-white font-display">MSBTE Notes &amp; Info</span>
                </a>
                <p class="text-sm leading-relaxed text-indigo-200">
                    The all-in-one resource hub for MSBTE diploma engineering students across Maharashtra. Free notes, solved model answers, question papers, and syllabus schemes.
                </p>
            </div>

            <div>
                <h3 class="text-white font-semibold text-lg mb-5 font-display">Navigation Hub</h3>
                <ul class="space-y-2.5 text-sm">
                    <li><a href="/" class="hover:text-white transition-colors flex items-center gap-2"><span class="w-1.5 h-1.5 bg-blue-400 rounded-full"></span> Home</a></li>
                    <li><a href="/start.html" class="text-white font-semibold flex items-center gap-2"><span class="w-1.5 h-1.5 bg-emerald-400 rounded-full"></span> Start Here Directory</a></li>
                    <li><a href="/notes/" class="hover:text-white transition-colors flex items-center gap-2"><span class="w-1.5 h-1.5 bg-blue-400 rounded-full"></span> Notes Library (470+)</a></li>
                    <li><a href="/pyq/" class="hover:text-white transition-colors flex items-center gap-2"><span class="w-1.5 h-1.5 bg-rose-400 rounded-full"></span> Question Papers (PYQ)</a></li>
                    <li><a href="/model-answer/" class="hover:text-white transition-colors flex items-center gap-2"><span class="w-1.5 h-1.5 bg-emerald-400 rounded-full"></span> Model Answer Papers</a></li>
                    <li><a href="/video-course/" class="hover:text-white transition-colors flex items-center gap-2"><span class="w-1.5 h-1.5 bg-purple-400 rounded-full"></span> Video Courses</a></li>
                    <li><a href="/blog/" class="hover:text-white transition-colors flex items-center gap-2"><span class="w-1.5 h-1.5 bg-blue-400 rounded-full"></span> Blog &amp; Updates</a></li>
                </ul>
            </div>

            <div>
                <h3 class="text-white font-semibold text-lg mb-5 font-display">Student Community</h3>
                <div class="space-y-3 text-sm">
                    <p class="flex items-center gap-2.5"><span class="text-indigo-400">Email:</span> info.mraaglave@gmail.com</p>
                    <p class="flex items-center gap-2.5"><span class="text-indigo-400">WhatsApp:</span> +91 70832 36221</p>

                    <a href="https://chat.whatsapp.com/KFcI5VeJOpjLPgp30NXMfQ" target="_blank" rel="noopener noreferrer"
                        class="inline-flex items-center gap-2 mt-4 bg-[#25D366] text-white px-5 py-2.5 rounded-full font-bold text-sm hover:bg-[#20bd5a] transition-colors shadow-lg min-h-[44px]">
                        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.008-.57-.008-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z" />
                        </svg>
                        Join WhatsApp Group
                    </a>
                </div>
            </div>
        </div>

        <div class="max-w-6xl mx-auto px-4 mt-12 pt-8 border-t border-indigo-900/60 flex flex-col md:flex-row justify-between items-center text-xs text-indigo-300 gap-4">
            <p>&copy; 2026 MSBTE Notes &amp; Info. All rights reserved.</p>
            <div class="flex items-center gap-6">
                <a href="/start.html" class="hover:text-white transition-colors">Start Here</a>
                <a href="/blog/" class="hover:text-white transition-colors">Blog</a>
                <a href="/sitemap" class="hover:text-white transition-colors">Sitemap</a>
                <a href="/privacy-policy.html" class="hover:text-white transition-colors">Privacy</a>
            </div>
        </div>
    </footer>

    <!-- Client-side Logic for Fast Subject Finder and Semester Filter -->
    <script>
        const subjectsData = {subjects_json};

        // Navigation drawer & dropdown logic
        window.toggleMobileMenu = function() {{
            const menu = document.getElementById('mobileNav');
            const menuIcon = document.getElementById('menuIcon');
            const closeIcon = document.getElementById('closeIcon');
            const button = document.querySelector('.mobile-menu-button');
            if (!menu) return;

            const isClosed = menu.classList.contains('translate-x-full');
            if (isClosed) {{
                menu.classList.remove('translate-x-full');
                if (menuIcon) menuIcon.classList.add('hidden');
                if (closeIcon) closeIcon.classList.remove('hidden');
                if (button) button.setAttribute('aria-expanded', 'true');
                document.body.style.overflow = 'hidden';
            }} else {{
                menu.classList.add('translate-x-full');
                if (menuIcon) menuIcon.classList.remove('hidden');
                if (closeIcon) closeIcon.classList.add('hidden');
                if (button) button.setAttribute('aria-expanded', 'false');
                document.body.style.overflow = '';
            }}
        }};

        window.toggleMobileSubmenu = function(submenuId, arrowId) {{
            const submenu = document.getElementById(submenuId);
            const arrow = document.getElementById(arrowId);
            if (!submenu) return;
            const isHidden = submenu.classList.contains('hidden');
            if (isHidden) {{
                submenu.classList.remove('hidden');
                if (arrow) arrow.classList.add('rotate-180');
            }} else {{
                submenu.classList.add('hidden');
                if (arrow) arrow.classList.remove('rotate-180');
            }}
        }};

        window.toggleDropdown = function(btn, event) {{
            if (event) event.stopPropagation();
            const parent = btn.closest('.nav-dropdown');
            if (!parent) return;
            const isOpen = parent.classList.contains('is-open');
            document.querySelectorAll('.nav-dropdown').forEach(d => {{
                if (d !== parent) {{
                    d.classList.remove('is-open');
                    const b = d.querySelector('button[aria-expanded]');
                    if (b) b.setAttribute('aria-expanded', 'false');
                }}
            }});
            if (isOpen) {{
                parent.classList.remove('is-open');
                btn.setAttribute('aria-expanded', 'false');
            }} else {{
                parent.classList.add('is-open');
                btn.setAttribute('aria-expanded', 'true');
            }}
        }};

        document.addEventListener('click', (e) => {{
            if (!e.target.closest('.nav-dropdown')) {{
                document.querySelectorAll('.nav-dropdown').forEach(d => {{
                    d.classList.remove('is-open');
                    const b = d.querySelector('button[aria-expanded]');
                    if (b) b.setAttribute('aria-expanded', 'false');
                }});
            }}
        }});

        // Semester Matrix Data Mapping
        const branchSemesterMap = [
            {{ name: 'Computer Engineering', slug: 'Computer', code: 'CO', color: 'indigo' }},
            {{ name: 'Information Technology', slug: 'Information-Technology', code: 'IF', color: 'purple' }},
            {{ name: 'AI & Machine Learning', slug: 'AI-ML', code: 'AN', color: 'pink' }},
            {{ name: 'Mechanical Engineering', slug: 'Mechanical-Engineering', code: 'ME', color: 'amber' }},
            {{ name: 'Civil Engineering', slug: 'Civil', code: 'CE', color: 'emerald' }},
            {{ name: 'Electrical Engineering', slug: 'Electrical-Engineering', code: 'EE', color: 'yellow' }},
            {{ name: 'Electronics & TC', slug: 'ETC-Engineering', code: 'EJ', color: 'teal' }}
        ];

        function renderSemesterLinks(semNum) {{
            const grid = document.getElementById('semester-links-grid');
            if (!grid) return;
            
            grid.innerHTML = branchSemesterMap.map(b => {{
                return `
                    <a href="/Branches/${{b.slug}}-Semester-${{semNum}}.html" class="p-3.5 bg-gray-50 hover:bg-blue-50 border border-gray-200/80 hover:border-blue-200 rounded-xl transition flex items-center justify-between group min-h-[44px]">
                        <div class="flex items-center gap-2.5">
                            <span class="w-8 h-8 rounded-lg bg-white border border-gray-200 font-bold text-xs flex items-center justify-center text-gray-700 group-hover:text-blue-600 shadow-sm">${{b.code}}</span>
                            <div>
                                <h4 class="text-sm font-bold text-gray-900 group-hover:text-blue-600 transition leading-tight">${{b.name}}</h4>
                                <span class="text-[11px] text-gray-500">Semester ${{semNum}} Curriculum</span>
                            </div>
                        </div>
                        <span class="text-gray-400 group-hover:text-blue-600 group-hover:translate-x-1 transition-transform text-sm">&rarr;</span>
                    </a>
                `;
            }}).join('');
        }}

        // Setup Semester Buttons
        document.querySelectorAll('.sem-btn').forEach(btn => {{
            btn.addEventListener('click', () => {{
                document.querySelectorAll('.sem-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                renderSemesterLinks(btn.getAttribute('data-sem'));
            }});
        }});

        // Render initial Semester 1
        renderSemesterLinks(1);

        // Instant Subject Finder Logic
        const searchInput = document.getElementById('subject-search-input');
        const clearBtn = document.getElementById('subject-search-clear');
        const resultsBox = document.getElementById('search-results-box');
        const resultsCount = document.getElementById('search-results-count');
        const resultsList = document.getElementById('search-results-list');

        function highlightMatch(text, query) {{
            if (!query) return text;
            const safeQuery = query.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&');
            return text.replace(new RegExp(`(${{safeQuery}})`, 'gi'), '<mark>$1</mark>');
        }}

        function executeSearch(query) {{
            const q = query.trim().toLowerCase();
            if (!q) {{
                resultsBox.classList.add('hidden');
                clearBtn.classList.add('hidden');
                return;
            }}

            clearBtn.classList.remove('hidden');
            resultsBox.classList.remove('hidden');

            const matches = subjectsData.filter(s => {{
                return s.code.includes(q) ||
                       s.name.toLowerCase().includes(q) ||
                       s.branches.toLowerCase().includes(q) ||
                       s.semester.toLowerCase().includes(q);
            }});

            resultsCount.textContent = `Found ${{matches.length}} matching subject${{matches.length === 1 ? '' : 's'}} for "${{query}}"`;

            if (matches.length === 0) {{
                resultsList.innerHTML = `
                    <div class="text-center py-6 text-gray-500 text-sm">
                        No subject found matching "${{query}}". Try searching by 6-digit MSBTE code (e.g. 313301) or short name.
                    </div>
                `;
                return;
            }}

            resultsList.innerHTML = matches.slice(0, 15).map(s => {{
                let actionPills = [];
                if (s.links.syllabus) {{
                    actionPills.push(`<a href="${{s.links.syllabus}}" class="px-2.5 py-1 text-xs font-semibold rounded-md bg-blue-50 text-blue-700 hover:bg-blue-100 border border-blue-200 transition">📖 Syllabus</a>`);
                }}
                if (s.links.notes) {{
                    actionPills.push(`<a href="${{s.links.notes}}" class="px-2.5 py-1 text-xs font-semibold rounded-md bg-indigo-50 text-indigo-700 hover:bg-indigo-100 border border-indigo-200 transition">📝 Notes</a>`);
                }}
                if (s.links.pyq) {{
                    actionPills.push(`<a href="${{s.links.pyq}}" class="px-2.5 py-1 text-xs font-semibold rounded-md bg-rose-50 text-rose-700 hover:bg-rose-100 border border-rose-200 transition">📄 PYQ Papers</a>`);
                }}
                if (s.links.model_answer) {{
                    actionPills.push(`<a href="${{s.links.model_answer}}" class="px-2.5 py-1 text-xs font-semibold rounded-md bg-emerald-50 text-emerald-700 hover:bg-emerald-100 border border-emerald-200 transition">💡 Model Answer</a>`);
                }}
                if (s.links.syllabus_pdf) {{
                    actionPills.push(`<a href="${{s.links.syllabus_pdf}}" target="_blank" rel="noopener noreferrer" class="px-2.5 py-1 text-xs font-semibold rounded-md bg-gray-100 text-gray-700 hover:bg-gray-200 transition">📥 PDF</a>`);
                }}

                return `
                    <div class="p-3.5 bg-gray-50 hover:bg-white rounded-xl border border-gray-200/90 transition shadow-sm">
                        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                            <div>
                                <div class="flex items-center gap-2 mb-1">
                                    <span class="font-mono text-xs font-bold px-2 py-0.5 rounded bg-blue-100 text-blue-800">${{s.code}}</span>
                                    <span class="text-xs font-semibold text-gray-500">${{s.semester}} • ${{s.branches}}</span>
                                </div>
                                <h4 class="text-sm font-bold text-gray-900">${{highlightMatch(s.name, query)}}</h4>
                            </div>
                            <div class="flex flex-wrap items-center gap-1.5 mt-2 sm:mt-0">
                                ${{actionPills.join('')}}
                            </div>
                        </div>
                    </div>
                `;
            }}).join('');
        }}

        if (searchInput) {{
            searchInput.addEventListener('input', (e) => executeSearch(e.target.value));
            searchInput.addEventListener('keydown', (e) => {{
                if (e.key === 'Escape') {{
                    searchInput.value = '';
                    executeSearch('');
                }}
            }});
        }}

        if (clearBtn) {{
            clearBtn.addEventListener('click', () => {{
                searchInput.value = '';
                executeSearch('');
                searchInput.focus();
            }});
        }}

        document.querySelectorAll('.quick-chip').forEach(chip => {{
            chip.addEventListener('click', () => {{
                const term = chip.getAttribute('data-term');
                searchInput.value = term;
                executeSearch(term);
                searchInput.focus();
            }});
        }});
    </script>
</body>

</html>
"""

    with open('start.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Successfully generated start.html with {len(subjects)} indexed subjects.")

if __name__ == '__main__':
    generate_start_html()
