#!/usr/bin/env python3
"""
MSBTE K-Scheme PYQ Pages Generator (Data-Enriched, Mobile-Responsive & UI/UX Refined)
Generates:
1. 116 High-Performance, SEO/GEO/AEO-Optimized Subject PYQ Pages in /pyq/
2. Master PYQ Hub Portal in /pyq/index.html with Live Search, Branch, Semester & Course Type Filters
3. Direct Download Links (uc?export=download) with Exact File Sizes (KB/MB)
4. Dedicated 5-Unit Syllabus Breakdown Cards & High-Frequency Repeated Board Questions
5. Exact UI/UX parity with Notes/osy-k-scheme-notes.html (.res-card, quick jump bar, animated chevron FAQs, blue theme footer)
6. Fix for clean URL resolution: direct .html links and pyq/{slug}/index.html directory folders
7. Catalogs: /pyq/resources.json, /Notes/resources.json, and /pyq/all_drive_papers.json (734 Drive papers)
8. Sitemap entries in /sitemap.xml & 301 Redirects in /_redirects
"""

import os
import re
import csv
import json
import sys
import xml.etree.ElementTree as ET

# Ensure scripts directory is in path for subject_seo_data import
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPTS_DIR)
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from subject_seo_data import SUBJECT_SEO

CSV_PATH = os.path.join(BASE_DIR, 'data', 'pyq_data.csv')
DRIVE_CSV_PATH = os.path.join(r'C:/Users/bitbu/.gemini/antigravity/brain/90f0981b-055f-4fb4-9ee8-bf6b73c20543/.user_uploaded/media_1794080585428_d92d687e.csv')
PYQ_DIR = os.path.join(BASE_DIR, 'pyq')
THUMBS_DIR = os.path.join(BASE_DIR, 'resourse', 'note-thumbs')
PYQ_PNG_DIR = os.path.join(BASE_DIR, 'resourse', 'pyq')
NOTES_DIR = os.path.join(BASE_DIR, 'Notes')
SITEMAP_PATH = os.path.join(BASE_DIR, 'sitemap.xml')
REDIRECTS_PATH = os.path.join(BASE_DIR, '_redirects')
NOTES_RESOURCES_PATH = os.path.join(NOTES_DIR, 'resources.json')
PYQ_RESOURCES_PATH = os.path.join(PYQ_DIR, 'resources.json')
ALL_DRIVE_PAPERS_PATH = os.path.join(PYQ_DIR, 'all_drive_papers.json')

AVAILABLE_PYQ_PNGS = set(os.listdir(PYQ_PNG_DIR)) if os.path.exists(PYQ_PNG_DIR) else set()
AVAILABLE_NOTE_FILES = [f for f in os.listdir(NOTES_DIR) if f.endswith('.html')] if os.path.exists(NOTES_DIR) else []

BRANCH_ORDER = ['CM', 'IF', 'AI', 'ME', 'CE', 'EE', 'EJ']

BRANCH_INFO = {
    'AI': {
        'name': 'Artificial Intelligence & Machine Learning',
        'short': 'AI & ML',
        'badge_bg': 'bg-purple-100',
        'badge_text': 'text-purple-800',
        'border': 'border-purple-200'
    },
    'CE': {
        'name': 'Civil Engineering',
        'short': 'Civil',
        'badge_bg': 'bg-yellow-100',
        'badge_text': 'text-yellow-800',
        'border': 'border-yellow-200'
    },
    'CM': {
        'name': 'Computer Engineering',
        'short': 'Computer',
        'badge_bg': 'bg-blue-100',
        'badge_text': 'text-blue-800',
        'border': 'border-blue-200'
    },
    'EE': {
        'name': 'Electrical Engineering',
        'short': 'Electrical',
        'badge_bg': 'bg-amber-100',
        'badge_text': 'text-amber-800',
        'border': 'border-amber-200'
    },
    'EJ': {
        'name': 'Electronics & Telecommunication',
        'short': 'E&TC',
        'badge_bg': 'bg-red-100',
        'badge_text': 'text-red-800',
        'border': 'border-red-200'
    },
    'IF': {
        'name': 'Information Technology',
        'short': 'IT',
        'badge_bg': 'bg-cyan-100',
        'badge_text': 'text-cyan-800',
        'border': 'border-cyan-200'
    },
    'ME': {
        'name': 'Mechanical Engineering',
        'short': 'Mechanical',
        'badge_bg': 'bg-green-100',
        'badge_text': 'text-green-800',
        'border': 'border-green-200'
    }
}

SEM_NAMES = {
    1: '1st Semester',
    2: '2nd Semester',
    3: '3rd Semester',
    4: '4th Semester',
    5: '5th Semester',
    6: '6th Semester'
}

ACADEMIC_YEARS = {
    1: 'First Year (FY)',
    2: 'First Year (FY)',
    3: 'Second Year (SY)',
    4: 'Second Year (SY)',
    5: 'Third Year (TY)',
    6: 'Third Year (TY)'
}

PALETTES = [
    ('#2563EB', '#1D4ED8'),  # Blue
    ('#059669', '#047857'),  # Emerald
    ('#7C3AED', '#6D28D9'),  # Purple
    ('#D97706', '#B45309'),  # Amber
    ('#DC2626', '#B91C1C'),  # Red
    ('#0891B2', '#0E7490'),  # Cyan
    ('#4F46E5', '#4338CA'),  # Indigo
    ('#0D9488', '#0F766E'),  # Teal
]

WHATSAPP_IMP_URL = "https://wa.me/917083236221?text=Hello%2C%20I%20want%20the%20MSBTE%20Important%20Question%20Bank"

def create_slug(text):
    text = text.lower()
    text = re.sub(r'[\(\)]', '', text)
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def extract_drive_id(url):
    m = re.search(r'/d/([a-zA-Z0-9_-]+)', url)
    if m:
        return m.group(1)
    m = re.search(r'id=([a-zA-Z0-9_-]+)', url)
    if m:
        return m.group(1)
    return ''

def format_size(size_kb_str):
    try:
        val = float(size_kb_str)
        if val >= 1024:
            return f"{val/1024:.1f} MB"
        else:
            return f"{int(round(val))} KB"
    except (ValueError, TypeError):
        return ""

def get_matching_notes_file(code, slug):
    for fn in AVAILABLE_NOTE_FILES:
        if code in fn:
            return fn
    slug_core = re.sub(r'^\d+-', '', slug)
    for fn in AVAILABLE_NOTE_FILES:
        if slug_core in fn:
            return fn
    return None

def get_subject_thumbnail(code, name, slug, subject_ids):
    candidates = []
    candidates.append(f"{code}.png")
    for sid in subject_ids:
        candidates.append(f"{sid}.png")
        candidates.append(f"{sid.lower()}.png")
        parts = sid.split('-')
        if len(parts) == 2:
            candidates.append(f"{parts[1]}.png")
            candidates.append(f"{parts[1].lower()}.png")
    for cand in candidates:
        if cand in AVAILABLE_PYQ_PNGS:
            return f"/resourse/pyq/{cand}"
    svg_candidate = f"pyq-{slug}.svg"
    if os.path.exists(os.path.join(THUMBS_DIR, svg_candidate)):
        return f"/resourse/note-thumbs/{svg_candidate}"
    return f"/resourse/note-thumbs/pyq-{slug}.svg"

def generate_svg(code, name, slug, color_idx):
    svg_filename = f"pyq-{slug}.svg"
    svg_path = os.path.join(THUMBS_DIR, svg_filename)
    if os.path.exists(svg_path):
        return
    c1, c2 = PALETTES[color_idx % len(PALETTES)]
    disp_name = name[:36] + "..." if len(name) > 38 else name
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{c1}"/>
      <stop offset="100%" stop-color="{c2}"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="630" fill="url(#bg)"/>
  <rect x="60" y="60" width="1080" height="510" rx="24" fill="#ffffff" fill-opacity="0.08" stroke="#ffffff" stroke-opacity="0.2" stroke-width="2"/>
  <rect x="90" y="90" width="160" height="42" rx="21" fill="#ffffff" fill-opacity="0.2"/>
  <text x="170" y="117" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="700" fill="#ffffff" text-anchor="middle" letter-spacing="1.5">MSBTE K-SCHEME</text>
  <text x="100" y="270" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="108" font-weight="900" fill="#ffffff" letter-spacing="-2">{code}</text>
  <text x="100" y="340" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="34" font-weight="700" fill="#ffffff">{disp_name}</text>
  <text x="100" y="390" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="22" font-weight="500" fill="#ffffff" fill-opacity="0.85">Previous Year Question Papers • Summer 2026 &amp; Winter 2025</text>
  <g transform="translate(100, 450)">
    <rect x="0" y="0" width="170" height="40" rx="8" fill="#ffffff"/>
    <text x="85" y="25" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="700" fill="{c1}" text-anchor="middle">OFFICIAL PAPERS</text>
    <rect x="185" y="0" width="130" height="40" rx="8" fill="#ffffff" fill-opacity="0.2"/>
    <text x="250" y="25" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="600" fill="#ffffff" text-anchor="middle">70 MARKS</text>
  </g>
</svg>'''
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)

def generate_subject_guide(name, code, sem, branches_str):
    subj_lower = name.lower()
    if any(k in subj_lower for k in ['math', 'modelling', 'statistics', 'calculus']):
        domain_tips = """
        <ul class="list-disc pl-5 space-y-2 text-sm text-gray-700">
            <li><strong>Formula Box:</strong> State formulas explicitly (e.g., standard integration forms, matrix inversion formulas) before plugging in numeric values.</li>
            <li><strong>Step Marks:</strong> MSBTE examiners check intermediate steps. Show substitution, determinant evaluations, and intermediate derivatives clearly.</li>
            <li><strong>Box Final Answers:</strong> Enclose your final answers with correct units to speed up examiner paper evaluation.</li>
            <li><strong>High-Frequency Topics:</strong> Pay special attention to repeated questions on partial fractions, definite integrals, and differential equations.</li>
        </ul>"""
    elif any(k in subj_lower for k in ['c++', 'python', 'java', 'programming', 'software', 'structure', 'data', 'algorithm', 'database', 'network', 'operating', 'cloud', 'security', 'hacking', 'web', 'machine learning']):
        domain_tips = """
        <ul class="list-disc pl-5 space-y-2 text-sm text-gray-700">
            <li><strong>Full Program Syntax:</strong> Write working, well-commented code with complete import/header statements and standard naming conventions.</li>
            <li><strong>Trace Tables:</strong> When tracing loops or recursive calls, draw a dry-run execution table showing variable states at each iteration.</li>
            <li><strong>Neat Architecture Sketches:</strong> Accompany theoretical questions with pencil diagrams (e.g. OSI stack, ER diagram, memory layout).</li>
            <li><strong>Differences in Tables:</strong> For comparison questions (e.g., Process vs Thread, TCP vs UDP), write at least 5 distinct comparison parameters in a table.</li>
        </ul>"""
    elif any(k in subj_lower for k in ['electronic', 'electrical', 'circuit', 'power', 'motor', 'transformer', 'machine', 'microcontroller', 'microprocessor', 'communication', 'vlsi', 'switchgear', 'transmission']):
        domain_tips = """
        <ul class="list-disc pl-5 space-y-2 text-sm text-gray-700">
            <li><strong>Pencil Circuit Diagrams:</strong> Draw neat diagrams with clear component values, polarity signs, and ground references.</li>
            <li><strong>Pinouts &amp; Registers:</strong> Clearly label IC pin numbers, bus structures, and register flags for microprocessor/controller questions.</li>
            <li><strong>Governing Equations:</strong> State basic laws (Kirchhoff's laws, Ohm's law, transformer turns ratio) before substituting values.</li>
            <li><strong>Operational Modes:</strong> Explain working principles step-by-step using numbered points for conduction and cutoff cycles.</li>
        </ul>"""
    elif any(k in subj_lower for k in ['mechanic', 'drawing', 'thermal', 'manufacturing', 'cad', 'fluid', 'automobile', 'hvac', 'machine elements']):
        domain_tips = """
        <ul class="list-disc pl-5 space-y-2 text-sm text-gray-700">
            <li><strong>Free Body Diagrams (FBD):</strong> Isolate components and show all active forces, normal reactions, and friction arrows.</li>
            <li><strong>Thermodynamic Cycles:</strong> Sketch neat P-v and T-s diagrams with numbered state points and cycle directions.</li>
            <li><strong>Standard BIS Conventions:</strong> Adhere strictly to projection rules, center lines, section hatching, and dimensioning standards.</li>
            <li><strong>Process Sequences:</strong> Break down manufacturing operations into chronological, numbered stages with tool descriptions.</li>
        </ul>"""
    elif any(k in subj_lower for k in ['civil', 'building', 'survey', 'concrete', 'highway', 'soil', 'structure', 'hydraulic', 'bridge', 'water', 'costing']):
        domain_tips = """
        <ul class="list-disc pl-5 space-y-2 text-sm text-gray-700">
            <li><strong>IS Code Standards:</strong> Cite relevant Indian Standards (IS 456, IS 800) and specify permissible stresses and concrete grades.</li>
            <li><strong>Neat Structural Sketches:</strong> Sketch reinforced concrete sections with proper rebar callouts, cover specifications, and stirrups.</li>
            <li><strong>Tabular Reductions:</strong> In Surveying and Levelling questions, maintain exact arithmetic checks (Sum BS - Sum FS = Last RL - First RL).</li>
            <li><strong>Field Applications:</strong> Highlight practical construction remedies and soil classification criteria in theoretical explanations.</li>
        </ul>"""
    else:
        domain_tips = """
        <ul class="list-disc pl-5 space-y-2 text-sm text-gray-700">
            <li><strong>Structured Headings:</strong> Break answers into Definition, Working Principle, Advantages, Disadvantages, and Real-World Applications.</li>
            <li><strong>Labelled Block Diagrams:</strong> MSBTE marking guidelines allocate up to 50% of question marks to clear, labelled schematic diagrams.</li>
            <li><strong>Comparison Tables:</strong> Present differentiating features in side-by-side comparative tables with at least 4 to 6 criteria.</li>
            <li><strong>Target Question 1:</strong> Thoroughly revise short conceptual questions to secure guaranteed passing marks in the first 20 minutes.</li>
        </ul>"""

    return f"""
    <div class="bg-blue-50/60 rounded-xl p-5 border border-blue-100 my-4">
        <h3 class="text-base font-bold text-blue-900 mb-2 flex items-center gap-2">
            <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            Subject-Specific Scoring Strategy for {name} ({code})
        </h3>
        {domain_tips}
    </div>"""

NAV_HTML = """    <!-- Header Navigation -->
    <nav class="bg-white shadow fixed top-0 left-0 right-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <!-- Left: Logo -->
                <div class="flex items-center">
                    <a href="/" class="flex items-center text-blue-600 font-bold text-xl font-display">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 mr-2" viewBox="0 0 576 512" fill="currentColor">
                            <path d="M249.6 471.5c10.8 3.8 22.4-4.1 22.4-15.5V78.6c0-4.2-1.6-8.4-5-11C247.4 52 202.4 32 144 32C93.5 32 46.3 45.3 18.1 56.1C6.8 60.5 0 71.7 0 83.8V454.1c0 11.9 12.8 20.2 24.1 16.5C55.6 460.1 105.5 448 144 448c33.9 0 79 14 105.6 23.5zm76.8 0C353 462 398.1 448 432 448c38.5 0 88.4 12.1 119.9 22.6c11.3 3.8 24.1-4.6 24.1-16.5V83.8c0-12.1-6.8-23.3-18.1-27.6C529.7 45.3 482.5 32 432 32c-58.4 0-103.4 20-123 35.6c-3.3 2.6-5 6.8-5 11V456c0 11.4 11.7 19.3 22.4 15.5z"/>
                        </svg>
                        MSBTE Notes &amp; Info
                    </a>
                </div>

                <!-- Middle: Desktop Nav with Hover & Click Dropdowns -->
                <div class="hidden md:flex space-x-6 items-center">
                    <a href="/" class="hover:text-blue-500 font-medium text-gray-700">Home</a>

                    <!-- Notes & Study Dropdown -->
                    <div class="relative group py-2 nav-dropdown">
                        <button type="button" onclick="toggleDropdown(this, event)" class="flex items-center gap-1 hover:text-blue-500 font-medium text-gray-700 focus:outline-none" aria-haspopup="true" aria-expanded="false">
                            <span>Notes &amp; Study</span>
                            <svg class="w-4 h-4 transition-transform duration-200 group-hover:rotate-180 dropdown-arrow" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                        </button>
                        <div class="dropdown-menu absolute left-0 top-full -mt-1 w-56 bg-white rounded-xl shadow-xl border border-gray-100 py-2 hidden group-hover:block transition-all z-50">
                            <a href="/#notes" class="flex items-center gap-2.5 px-4 py-2.5 text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-600 font-medium transition">
                                <span class="text-base">📝</span>
                                <span>Subject Notes</span>
                            </a>
                            <a href="/pyq/" class="flex items-center gap-2.5 px-4 py-2.5 text-sm text-blue-600 font-bold hover:bg-blue-50 transition">
                                <span class="text-base">📑</span>
                                <span>Question Papers (PYQ)</span>
                            </a>
                            <a href="/video-course/" class="flex items-center gap-2.5 px-4 py-2.5 text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-600 font-medium transition">
                                <span class="text-base">🎥</span>
                                <span>Video Courses</span>
                            </a>
                        </div>
                    </div>

                    <a href="/#departments" class="hover:text-blue-500 font-medium text-gray-700">Departments</a>
                    <a href="/#blogs" class="hover:text-blue-500 font-medium text-gray-700">Blog</a>
                    <a href="/news/" class="hover:text-red-500 font-medium text-gray-700 flex items-center gap-1">
                        <span class="inline-block w-2 h-2 rounded-full bg-red-500 animate-pulse"></span>
                        <span>News</span>
                    </a>
                    <a href="/collegeinfo/" class="hover:text-blue-500 font-medium text-gray-700">Colleges</a>

                    <!-- Jobs & Career Dropdown -->
                    <div class="relative group py-2 nav-dropdown">
                        <button type="button" onclick="toggleDropdown(this, event)" class="flex items-center gap-1 hover:text-blue-500 font-medium text-gray-700 focus:outline-none" aria-haspopup="true" aria-expanded="false">
                            <span>Jobs &amp; Career</span>
                            <svg class="w-4 h-4 transition-transform duration-200 group-hover:rotate-180 dropdown-arrow" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                        </button>
                        <div class="dropdown-menu absolute left-0 top-full -mt-1 w-52 bg-white rounded-xl shadow-xl border border-gray-100 py-2 hidden group-hover:block transition-all z-50">
                            <a href="/jobs/index.html" class="flex items-center gap-2.5 px-4 py-2.5 text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-600 font-medium transition">
                                <span class="text-base">💼</span>
                                <span>Jobs Portal</span>
                            </a>
                            <a href="/internships.html" class="flex items-center gap-2.5 px-4 py-2.5 text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-600 font-medium transition">
                                <span class="text-base">🎓</span>
                                <span>Internships</span>
                            </a>
                        </div>
                    </div>

                    <a href="/about.html" class="hover:text-blue-500 font-medium text-gray-700">About</a>
                    <a href="/contact.html" class="hover:text-blue-500 font-medium text-gray-700">Contact</a>
                </div>

                <!-- Right: Mobile Menu Toggle -->
                <div class="flex items-center md:hidden">
                    <button onclick="toggleMobileMenu()" class="mobile-menu-button p-2 text-gray-600 hover:text-blue-600 focus:outline-none" aria-controls="mobileNav" aria-expanded="false" aria-label="Toggle menu">
                        <svg id="menuIcon" class="h-7 w-7 transition-transform duration-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7"/>
                        </svg>
                        <svg id="closeIcon" class="h-7 w-7 hidden transition-transform duration-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                        </svg>
                    </button>
                </div>
            </div>
        </div>

        <!-- Modern Mobile Navigation Overlay Drawer -->
        <div id="mobileNav" class="fixed inset-0 bg-white z-50 transform translate-x-full transition-transform duration-300 ease-in-out md:hidden overflow-y-auto pt-20 px-6" style="z-index: 9999 !important;">
            <button onclick="toggleMobileMenu()" class="absolute top-5 right-5 p-2 text-gray-600 hover:text-blue-600 focus:outline-none" aria-label="Close menu">
                <svg class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
            </button>

            <div class="flex flex-col space-y-4">
                <a href="/" onclick="toggleMobileMenu()" class="text-xl font-display font-bold text-gray-900 border-b border-gray-100 pb-2">Home</a>

                <!-- Notes Mobile Submenu (Accordion) -->
                <div class="border-b border-gray-100 pb-2">
                    <button type="button" onclick="toggleMobileSubmenu('mobileNotesSubmenu', 'mobileNotesArrow')" class="w-full flex items-center justify-between text-xl font-display font-bold text-gray-900 py-1.5 focus:outline-none">
                        <span class="flex items-center gap-2">
                            <span>Notes &amp; Study</span>
                            <span class="text-xs font-sans font-semibold px-2 py-0.5 rounded-full bg-blue-100 text-blue-700">3 Links</span>
                        </span>
                        <svg id="mobileNotesArrow" class="w-5 h-5 text-gray-500 transition-transform duration-200 transform rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                        </svg>
                    </button>
                    <div id="mobileNotesSubmenu" class="space-y-1 pl-2 pt-1 pb-1 transition-all">
                        <a href="/#notes" onclick="toggleMobileMenu()" class="flex items-center gap-2.5 py-2 px-3 rounded-lg text-base font-medium text-gray-700 hover:bg-blue-50 hover:text-blue-600 transition">
                            <span class="text-lg">📝</span>
                            <div>
                                <div class="font-semibold text-gray-900">Subject Notes</div>
                                <div class="text-xs text-gray-500">Curated notes, unit test IMPs &amp; manuals</div>
                            </div>
                        </a>
                        <a href="/pyq/" onclick="toggleMobileMenu()" class="flex items-center gap-2.5 py-2 px-3 rounded-lg text-base font-bold text-blue-600 bg-blue-50 transition">
                            <span class="text-lg">📑</span>
                            <div>
                                <div class="font-bold text-blue-700">Question Papers (PYQ)</div>
                                <div class="text-xs text-blue-500">Summer 2026 &amp; Winter 2025 papers</div>
                            </div>
                        </a>
                        <a href="/video-course/" onclick="toggleMobileMenu()" class="flex items-center gap-2.5 py-2 px-3 rounded-lg text-base font-medium text-gray-700 hover:bg-blue-50 hover:text-blue-600 transition">
                            <span class="text-lg">🎥</span>
                            <div>
                                <div class="font-semibold text-gray-900">Video Courses</div>
                                <div class="text-xs text-gray-500">Video tutorials and concept lectures</div>
                            </div>
                        </a>
                    </div>
                </div>

                <a href="/#departments" onclick="toggleMobileMenu()" class="text-xl font-display font-bold text-gray-900 border-b border-gray-100 pb-2">Departments</a>
                <a href="/#blogs" onclick="toggleMobileMenu()" class="text-xl font-display font-bold text-gray-900 border-b border-gray-100 pb-2">Blog</a>
                <a href="/news/" onclick="toggleMobileMenu()" class="text-xl font-display font-bold text-red-600 border-b border-gray-100 pb-2 flex items-center justify-between">
                    <span>🔴 Breaking News</span>
                    <span class="text-xs bg-red-100 text-red-700 px-2 py-0.5 rounded-full font-sans font-semibold">Live</span>
                </a>
                <a href="/collegeinfo/" onclick="toggleMobileMenu()" class="text-xl font-display font-bold text-gray-900 border-b border-gray-100 pb-2">Colleges</a>

                <!-- Jobs Mobile Submenu (Accordion) -->
                <div class="border-b border-gray-100 pb-2">
                    <button type="button" onclick="toggleMobileSubmenu('mobileJobsSubmenu', 'mobileJobsArrow')" class="w-full flex items-center justify-between text-xl font-display font-bold text-gray-900 py-1.5 focus:outline-none">
                        <span class="flex items-center gap-2">
                            <span>Jobs &amp; Career</span>
                            <span class="text-xs font-sans font-semibold px-2 py-0.5 rounded-full bg-indigo-100 text-indigo-700">2 Links</span>
                        </span>
                        <svg id="mobileJobsArrow" class="w-5 h-5 text-gray-500 transition-transform duration-200 transform rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                        </svg>
                    </button>
                    <div id="mobileJobsSubmenu" class="space-y-1 pl-2 pt-1 pb-1 transition-all">
                        <a href="/jobs/index.html" onclick="toggleMobileMenu()" class="flex items-center gap-2.5 py-2 px-3 rounded-lg text-base font-medium text-gray-700 hover:bg-blue-50 hover:text-blue-600 transition">
                            <span class="text-lg">💼</span>
                            <div>
                                <div class="font-semibold text-gray-900">Jobs Portal</div>
                                <div class="text-xs text-gray-500">Engineering jobs &amp; campus recruitments</div>
                            </div>
                        </a>
                        <a href="/internships.html" onclick="toggleMobileMenu()" class="flex items-center gap-2.5 py-2 px-3 rounded-lg text-base font-medium text-gray-700 hover:bg-blue-50 hover:text-blue-600 transition">
                            <span class="text-lg">🎓</span>
                            <div>
                                <div class="font-semibold text-gray-900">Internships</div>
                                <div class="text-xs text-gray-500">Verified summer/winter internships</div>
                            </div>
                        </a>
                    </div>
                </div>

                <a href="/about.html" onclick="toggleMobileMenu()" class="text-xl font-display font-bold text-gray-900 border-b border-gray-100 pb-2">About</a>
                <a href="/contact.html" onclick="toggleMobileMenu()" class="text-xl font-display font-bold text-gray-900 border-b border-gray-100 pb-2">Contact</a>

                <div class="pt-4">
                    <a href="https://chat.whatsapp.com/KFcI5VeJOpjLPgp30NXMfQ" target="_blank" rel="noopener noreferrer" class="block w-full bg-green-500 hover:bg-green-600 text-white text-center py-3.5 rounded-xl font-bold shadow-lg shadow-green-200 transition">
                        Join WhatsApp Community
                    </a>
                </div>
            </div>
        </div>
    </nav>"""

NAV_JS = """
        function toggleMobileMenu() {
            const menu = document.getElementById('mobileNav');
            const btn = document.querySelector('.mobile-menu-button');
            const menuIcon = document.getElementById('menuIcon');
            const closeIcon = document.getElementById('closeIcon');
            if (!menu) return;
            const isClosed = menu.classList.contains('translate-x-full');
            if (isClosed) {
                menu.classList.remove('translate-x-full');
                if (menuIcon) menuIcon.classList.add('hidden');
                if (closeIcon) closeIcon.classList.remove('hidden');
                if (btn) btn.setAttribute('aria-expanded', 'true');
                document.body.style.overflow = 'hidden';
            } else {
                menu.classList.add('translate-x-full');
                if (menuIcon) menuIcon.classList.remove('hidden');
                if (closeIcon) closeIcon.classList.remove('hidden');
                if (btn) btn.setAttribute('aria-expanded', 'false');
                document.body.style.overflow = '';
            }
        }

        function toggleMobileSubmenu(submenuId, arrowId) {
            const sub = document.getElementById(submenuId);
            const arr = document.getElementById(arrowId);
            if (!sub) return;
            const isHidden = sub.classList.contains('hidden');
            if (isHidden) {
                sub.classList.remove('hidden');
                if (arr) arr.classList.add('rotate-180');
            } else {
                sub.classList.add('hidden');
                if (arr) arr.classList.remove('rotate-180');
            }
        }

        function toggleDropdown(btn, event) {
            if (event) event.stopPropagation();
            const parent = btn.closest('.nav-dropdown');
            if (!parent) return;
            const isOpen = parent.classList.contains('is-open');
            document.querySelectorAll('.nav-dropdown').forEach(d => {
                if (d !== parent) {
                    d.classList.remove('is-open');
                    const b = d.querySelector('button[aria-expanded]');
                    if (b) b.setAttribute('aria-expanded', 'false');
                }
            });
            if (isOpen) {
                parent.classList.remove('is-open');
                btn.setAttribute('aria-expanded', 'false');
            } else {
                parent.classList.add('is-open');
                btn.setAttribute('aria-expanded', 'true');
            }
        }

        document.addEventListener('click', function (e) {
            if (!e.target.closest('.nav-dropdown')) {
                document.querySelectorAll('.nav-dropdown').forEach(d => {
                    d.classList.remove('is-open');
                    const b = d.querySelector('button[aria-expanded]');
                    if (b) b.setAttribute('aria-expanded', 'false');
                });
            }
        });

        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') {
                document.querySelectorAll('.nav-dropdown').forEach(d => {
                    d.classList.remove('is-open');
                    const b = d.querySelector('button[aria-expanded]');
                    if (b) b.setAttribute('aria-expanded', 'false');
                });
            }
        });
"""

SUBJECT_PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Consent default -->
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag() { dataLayer.push(arguments); }
        gtag('consent', 'default', { 'ad_storage': 'denied', 'analytics_storage': 'denied' });
    </script>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-H5G5CCD95W"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag() { dataLayer.push(arguments); }
        gtag('js', new Date());
        gtag('config', 'G-H5G5CCD95W');
    </script>

    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>__PAGE_TITLE__</title>
    <meta name="description" content="__META_DESC__" />
    <meta name="keywords" content="__META_KEYWORDS__" />
    <meta name="author" content="MSBTE Notes &amp; Info Team" />
    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />

    <link rel="canonical" href="__CANONICAL_URL__" />

    <!-- Open Graph Meta Tags -->
    <meta property="og:title" content="__PAGE_TITLE__" />
    <meta property="og:description" content="__META_DESC__" />
    <meta property="og:url" content="__CANONICAL_URL__" />
    <meta property="og:type" content="article" />
    <meta property="og:image" content="__IMAGE_URL__" />
    <meta property="og:image:width" content="1920" />
    <meta property="og:image:height" content="1080" />
    <meta property="og:site_name" content="MSBTE Notes &amp; Info" />
    <meta property="og:locale" content="en_IN" />

    <!-- Twitter Card Meta Tags -->
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="__PAGE_TITLE__" />
    <meta name="twitter:description" content="__META_DESC__" />
    <meta name="twitter:image" content="__IMAGE_URL__" />
    <meta name="twitter:site" content="@msbtenotes" />

    <!-- Favicon and App Icons -->
    <link rel="apple-touch-icon" sizes="180x180" href="/resourse/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/resourse/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/resourse/favicon-16x16.png">
    <link rel="manifest" href="/resourse/site.webmanifest">
    <link rel="icon" href="/resourse/favicon.ico" type="image/x-icon">

    <!-- Stylesheets & Fonts -->
    <link rel="stylesheet" href="/style.css">
    <link href="https://api.fontshare.com/v2/css?f[]=clash-display@600&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">

    <!-- AdSense Verification Script -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9227354288966999" crossorigin="anonymous"></script>

    <!-- JSON-LD Structured Data -->
    <script type="application/ld+json">
    __SCHEMA_BREADCRUMB__
    </script>
    <script type="application/ld+json">
    __SCHEMA_COURSE__
    </script>
    <script type="application/ld+json">
    __SCHEMA_FAQ__
    </script>

    <style>
        .font-display { font-family: 'Clash Display', sans-serif; }
        .res-card {
            background: #fff;
            border: 1px solid #f1f5f9;
            border-radius: 1rem;
            box-shadow: 0 4px 12px rgba(0,0,0,.03);
            transition: transform .3s ease, box-shadow .3s ease;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .res-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 16px 32px rgba(0,0,0,.07);
        }
        details > summary { list-style: none; cursor: pointer; }
        details > summary::-webkit-details-marker { display: none; }
        .chev { transition: transform .2s ease; }
        details[open] .chev { transform: rotate(180deg); }
        details[open] > summary { color: #2563eb; }
        .pdf-container {
            position: relative;
            width: 100%;
            height: 600px;
            background: #f8fafc;
            border-radius: 1rem;
            overflow: hidden;
            border: 1px solid #e2e8f0;
        }
        .pdf-container iframe {
            width: 100%;
            height: 100%;
            border: none;
        }
        .no-scrollbar::-webkit-scrollbar { display: none; }
        .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
    </style>
</head>

<body class="bg-gray-50 text-gray-900 pt-16 overflow-x-hidden w-full max-w-full">

    __NAV_HTML__

    <!-- Breadcrumb Navigation matching Notes pages -->
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pt-5 pb-2">
        <nav class="flex text-sm" aria-label="Breadcrumb">
            <ol class="flex items-center space-x-1 md:space-x-2 flex-wrap">
                <li class="inline-flex items-center">
                    <a href="/" class="inline-flex items-center font-medium text-gray-700 hover:text-blue-600 transition">
                        <svg class="w-4 h-4 mr-1.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path></svg>Home
                    </a>
                </li>
                <li class="flex items-center">
                    <svg class="w-4 h-4 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
                    <a href="/pyq/" class="ml-1 md:ml-2 font-medium text-gray-700 hover:text-blue-600 transition">Question Papers</a>
                </li>
                <li class="flex items-center min-w-0" aria-current="page">
                    <svg class="w-4 h-4 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
                    <span class="ml-1 md:ml-2 font-medium text-gray-500 max-w-[160px] sm:max-w-xs truncate">__CODE__ - __NAME__</span>
                </li>
            </ol>
        </nav>
    </div>

    <!-- Main Content Container -->
    <main class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-4">

        <!-- Hero Header -->
        <header class="mb-6 text-left border-b border-gray-200 pb-6">
            <div class="flex flex-wrap items-center gap-1.5 mb-3">
                <span class="badge badge-free">K-Scheme</span>
                <span class="badge badge-sem">__SEM_NAME__</span>
                <span class="badge bg-gray-100 text-gray-700 border border-gray-200">Code: __CODE__</span>
                __SUBJECT_TYPE_BADGE__
            </div>

            <h1 class="text-2xl sm:text-3xl lg:text-4xl font-bold text-blue-600 leading-tight break-words font-display">
                __NAME__ (__ABBR__ - __CODE__) Previous Year Question Papers
            </h1>
            
            <p class="mt-3 text-base sm:text-lg text-gray-600 leading-relaxed">
                Download official MSBTE K-Scheme <strong>__NAME__ (__CODE__)</strong> Summer 2026 and Winter 2025 board exam question papers. Free PDF direct download for __ACAD_YEAR__ diploma engineering students.
            </p>

            <!-- Quick Jump Filter Bar -->
            <div class="w-full overflow-x-auto no-scrollbar py-1 mt-5" style="overscroll-behavior-x: contain; -webkit-overflow-scrolling: touch;" aria-label="Jump to section">
                <div class="inline-flex gap-2">
                    <a href="#download-section" class="filter-btn whitespace-nowrap inline-flex items-center gap-2 text-sm hover:border-blue-300 hover:text-blue-600 hover:bg-blue-50">
                        <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                        Question Papers
                    </a>
                    <a href="#preview-section" class="filter-btn whitespace-nowrap inline-flex items-center gap-2 text-sm hover:border-blue-300 hover:text-blue-600 hover:bg-blue-50">
                        <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path></svg>
                        PDF Preview
                    </a>
                    <a href="#syllabus-units" class="filter-btn whitespace-nowrap inline-flex items-center gap-2 text-sm hover:border-blue-300 hover:text-blue-600 hover:bg-blue-50">
                        <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path></svg>
                        Syllabus Units
                    </a>
                    <a href="#repeated-questions" class="filter-btn whitespace-nowrap inline-flex items-center gap-2 text-sm hover:border-blue-300 hover:text-blue-600 hover:bg-blue-50">
                        <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"></path></svg>
                        IMP Questions
                    </a>
                    <a href="#course-spec" class="filter-btn whitespace-nowrap inline-flex items-center gap-2 text-sm hover:border-blue-300 hover:text-blue-600 hover:bg-blue-50">
                        <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                        Exam Pattern
                    </a>
                    <a href="#faqs" class="filter-btn whitespace-nowrap inline-flex items-center gap-2 text-sm hover:border-blue-300 hover:text-blue-600 hover:bg-blue-50">
                        <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                        FAQs
                    </a>
                </div>
            </div>

            <!-- Branch badges -->
            <div class="mt-4 flex flex-wrap items-center gap-1.5">
                <span class="text-xs font-bold text-gray-500 mr-1">Applicable Branches:</span>
                __BRANCH_PILLS_HTML__
            </div>

            <!-- Authentic 1080p Thumbnail Banner -->
            <div class="my-6 rounded-2xl overflow-hidden border border-gray-200 shadow-md bg-gray-100">
                <img src="__THUMB_URL__" alt="MSBTE __CODE__ __NAME__ Question Paper Banner" class="w-full h-auto object-cover" loading="lazy" width="1920" height="1080">
            </div>

            <!-- WhatsApp Question Bank CTA -->
            __WHATSAPP_CTA_HTML__
        </header>

        <!-- Top In-Article Ad -->
        <div class="my-6">
            <ins class="adsbygoogle" style="display:block; text-align:center;" data-ad-layout="in-article"
                 data-ad-format="fluid" data-ad-client="ca-pub-9227354288966999" data-ad-slot="7917907402"></ins>
            <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
        </div>

        <!-- Section 1: Question Papers Download Section -->
        <section id="download-section" class="mt-10 mb-12" aria-labelledby="download-section-title">
            <div class="border-b border-gray-200 pb-3 mb-6 flex items-start gap-3">
                <span class="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center flex-shrink-0">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                </span>
                <div class="min-w-0 flex-1">
                    <h2 id="download-section-title" class="text-2xl sm:text-3xl font-bold text-gray-900 leading-tight font-display break-words">Download Question Paper PDFs</h2>
                    <p class="text-sm text-gray-500 mt-1">Official MSBTE K-Scheme question papers with direct 1-click downloads.</p>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                __DOWNLOAD_CARDS_HTML__
            </div>
        </section>

        <!-- Section 2: Online PDF Preview Section -->
        <section id="preview-section" class="mt-10 mb-12" aria-labelledby="preview-title">
            <div class="border-b border-gray-200 pb-3 mb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
                <div class="flex items-start gap-3">
                    <span class="w-10 h-10 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center flex-shrink-0">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                    </span>
                    <div class="min-w-0">
                        <h2 id="preview-title" class="text-2xl sm:text-3xl font-bold text-gray-900 leading-tight font-display break-words">Online PDF Preview</h2>
                        <p class="text-sm text-gray-500 mt-1">Read question papers directly inside your browser without taking up device storage.</p>
                    </div>
                </div>
                <div class="flex items-center gap-2 self-start sm:self-auto" id="previewTabs">
                    <span id="activePreviewLabel" class="text-xs font-bold text-blue-600 bg-blue-50 px-3 py-1.5 rounded-lg border border-blue-200">
                        Viewing: Summer 2026
                    </span>
                </div>
            </div>

            <div class="pdf-container shadow-md">
                <iframe id="pdfViewer" src="https://drive.google.com/file/d/__PRIMARY_ID__/preview" allow="autoplay" title="__NAME__ Question Paper Preview"></iframe>
            </div>
            
            <div class="mt-3 text-right">
                <a id="fullscreenLink" href="https://drive.google.com/file/d/__PRIMARY_ID__/view?usp=sharing" target="_blank" rel="noopener noreferrer"
                   class="text-xs font-semibold text-blue-600 hover:text-blue-800 underline inline-flex items-center gap-1">
                    Open Fullscreen in Google Drive &rarr;
                </a>
            </div>
        </section>

        <!-- Branded YouTube Promo Banner matching Notes -->
        <aside class="bg-white border border-gray-100 p-5 rounded-2xl shadow-sm mb-10 flex flex-col md:flex-row items-center gap-4">
            <span class="bg-red-600 text-white rounded-full p-3 flex-shrink-0">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path d="M19.615 3.184c-3.604-.246-11.631-.245-15.23 0-3.897.266-4.356 2.62-4.385 8.816.029 6.185.484 8.549 4.385 8.816 3.6.245 11.626.246 15.23 0 3.897-.266 4.356-2.62 4.385-8.816-.029-6.185-.484-8.549-4.385-8.816zm-10.615 12.816v-8l8 3.993-8 4.007z"/></svg>
            </span>
            <div class="flex-grow text-center md:text-left">
                <h3 class="font-bold text-gray-900 text-lg">Subscribe to Our YouTube Channel</h3>
                <p class="text-gray-600 text-sm mt-1">MSBTE updates, video lectures, and exam tips from top educators.</p>
            </div>
            <a href="https://www.youtube.com/@msbte-notes-and-info" target="_blank" rel="noopener noreferrer"
               class="bg-red-600 hover:bg-red-700 text-white font-semibold py-3 px-6 rounded-lg transition flex-shrink-0 whitespace-nowrap text-sm shadow-sm w-full md:w-auto text-center">
                Subscribe Channel
            </a>
        </aside>

        <!-- Section 3: Prescribed Syllabus Units -->
        <section id="syllabus-units" class="mt-10 mb-12" aria-labelledby="syllabus-units-title">
            <div class="border-b border-gray-200 pb-3 mb-6 flex items-start gap-3">
                <span class="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center flex-shrink-0">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path></svg>
                </span>
                <div class="min-w-0 flex-1">
                    <h2 id="syllabus-units-title" class="text-2xl sm:text-3xl font-bold text-gray-900 leading-tight font-display break-words">Prescribed Syllabus Units</h2>
                    <p class="text-sm text-gray-500 mt-1">Official MSBTE K-Scheme course curriculum and unit weightage breakdown.</p>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                __SYLLABUS_CARDS_HTML__
            </div>
        </section>

        <!-- Section 4: Repeated Board Exam Questions -->
        <section id="repeated-questions" class="mt-10 mb-12" aria-labelledby="repeated-questions-title">
            <div class="border-b border-gray-200 pb-3 mb-6 flex items-start gap-3">
                <span class="w-10 h-10 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center flex-shrink-0">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"></path></svg>
                </span>
                <div class="min-w-0 flex-1">
                    <h2 id="repeated-questions-title" class="text-2xl sm:text-3xl font-bold text-gray-900 leading-tight font-display break-words">Repeated Board Exam Questions</h2>
                    <p class="text-sm text-gray-500 mt-1">Frequently asked questions with typical MSBTE mark allocations.</p>
                </div>
            </div>

            <div class="space-y-3">
                __REPEATED_QUESTIONS_HTML__
            </div>
        </section>

        <!-- Section 5: Course Specification & Examination Pattern -->
        <section id="course-spec" class="mb-10 bg-white rounded-2xl p-6 border border-gray-200 shadow-sm" aria-labelledby="course-spec-title">
            <h2 id="course-spec-title" class="text-xl font-bold text-gray-900 font-display mb-4 flex items-center gap-2">
                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path></svg>
                Course Specification &amp; Examination Pattern
            </h2>
            <div class="overflow-x-auto">
                <table class="w-full text-left text-sm text-gray-600 border-collapse">
                    <tbody>
                        <tr class="border-b border-gray-100">
                            <th class="py-2.5 font-semibold text-gray-800 w-1/3">Course Title</th>
                            <td class="py-2.5 font-bold text-blue-600">__NAME__ (__ABBR__)</td>
                        </tr>
                        <tr class="border-b border-gray-100 bg-gray-50">
                            <th class="py-2.5 font-semibold text-gray-800">Course Code</th>
                            <td class="py-2.5 font-mono font-bold text-gray-900">__CODE__</td>
                        </tr>
                        <tr class="border-b border-gray-100">
                            <th class="py-2.5 font-semibold text-gray-800">Curriculum Scheme</th>
                            <td class="py-2.5">MSBTE K-Scheme (NEP 2020 Aligned)</td>
                        </tr>
                        <tr class="border-b border-gray-100 bg-gray-50">
                            <th class="py-2.5 font-semibold text-gray-800">Course Classification</th>
                            <td class="py-2.5 font-semibold text-gray-900">__SUBJECT_TYPE__ Subject</td>
                        </tr>
                        <tr class="border-b border-gray-100">
                            <th class="py-2.5 font-semibold text-gray-800">Semester &amp; Year</th>
                            <td class="py-2.5">__SEM_NAME__ &bull; __ACAD_YEAR__</td>
                        </tr>
                        <tr class="border-b border-gray-100 bg-gray-50">
                            <th class="py-2.5 font-semibold text-gray-800">Theory Marks (ESE)</th>
                            <td class="py-2.5"><strong>70 Marks</strong> (End Semester Board Exam)</td>
                        </tr>
                        <tr class="border-b border-gray-100">
                            <th class="py-2.5 font-semibold text-gray-800">Passing Criteria</th>
                            <td class="py-2.5"><span class="text-green-700 font-bold">28 Marks (40%)</span> in Theory Paper</td>
                        </tr>
                        <tr class="border-b border-gray-100 bg-gray-50">
                            <th class="py-2.5 font-semibold text-gray-800">Exam Duration</th>
                            <td class="py-2.5">3.0 Hours (180 Minutes)</td>
                        </tr>
                        <tr class="border-b border-gray-100">
                            <th class="py-2.5 font-semibold text-gray-800">Verified Paper Size</th>
                            <td class="py-2.5 text-gray-700 font-mono text-xs">__SIZES_SUMMARY__</td>
                        </tr>
                        <tr class="bg-gray-50">
                            <th class="py-2.5 font-semibold text-gray-800">Prescribed Branches</th>
                            <td class="py-2.5">__BRANCHES_STR__</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </section>

        <!-- Deep-Dive Study & Exam Preparation Guide -->
        <article class="mb-10 bg-white rounded-2xl p-6 sm:p-8 border border-gray-200 shadow-sm prose prose-blue max-w-none">
            <h2 class="text-2xl font-bold text-gray-900 font-display mb-4">
                How to Prepare for __NAME__ (__CODE__) Using Previous Papers
            </h2>
            <div class="text-gray-700 space-y-4">
                <p>
                    Scoring high marks in <strong>__NAME__ (__CODE__)</strong> requires a systematic review of repeated board examination patterns. Rather than attempting to memorize the entire syllabus at the last minute, top-performing polytechnic students analyze question papers from recent exam cycles like <strong>Summer 2026</strong> and <strong>Winter 2025</strong> to understand MSBTE evaluator expectations.
                </p>

                __SUBJECT_GUIDE_HTML__

                <h3 class="text-xl font-bold text-gray-900 font-display mt-6 mb-2">Effective 4-Step Revision Routine</h3>
                <ol class="list-decimal pl-5 space-y-2 text-sm sm:text-base">
                    <li><strong>Map Questions to Syllabus Units:</strong> Categorize every question from Summer 2026 into specific course outcomes (COs) to uncover which units carry maximum optional weight.</li>
                    <li><strong>Master Standard Question 1 Compulsory Topics:</strong> Question 1 contains short conceptual 2-mark questions (attempt 5 out of 6). Revise standard definitions, unit conversions, and block sketches to lock in these 10 marks quickly.</li>
                    <li><strong>Write Under Timed Exam Simulation:</strong> Solve the complete 70-mark paper within a strict 3-hour window. This builds speed and ensures you have sufficient buffer time to re-check numerical calculations.</li>
                    <li><strong>Cross-Check with Official Marking Schemes:</strong> Evaluate your handwritten solutions against official MSBTE model answers. Ensure every required keyword, formula derivation step, and labelled pencil sketch is present.</li>
                </ol>
            </div>
        </article>

        <!-- Middle Ad Placement -->
        <div class="my-8">
            <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-9227354288966999"
                 data-ad-slot="1275037071" data-ad-format="auto" data-full-width-responsive="true"></ins>
            <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
        </div>

        <!-- Section 7: Frequently Asked Questions (FAQ) Section -->
        <section id="faqs" class="mt-12 mb-10" aria-labelledby="faqs-title">
            <div class="border-b border-gray-200 pb-3 mb-6 flex items-start gap-3">
                <span class="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center flex-shrink-0">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                </span>
                <div class="min-w-0 flex-1">
                    <h2 id="faqs-title" class="text-2xl sm:text-3xl font-bold text-gray-900 leading-tight font-display break-words">Frequently Asked Questions (__CODE__)</h2>
                    <p class="text-sm text-gray-500 mt-1">Key answers on question papers, passing criteria, and examination strategy.</p>
                </div>
            </div>

            <div class="space-y-4">
                __FAQ_ITEMS_HTML__
            </div>
        </section>

        <!-- Social Share Bar -->
        <div class="my-8 text-center bg-white p-6 rounded-2xl border border-gray-200 shadow-sm">
            <h3 class="text-base font-bold text-gray-800 mb-3 font-display">Share __NAME__ PYQ with Classmates</h3>
            <div class="flex justify-center gap-3 flex-wrap">
                <a href="#" id="whatsappShare" target="_blank" rel="noopener noreferrer"
                   class="inline-flex items-center gap-2 bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-full font-semibold text-xs sm:text-sm transition shadow-sm">
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 448 512"><path d="M380.9 97.1C339 55.1 283.2 32 223.9 32c-122.4 0-222 99.6-222 222 0 39.1 10.2 77.3 29.6 111L0 480l117.7-30.9c32.4 17.7 68.9 27 106.1 27h.1c122.3 0 224.1-99.6 224.1-222 0-59.3-25.2-115-67.1-157zm-157 341.6c-33.2 0-65.7-8.9-94-25.7l-6.7-4-69.8 18.3L72 359.2l-4.4-7c-18.5-29.4-28.2-63.3-28.2-98.2 0-101.7 82.8-184.5 184.6-184.5 49.3 0 95.6 19.2 130.4 54.1 34.8 34.9 56.2 81.2 56.1 130.5 0 101.8-84.9 184.6-186.6 184.6zm101.2-138.2c-5.5-2.8-32.8-16.2-37.9-18-5.1-1.9-8.8-2.8-12.5 2.8-3.7 5.6-14.3 18-17.6 21.8-3.2 3.7-6.5 4.2-12 1.4-32.6-16.3-54-29.1-75.5-66-5.7-9.8 5.7-9.1 16.3-30.3 1.8-3.7 .9-6.9-.5-9.7-1.4-2.8-12.5-30.1-17.1-41.2-4.5-10.8-9.1-9.3-12.5-9.5-3.2-.2-6.9-.2-10.6-.2-3.7 0-9.7 1.4-14.8 6.9-5.1 5.6-19.4 19-19.4 46.3 0 27.3 19.9 53.7 22.6 57.4 2.8 3.7 39.1 59.7 94.8 83.8 35.2 15.2 49 16.5 66.6 13.9 10.7-1.6 32.8-13.4 37.4-26.4 4.6-13 4.6-24.1 3.2-26.4-1.3-2.5-5-3.9-10.5-6.6z"/></svg>
                    WhatsApp
                </a>
                <a href="#" id="telegramShare" target="_blank" rel="noopener noreferrer"
                   class="inline-flex items-center gap-2 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-full font-semibold text-xs sm:text-sm transition shadow-sm">
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 496 512"><path d="M248 8C111 8 0 119 0 256S111 504 248 504 496 393 496 256 385 8 248 8zM363 176.7c-3.7 39.2-19.9 134.4-28.1 178.3-3.5 18.6-10.3 24.8-16.9 25.4-14.4 1.3-25.3-9.5-39.3-18.7-21.8-14.3-34.2-23.2-55.3-37.2-24.5-16.1-8.6-25 5.3-39.5 3.7-3.8 67.1-61.5 68.3-66.7 .2-.7 .3-3.1-1.2-4.4s-3.6-.8-5.1-.5q-3.3 .7-104.6 69.1-14.8 10.2-26.9 9.9c-8.9-.2-25.9-5-38.6-9.1-15.5-5-27.9-7.7-26.8-16.3q.8-6.7 18.5-13.7 108.4-47.2 144.6-62.3c68.9-28.6 83.2-33.6 92.5-33.8 2.1 0 6.6 .5 9.6 2.9a10.5 10.5 0 0 1 3.5 6.7A43.8 43.8 0 0 1 363 176.7z"/></svg>
                    Telegram
                </a>
                <button onclick="copyLink()"
                        class="inline-flex items-center gap-2 bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-full font-semibold text-xs sm:text-sm transition shadow-sm">
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 448 512"><path d="M208 0L332.1 0c12.7 0 24.9 5.1 33.9 14.1l67.9 67.9c9 9 14.1 21.2 14.1 33.9L448 336c0 26.5-21.5 48-48 48l-192 0c-26.5 0-48-21.5-48-48l0-288c0-26.5 21.5-48 48-48zM48 128l80 0 0 64-64 0 0 256 192 0 0-32 64 0 0 48c0 26.5-21.5 48-48 48L48 512c-26.5 0-48-21.5-48-48L0 176c0-26.5 21.5-48 48-48z"/></svg>
                    Copy Link
                </button>
            </div>
        </div>

        <!-- Responsive Display Ad -->
        <div class="my-8">
            <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-9227354288966999"
                 data-ad-slot="1275037071" data-ad-format="auto" data-full-width-responsive="true"></ins>
            <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
        </div>

        <!-- Related Blogs & Notes Section -->
        <section id="related-blogs" class="mt-12 w-full overflow-hidden">
            <h2 class="text-2xl font-bold text-gray-900 font-display mb-6 text-center">More Study Resources &amp; Guides</h2>
            <div id="relatedContainer" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6"></div>
            <div id="relatedPagination" class="flex flex-wrap justify-center items-center gap-2 mt-8"></div>
        </section>

    </main>

    <!-- Site Theme Footer matching Notes & Homepage -->
    <footer class="bg-blue-600 text-white mt-16 py-12 w-full max-w-full overflow-hidden">
        <div class="max-w-6xl mx-auto px-4 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8">
            <div>
                <h3 class="text-xl font-semibold mb-4 font-display">About MSBTE Notes &amp; Info</h3>
                <p class="text-sm leading-relaxed text-blue-100">
                    We provide free and premium study materials, verified question papers, and syllabus schemes for MSBTE diploma engineering students across all polytechnic colleges in Maharashtra.
                </p>
            </div>
            <div>
                <h3 class="text-xl font-semibold mb-4 font-display">Quick Links</h3>
                <ul class="space-y-2 text-sm text-blue-100">
                    <li><a href="/" class="hover:underline">Home</a></li>
                    <li><a href="/pyq/" class="hover:underline font-bold text-white">Question Papers (PYQ)</a></li>
                    <li><a href="/#notes" class="hover:underline">Subject Notes</a></li>
                    <li><a href="/video-course/" class="hover:underline">Video Courses</a></li>
                    <li><a href="/jobs/index.html" class="hover:underline">Jobs Portal</a></li>
                    <li><a href="/internships.html" class="hover:underline">Internships</a></li>
                    <li><a href="/about.html" class="hover:underline">About Us</a></li>
                    <li><a href="/contact.html" class="hover:underline">Contact</a></li>
                    <li><a href="/privacy-policy.html" class="hover:underline">Privacy Policy</a></li>
                </ul>
            </div>
            <div>
                <h3 class="text-xl font-semibold mb-4 font-display">Student Support</h3>
                <p class="text-sm mb-2 text-blue-100">&#128231; info.mraaglave@gmail.com</p>
                <p class="text-sm mb-2 text-blue-100">&#128241; +91 70832 36221</p>
                <a href="https://chat.whatsapp.com/KFcI5VeJOpjLPgp30NXMfQ" target="_blank" rel="noopener noreferrer"
                   class="inline-block mt-4 bg-white text-blue-600 px-5 py-2.5 rounded-full font-semibold hover:bg-gray-100 shadow transition text-sm">
                    Join WhatsApp Community &rarr;
                </a>
            </div>
        </div>
        <div class="flex justify-center mt-8">
            <a href="https://www.producthunt.com/products/msbte-notes-info/reviews/new?utm_source=badge-product_review&utm_medium=badge&utm_source=badge-msbte&#0045;notes&#0045;info"
               target="_blank">
                <img src="https://api.producthunt.com/widgets/embed-image/v1/product_review.svg?product_id=1131454&theme=light"
                     alt="MSBTE Notes &amp; Info on Product Hunt" style="width: 250px; height: 54px;" width="250" height="54" />
            </a>
        </div>
        <div class="text-center mt-10 text-sm text-blue-100 border-t border-blue-500/40 pt-8">
            <p>
                <a href="/about.html" class="hover:underline">About</a> |
                <a href="/sitemap.xml" class="hover:underline">Sitemap</a> |
                <a href="/privacy-policy.html" class="hover:underline">Privacy Policy</a> |
                <a href="/contact.html" class="hover:underline">Contact</a>
            </p>
            <p class="mt-2 text-xs text-blue-200">Not affiliated with or endorsed by MSBTE. Official information is available at msbte.ac.in.</p>
            <p class="mt-1 text-xs text-blue-200">&copy; 2026 MSBTE Notes &amp; Info. All rights reserved.</p>
        </div>
    </footer>

    <!-- Interactive Scripts -->
    <script>
__NAV_JS__

        function setPreview(driveId, label) {
            const viewer = document.getElementById('pdfViewer');
            const fullLink = document.getElementById('fullscreenLink');
            const activeLabel = document.getElementById('activePreviewLabel');

            viewer.src = `https://drive.google.com/file/d/${driveId}/preview`;
            fullLink.href = `https://drive.google.com/file/d/${driveId}/view?usp=sharing`;
            activeLabel.innerText = `Viewing: ${label}`;

            viewer.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }

        function copyLink() {
            navigator.clipboard.writeText(window.location.href).then(() => {
                alert('Page link copied to clipboard!');
            }).catch(() => {
                prompt('Copy this link:', window.location.href);
            });
        }

        // Setup share URLs
        document.addEventListener('DOMContentLoaded', function() {
            const shareUrl = encodeURIComponent(window.location.href);
            const shareTitle = encodeURIComponent("__PAGE_TITLE__");

            const waBtn = document.getElementById('whatsappShare');
            if (waBtn) waBtn.href = `https://api.whatsapp.com/send?text=${shareTitle}%20${shareUrl}`;

            const tgBtn = document.getElementById('telegramShare');
            if (tgBtn) tgBtn.href = `https://t.me/share/url?url=${shareUrl}&text=${shareTitle}`;
        });
    </script>

    <!-- Related Blogs Loader Script -->
    <script src="/blog.js" defer></script>
    <script src="../whatsapp-popup.js" defer></script>
</body>
</html>"""

HUB_PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Consent default -->
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag() { dataLayer.push(arguments); }
        gtag('consent', 'default', { 'ad_storage': 'denied', 'analytics_storage': 'denied' });
    </script>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-H5G5CCD95W"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag() { dataLayer.push(arguments); }
        gtag('js', new Date());
        gtag('config', 'G-H5G5CCD95W');
    </script>

    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>MSBTE K-Scheme Question Papers (PYQ) — All Subjects &amp; Branches PDF Download</title>
    <meta name="description" content="Download free MSBTE K-Scheme previous year question papers (PYQs) for all 116 subjects across Computer, IT, AI-ML, Mechanical, Civil, Electrical, and E&TC engineering." />
    <meta name="keywords" content="MSBTE question paper, MSBTE PYQ, msbte k scheme pyq, msbte previous year question papers, diploma question paper 2026, summer 2026 question paper, winter 2025 question paper, msbte model answer paper" />
    <meta name="author" content="MSBTE Notes &amp; Info Team" />
    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />

    <link rel="canonical" href="https://msbtenotes-info.netlify.app/pyq/" />

    <!-- Open Graph Meta Tags -->
    <meta property="og:title" content="MSBTE K-Scheme Question Papers (PYQ) — All Subjects &amp; Branches" />
    <meta property="og:description" content="Download free MSBTE K-Scheme previous year question papers (PYQs) for all 116 diploma engineering subjects." />
    <meta property="og:url" content="https://msbtenotes-info.netlify.app/pyq/" />
    <meta property="og:type" content="website" />
    <meta property="og:image" content="https://msbtenotes-info.netlify.app/resourse/MSBTE%20NOTES%20AND%20INFORMATION.png" />

    <!-- Twitter Card Meta Tags -->
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="MSBTE K-Scheme Question Papers (PYQ) Hub" />
    <meta name="twitter:description" content="Download free MSBTE K-Scheme previous year question papers (PYQs) for all 116 diploma engineering subjects." />
    <meta name="twitter:image" content="https://msbtenotes-info.netlify.app/resourse/MSBTE%20NOTES%20AND%20INFORMATION.png" />

    <!-- Favicon and App Icons -->
    <link rel="apple-touch-icon" sizes="180x180" href="/resourse/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/resourse/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/resourse/favicon-16x16.png">
    <link rel="manifest" href="/resourse/site.webmanifest">
    <link rel="icon" href="/resourse/favicon.ico" type="image/x-icon">

    <!-- Stylesheets & Fonts -->
    <link rel="stylesheet" href="/style.css">
    <link href="https://api.fontshare.com/v2/css?f[]=clash-display@600&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">

    <!-- AdSense Verification Script -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9227354288966999" crossorigin="anonymous"></script>

    <style>
        .font-display { font-family: 'Clash Display', sans-serif; }
        .filter-btn.active {
            background-color: #2563EB;
            color: #FFFFFF;
            border-color: #2563EB;
        }
        .pyq-hub-card {
            background: #fff;
            border: 1px solid #f1f5f9;
            border-radius: 1rem;
            box-shadow: 0 4px 12px rgba(0,0,0,.03);
            transition: transform .3s ease, box-shadow .3s ease;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .pyq-hub-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 16px 32px rgba(0,0,0,.07);
        }
    </style>
</head>

<body class="bg-gray-50 text-gray-900 pt-16 overflow-x-hidden w-full max-w-full">

    __NAV_HTML__

    <!-- Hero Header -->
    <header class="bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-700 text-white py-12 px-4 sm:px-6 lg:px-8 text-center">
        <div class="max-w-4xl mx-auto">
            <span class="inline-block bg-white/20 backdrop-blur-md px-3.5 py-1 rounded-full text-xs font-bold tracking-wide uppercase mb-3">
                📚 116 Subjects &bull; Direct 1-Click Downloads
            </span>
            <h1 class="text-3xl sm:text-4xl lg:text-5xl font-bold font-display leading-tight mb-3">
                MSBTE K-Scheme Question Papers (PYQ)
            </h1>
            <p class="text-base sm:text-lg text-blue-100 max-w-2xl mx-auto leading-relaxed">
                Download verified MSBTE board exam question papers for 1st, 2nd, 3rd, 4th, 5th, and 6th semester across all engineering departments.
            </p>
        </div>
    </header>

    <!-- Main Container -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

        <!-- Search & Filters Container -->
        <div class="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm mb-8 space-y-4">
            <!-- Search Bar -->
            <div class="relative">
                <input type="text" id="searchInput"
                       placeholder="Search by course code (e.g. 311302) or subject name..."
                       class="w-full pl-11 pr-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none text-sm sm:text-base">
                <svg class="w-5 h-5 text-gray-400 absolute left-3.5 top-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
            </div>

            <!-- Filter Controls -->
            <div class="space-y-3 pt-2 border-t border-gray-100">
                <!-- Branch Filters -->
                <div class="flex items-center gap-2 overflow-x-auto pb-1" id="branchFilters">
                    <span class="text-xs font-bold text-gray-500 uppercase tracking-wider whitespace-nowrap mr-1">Branch:</span>
                    <button class="filter-btn active text-xs whitespace-nowrap" data-val="all">All Branches</button>
                    <button class="filter-btn text-xs whitespace-nowrap" data-val="cm">Computer</button>
                    <button class="filter-btn text-xs whitespace-nowrap" data-val="if">IT</button>
                    <button class="filter-btn text-xs whitespace-nowrap" data-val="ai">AI &amp; ML</button>
                    <button class="filter-btn text-xs whitespace-nowrap" data-val="me">Mechanical</button>
                    <button class="filter-btn text-xs whitespace-nowrap" data-val="ce">Civil</button>
                    <button class="filter-btn text-xs whitespace-nowrap" data-val="ee">Electrical</button>
                    <button class="filter-btn text-xs whitespace-nowrap" data-val="ej">E&amp;TC</button>
                </div>

                <!-- Semester Filters -->
                <div class="flex items-center gap-2 overflow-x-auto pb-1" id="semFilters">
                    <span class="text-xs font-bold text-gray-500 uppercase tracking-wider whitespace-nowrap mr-1">Semester:</span>
                    <button class="filter-btn active text-xs whitespace-nowrap" data-val="all">All Semesters</button>
                    <button class="filter-btn text-xs whitespace-nowrap" data-val="1">Sem 1</button>
                    <button class="filter-btn text-xs whitespace-nowrap" data-val="2">Sem 2</button>
                    <button class="filter-btn text-xs whitespace-nowrap" data-val="3">Sem 3</button>
                    <button class="filter-btn text-xs whitespace-nowrap" data-val="4">Sem 4</button>
                    <button class="filter-btn text-xs whitespace-nowrap" data-val="5">Sem 5</button>
                    <button class="filter-btn text-xs whitespace-nowrap" data-val="6">Sem 6</button>
                </div>

                <!-- Course Type Filters -->
                <div class="flex items-center gap-2 overflow-x-auto pb-1" id="typeFilters">
                    <span class="text-xs font-bold text-gray-500 uppercase tracking-wider whitespace-nowrap mr-1">Type:</span>
                    <button class="filter-btn active text-xs whitespace-nowrap" data-val="all">All Courses</button>
                    <button class="filter-btn text-xs whitespace-nowrap" data-val="core">Core Subjects</button>
                    <button class="filter-btn text-xs whitespace-nowrap" data-val="elective">Electives</button>
                </div>
            </div>
        </div>

        <!-- Live Results Counter -->
        <div class="flex items-center justify-between mb-6 px-1">
            <p class="text-sm text-gray-600">
                Showing <strong id="visibleCount" class="text-blue-600">__CARDS_COUNT__</strong> subjects
            </p>
            <span class="text-xs text-gray-500">K-Scheme 2025–2026 Examination Series</span>
        </div>

        <!-- Cards Grid -->
        <div id="cardsGrid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            __CARDS_HTML__
        </div>

        <div id="noResults" class="hidden py-16 text-center">
            <p class="text-lg text-gray-500 font-semibold mb-2">No question papers found matching your filters.</p>
            <p class="text-sm text-gray-400">Try searching with a different course code, subject name, or resetting filters.</p>
        </div>

    </main>

    <!-- Site Theme Footer matching Notes & Homepage -->
    <footer class="bg-blue-600 text-white mt-16 py-12 w-full max-w-full overflow-hidden">
        <div class="max-w-6xl mx-auto px-4 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8">
            <div>
                <h3 class="text-xl font-semibold mb-4 font-display">About MSBTE Notes &amp; Info</h3>
                <p class="text-sm leading-relaxed text-blue-100">
                    We provide free and premium study materials, verified question papers, and syllabus schemes for MSBTE diploma engineering students across all polytechnic colleges in Maharashtra.
                </p>
            </div>
            <div>
                <h3 class="text-xl font-semibold mb-4 font-display">Quick Links</h3>
                <ul class="space-y-2 text-sm text-blue-100">
                    <li><a href="/" class="hover:underline">Home</a></li>
                    <li><a href="/pyq/" class="hover:underline font-bold text-white">Question Papers (PYQ)</a></li>
                    <li><a href="/#notes" class="hover:underline">Subject Notes</a></li>
                    <li><a href="/video-course/" class="hover:underline">Video Courses</a></li>
                    <li><a href="/jobs/index.html" class="hover:underline">Jobs Portal</a></li>
                    <li><a href="/internships.html" class="hover:underline">Internships</a></li>
                    <li><a href="/about.html" class="hover:underline">About Us</a></li>
                    <li><a href="/contact.html" class="hover:underline">Contact</a></li>
                    <li><a href="/privacy-policy.html" class="hover:underline">Privacy Policy</a></li>
                </ul>
            </div>
            <div>
                <h3 class="text-xl font-semibold mb-4 font-display">Student Support</h3>
                <p class="text-sm mb-2 text-blue-100">&#128231; info.mraaglave@gmail.com</p>
                <p class="text-sm mb-2 text-blue-100">&#128241; +91 70832 36221</p>
                <a href="https://chat.whatsapp.com/KFcI5VeJOpjLPgp30NXMfQ" target="_blank" rel="noopener noreferrer"
                   class="inline-block mt-4 bg-white text-blue-600 px-5 py-2.5 rounded-full font-semibold hover:bg-gray-100 shadow transition text-sm">
                    Join WhatsApp Community &rarr;
                </a>
            </div>
        </div>
        <div class="flex justify-center mt-8">
            <a href="https://www.producthunt.com/products/msbte-notes-info/reviews/new?utm_source=badge-product_review&utm_medium=badge&utm_source=badge-msbte&#0045;notes&#0045;info"
               target="_blank">
                <img src="https://api.producthunt.com/widgets/embed-image/v1/product_review.svg?product_id=1131454&theme=light"
                     alt="MSBTE Notes &amp; Info on Product Hunt" style="width: 250px; height: 54px;" width="250" height="54" />
            </a>
        </div>
        <div class="text-center mt-10 text-sm text-blue-100 border-t border-blue-500/40 pt-8">
            <p>
                <a href="/about.html" class="hover:underline">About</a> |
                <a href="/sitemap.xml" class="hover:underline">Sitemap</a> |
                <a href="/privacy-policy.html" class="hover:underline">Privacy Policy</a> |
                <a href="/contact.html" class="hover:underline">Contact</a>
            </p>
            <p class="mt-2 text-xs text-blue-200">Not affiliated with or endorsed by MSBTE. Official information is available at msbte.ac.in.</p>
            <p class="mt-1 text-xs text-blue-200">&copy; 2026 MSBTE Notes &amp; Info. All rights reserved.</p>
        </div>
    </footer>

    <!-- Interactive Client Filtering Script -->
    <script>
__NAV_JS__

        const searchInput = document.getElementById('searchInput');
        const cardsGrid = document.getElementById('cardsGrid');
        const cards = Array.from(cardsGrid.getElementsByClassName('pyq-hub-card'));
        const visibleCountSpan = document.getElementById('visibleCount');
        const noResultsDiv = document.getElementById('noResults');

        let activeBranch = 'all';
        let activeSem = 'all';
        let activeType = 'all';

        function filterCards() {
            const query = searchInput.value.toLowerCase().trim();
            let visible = 0;

            cards.forEach(card => {
                const code = card.getAttribute('data-code') || '';
                const name = card.getAttribute('data-name') || '';
                const sem = card.getAttribute('data-sem') || '';
                const branches = card.getAttribute('data-branches') || '';
                const type = card.getAttribute('data-type') || '';

                const matchesQuery = !query || code.includes(query) || name.includes(query);
                const matchesBranch = (activeBranch === 'all') || branches.includes(activeBranch);
                const matchesSem = (activeSem === 'all') || (sem === activeSem);
                const matchesType = (activeType === 'all') || (type === activeType);

                if (matchesQuery && matchesBranch && matchesSem && matchesType) {
                    card.style.display = '';
                    visible++;
                } else {
                    card.style.display = 'none';
                }
            });

            visibleCountSpan.innerText = visible;
            if (visible === 0) {
                noResultsDiv.classList.remove('hidden');
            } else {
                noResultsDiv.classList.add('hidden');
            }
        }

        searchInput.addEventListener('input', filterCards);

        // Branch filter buttons
        document.querySelectorAll('#branchFilters .filter-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                document.querySelectorAll('#branchFilters .filter-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                activeBranch = this.getAttribute('data-val');
                filterCards();
            });
        });

        // Semester filter buttons
        document.querySelectorAll('#semFilters .filter-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                document.querySelectorAll('#semFilters .filter-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                activeSem = this.getAttribute('data-val');
                filterCards();
            });
        });

        // Subject Type filter buttons
        document.querySelectorAll('#typeFilters .filter-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                document.querySelectorAll('#typeFilters .filter-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                activeType = this.getAttribute('data-val');
                filterCards();
            });
        });
    </script>
    <script src="../whatsapp-popup.js" defer></script>
</body>
</html>"""


def main():
    print("Loading enriched CSV data from:", CSV_PATH)
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))

    print(f"Total rows in CSV: {len(rows)}")

    by_code = {}
    sid_redirects = {}

    for r in rows:
        tag = r['tags'].strip()
        code_m = re.search(r'\b(3\d{5})\b', tag)
        code = code_m.group(1) if code_m else 'UNKNOWN'

        raw_title = r['title'].strip()
        clean_name = re.sub(r'\s+(Summer|Winter)\s+\d{4}\s+Question\s+Paper', '', raw_title, flags=re.IGNORECASE).strip()

        sid = r['subjectId'].strip()
        sem = int(r['semester'])
        branch_code = sid.split('-')[0]
        year = r['year'].strip()
        season = 'Summer' if 'Summer' in raw_title else 'Winter'
        paper_label = f"{season} {year}"
        drive_url = r['driveUrl'].strip()
        drive_id = extract_drive_id(drive_url)

        direct_dl = r.get('directDownloadUrl', f"https://drive.google.com/uc?export=download&id={drive_id}").strip()
        file_size_kb = r.get('fileSizeKB', '').strip()
        subj_type = r.get('subjectType', 'Core').strip()
        file_name = r.get('fileName', '').strip()

        if code not in by_code:
            slug = f"{code}-{create_slug(clean_name)}"
            by_code[code] = {
                'code': code,
                'name': clean_name,
                'slug': slug,
                'sem': sem,
                'subject_type': subj_type,
                'branches': set(),
                'subject_ids': set(),
                'papers': {}
            }

        by_code[code]['branches'].add(branch_code)
        by_code[code]['subject_ids'].add(sid)
        by_code[code]['papers'][paper_label] = {
            'url': drive_url,
            'direct_url': direct_dl,
            'size_kb': file_size_kb,
            'file_name': file_name,
            'id': drive_id,
            'year': year,
            'season': season
        }

        sid_redirects[sid.lower()] = by_code[code]['slug']

    print(f"Total unique subject codes identified: {len(by_code)}")
    print(f"Total subjectId alias redirects: {len(sid_redirects)}")

    os.makedirs(PYQ_DIR, exist_ok=True)
    os.makedirs(THUMBS_DIR, exist_ok=True)

    catalog_entries = []

    # Generate each subject page
    for idx, (code, data) in enumerate(sorted(by_code.items())):
        slug = data['slug']
        name = data['name']
        sem = data['sem']
        sem_name = SEM_NAMES.get(sem, f'Semester {sem}')
        acad_year = ACADEMIC_YEARS.get(sem, 'Diploma Year')
        subject_type = data.get('subject_type', 'Core')

        # Load bespoke SEO data
        subj_seo = SUBJECT_SEO.get(code, {})
        abbr = subj_seo.get('abbr', '')
        units_list = subj_seo.get('units', [])
        questions_list = subj_seo.get('repeated_questions', [])
        faqs_list = subj_seo.get('custom_faq', [])
        keywords_list = subj_seo.get('keywords', [])

        branch_codes_sorted = sorted(list(data['branches']))
        branch_full_names = [BRANCH_INFO.get(b, {}).get('name', b) for b in branch_codes_sorted]
        branch_shorts = [BRANCH_INFO.get(b, {}).get('short', b) for b in branch_codes_sorted]
        branches_str = ", ".join(branch_full_names)
        branches_short_str = ", ".join(branch_shorts)

        sids_sorted = sorted(list(data['subject_ids']))
        sids_str = ", ".join(sids_sorted)

        thumb_url = get_subject_thumbnail(code, name, slug, data['subject_ids'])
        generate_svg(code, name, slug, idx)

        papers = data['papers']
        summer_2026 = papers.get('Summer 2026')
        winter_2025 = papers.get('Winter 2025')

        primary_paper = summer_2026 if summer_2026 else winter_2025
        primary_id = primary_paper['id'] if primary_paper else ''

        download_cards_html = ""

        # Download card: Summer 2026
        if summer_2026:
            s_url = summer_2026['url']
            s_direct_url = summer_2026.get('direct_url', s_url)
            s_id = summer_2026['id']
            s_size = format_size(summer_2026.get('size_kb', ''))
            s_size_badge = f"PDF • {s_size}" if s_size else "Official Board QP"
            download_cards_html += f"""
            <article class="res-card p-5 sm:p-6 overflow-hidden">
                <div>
                    <div class="flex items-center justify-between gap-2 mb-3">
                        <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold bg-blue-50 text-blue-700 border border-blue-200">
                            ☀️ Summer 2026
                        </span>
                        <span class="text-xs font-semibold text-gray-500">{s_size_badge}</span>
                    </div>
                    <h3 class="text-lg font-bold text-gray-900 font-display mb-2">{name} — Summer 2026</h3>
                    <p class="text-sm text-gray-600 mb-5">Original MSBTE K-Scheme question paper with 70-mark theory distribution.</p>
                </div>
                <div class="flex flex-col sm:flex-row gap-3 pt-4 border-t border-gray-100">
                    <a href="{s_direct_url}" target="_blank" rel="noopener noreferrer" download
                       class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-3 rounded-lg font-semibold transition text-sm flex items-center justify-center gap-2 shadow-sm flex-1">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
                        Download PDF
                    </a>
                    <button onclick="setPreview('{s_id}', 'Summer 2026')"
                            class="bg-gray-100 hover:bg-gray-200 text-gray-800 px-4 py-3 rounded-lg font-semibold transition text-sm flex items-center justify-center gap-1.5 border border-gray-200">
                        <svg class="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path></svg>
                        Preview
                    </button>
                </div>
            </article>"""

        # Download card: Winter 2025
        if winter_2025:
            w_url = winter_2025['url']
            w_direct_url = winter_2025.get('direct_url', w_url)
            w_id = winter_2025['id']
            w_size = format_size(winter_2025.get('size_kb', ''))
            w_size_badge = f"PDF • {w_size}" if w_size else "Official Board QP"
            download_cards_html += f"""
            <article class="res-card p-5 sm:p-6 overflow-hidden">
                <div>
                    <div class="flex items-center justify-between gap-2 mb-3">
                        <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold bg-indigo-50 text-indigo-700 border border-indigo-200">
                            ❄️ Winter 2025
                        </span>
                        <span class="text-xs font-semibold text-gray-500">{w_size_badge}</span>
                    </div>
                    <h3 class="text-lg font-bold text-gray-900 font-display mb-2">{name} — Winter 2025</h3>
                    <p class="text-sm text-gray-600 mb-5">Original MSBTE K-Scheme Winter examination question paper with full marking scheme.</p>
                </div>
                <div class="flex flex-col sm:flex-row gap-3 pt-4 border-t border-gray-100">
                    <a href="{w_direct_url}" target="_blank" rel="noopener noreferrer" download
                       class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-3 rounded-lg font-semibold transition text-sm flex items-center justify-center gap-2 shadow-sm flex-1">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
                        Download PDF
                    </a>
                    <button onclick="setPreview('{w_id}', 'Winter 2025')"
                            class="bg-gray-100 hover:bg-gray-200 text-gray-800 px-4 py-3 rounded-lg font-semibold transition text-sm flex items-center justify-center gap-1.5 border border-gray-200">
                        <svg class="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path></svg>
                        Preview
                    </button>
                </div>
            </article>"""
        else:
            # Informative card explaining even-semester examination pattern for 6th sem
            download_cards_html += f"""
            <article class="res-card p-5 sm:p-6 overflow-hidden bg-gray-50 border-dashed">
                <div>
                    <div class="flex items-center justify-between gap-2 mb-3">
                        <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold bg-gray-200 text-gray-700">
                            ℹ️ Winter 2025 — Not Applicable
                        </span>
                        <span class="text-xs font-semibold text-gray-500">Even Semester Exam</span>
                    </div>
                    <h3 class="text-lg font-bold text-gray-800 font-display mb-2">{sem_name} Curriculum Note</h3>
                    <p class="text-sm text-gray-600 mb-4">Under MSBTE K-Scheme regulations, {sem_name.lower()} subjects are evaluated exclusively in Summer examination sessions. Winter 2025 board examinations were not conducted for this course.</p>
                </div>
                <div class="pt-4 border-t border-gray-200">
                    <a href="{WHATSAPP_IMP_URL}" target="_blank" rel="noopener noreferrer"
                       class="text-xs font-bold text-green-700 bg-green-50 hover:bg-green-100 border border-green-200 px-3.5 py-2.5 rounded-xl flex items-center justify-center gap-1.5 transition">
                        <svg class="w-3.5 h-3.5 text-green-600" fill="currentColor" viewBox="0 0 448 512"><path d="M380.9 97.1C339 55.1 283.2 32 223.9 32c-122.4 0-222 99.6-222 222 0 39.1 10.2 77.3 29.6 111L0 480l117.7-30.9c32.4 17.7 68.9 27 106.1 27h.1c122.3 0 224.1-99.6 224.1-222 0-59.3-25.2-115-67.1-157zm-157 341.6c-33.2 0-65.7-8.9-94-25.7l-6.7-4-69.8 18.3L72 359.2l-4.4-7c-18.5-29.4-28.2-63.3-28.2-98.2 0-101.7 82.8-184.5 184.6-184.5 49.3 0 95.6 19.2 130.4 54.1 34.8 34.9 56.2 81.2 56.1 130.5 0 101.8-84.9 184.6-186.6 184.6zm101.2-138.2c-5.5-2.8-32.8-16.2-37.9-18-5.1-1.9-8.8-2.8-12.5 2.8-3.7 5.6-14.3 18-17.6 21.8-3.2 3.7-6.5 4.2-12 1.4-32.6-16.3-54-29.1-75.5-66-5.7-9.8 5.7-9.1 16.3-30.3 1.8-3.7 .9-6.9-.5-9.7-1.4-2.8-12.5-30.1-17.1-41.2-4.5-10.8-9.1-9.3-12.5-9.5-3.2-.2-6.9-.2-10.6-.2-3.7 0-9.7 1.4-14.8 6.9-5.1 5.6-19.4 19-19.4 46.3 0 27.3 19.9 53.7 22.6 57.4 2.8 3.7 39.1 59.7 94.8 83.8 35.2 15.2 49 16.5 66.6 13.9 10.7-1.6 32.8-13.4 37.4-26.4 4.6-13 4.6-24.1 3.2-26.4-1.3-2.5-5-3.9-10.5-6.6z"/></svg>
                        Request I-Scheme Papers on WhatsApp ↗
                    </a>
                </div>
            </article>"""

        # Branch pills HTML
        branch_pills_html = "".join([
            f'<span class="inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-semibold {BRANCH_INFO.get(b, {}).get("badge_bg", "bg-gray-100")} {BRANCH_INFO.get(b, {}).get("badge_text", "text-gray-800")} border {BRANCH_INFO.get(b, {}).get("border", "border-gray-200")}">{BRANCH_INFO.get(b, {}).get("short", b)}</span>'
            for b in branch_codes_sorted
        ])

        # Subject Type Badge
        subject_type_badge = f'<span class="badge {"bg-purple-100 text-purple-800 border-purple-200" if subject_type == "Elective" else "bg-blue-100 text-blue-800 border-blue-200"}">{"📙 Elective Subject" if subject_type == "Elective" else "📘 Core Subject"}</span>'

        # Verified Sizes Summary
        sizes_parts = []
        if summer_2026:
            sizes_parts.append(f"Summer 2026: {format_size(summer_2026.get('size_kb', ''))}")
        if winter_2025:
            sizes_parts.append(f"Winter 2025: {format_size(winter_2025.get('size_kb', ''))}")
        sizes_summary = " &bull; ".join(sizes_parts) if sizes_parts else "Original MSBTE PDF"

        # Subject guide content
        subject_guide_html = generate_subject_guide(name, code, sem, branches_short_str)

        # Build Syllabus Cards (Section 3)
        syllabus_cards_html = ""
        for u_idx, u_info in enumerate(units_list):
            u_num = u_idx + 1
            if isinstance(u_info, (list, tuple)):
                u_title = u_info[0]
                u_desc = u_info[1] if len(u_info) > 1 else "Prescribed curriculum topics and competencies."
                u_marks = u_info[2] if len(u_info) > 2 else "14 Marks"
            else:
                u_title = str(u_info)
                u_desc = "Prescribed curriculum topics and competencies."
                u_marks = "14 Marks"

            syllabus_cards_html += f"""
            <article class="res-card p-5 sm:p-6 overflow-hidden">
                <div>
                    <div class="flex items-start justify-between gap-3 mb-3">
                        <div class="flex items-center gap-3 min-w-0">
                            <span class="w-9 h-9 rounded-xl bg-blue-600 text-white font-bold text-sm flex items-center justify-center font-display flex-shrink-0">{u_num}</span>
                            <h3 class="text-base sm:text-lg font-bold text-blue-900 leading-snug break-words">{u_title}</h3>
                        </div>
                        <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-blue-50 text-blue-700 flex-shrink-0">{u_marks}</span>
                    </div>
                    <p class="text-sm text-gray-600 leading-relaxed">{u_desc}</p>
                </div>
            </article>"""

        # Build Repeated Questions Cards (Section 4)
        repeated_questions_html = ""
        for q_idx, q_item in enumerate(questions_list):
            q_text = q_item.get('q', '')
            q_marks = q_item.get('marks', '4 Marks')
            badge_color = "bg-purple-100 text-purple-800" if "6" in q_marks else "bg-amber-100 text-amber-800"
            repeated_questions_html += f"""
            <div class="res-card p-4 sm:p-5">
                <div class="flex items-start justify-between gap-3">
                    <div class="flex items-start gap-3">
                        <span class="w-7 h-7 rounded-lg bg-gray-100 text-gray-700 font-bold text-xs flex items-center justify-center flex-shrink-0 mt-0.5 font-display">Q{q_idx + 1}</span>
                        <p class="text-sm sm:text-base text-gray-800 font-medium leading-relaxed">{q_text}</p>
                    </div>
                    <span class="inline-flex items-center px-2.5 py-1 rounded-md text-xs font-bold {badge_color} flex-shrink-0">{q_marks}</span>
                </div>
            </div>"""

        # Build FAQ Items (Section 7)
        faq_items_html = ""
        schema_faq_entities = []
        for f_idx, faq in enumerate(faqs_list):
            q = faq.get('q', '')
            a = faq.get('a', '')
            is_open = ' open' if f_idx == 0 else ''
            faq_items_html += f"""
            <details class="bg-white rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition"{is_open}>
                <summary class="p-5 font-bold text-gray-900 flex justify-between items-center gap-3 text-sm sm:text-base rounded-2xl">
                    <span>{q}</span>
                    <svg class="chev w-5 h-5 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                </summary>
                <p class="px-5 pb-5 text-sm text-gray-600 leading-relaxed">{a}</p>
            </details>"""
            schema_faq_entities.append({
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": a
                }
            })

        matching_note_file = get_matching_notes_file(code, slug)
        online_notes_btn_html = ""
        if matching_note_file:
            online_notes_btn_html = f"""
            <a href="/notes/{matching_note_file}" class="inline-flex items-center gap-1.5 bg-white border border-gray-300 hover:border-blue-500 hover:text-blue-600 text-gray-700 font-semibold text-xs sm:text-sm px-3.5 py-2.5 rounded-xl shadow-sm transition whitespace-nowrap">
                Read Online Notes &rarr;
            </a>"""

        whatsapp_cta_html = f"""
        <div class="mt-6 p-5 sm:p-6 bg-gradient-to-r from-emerald-50 to-green-50 border border-green-200 rounded-2xl shadow-sm">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div class="space-y-1">
                    <div class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-bold bg-green-100 text-green-800">
                        <svg class="w-3.5 h-3.5 text-green-600" fill="currentColor" viewBox="0 0 448 512"><path d="M380.9 97.1C339 55.1 283.2 32 223.9 32c-122.4 0-222 99.6-222 222 0 39.1 10.2 77.3 29.6 111L0 480l117.7-30.9c32.4 17.7 68.9 27 106.1 27h.1c122.3 0 224.1-99.6 224.1-222 0-59.3-25.2-115-67.1-157zm-157 341.6c-33.2 0-65.7-8.9-94-25.7l-6.7-4-69.8 18.3L72 359.2l-4.4-7c-18.5-29.4-28.2-63.3-28.2-98.2 0-101.7 82.8-184.5 184.6-184.5 49.3 0 95.6 19.2 130.4 54.1 34.8 34.9 56.2 81.2 56.1 130.5 0 101.8-84.9 184.6-186.6 184.6zm101.2-138.2c-5.5-2.8-32.8-16.2-37.9-18-5.1-1.9-8.8-2.8-12.5 2.8-3.7 5.6-14.3 18-17.6 21.8-3.2 3.7-6.5 4.2-12 1.4-32.6-16.3-54-29.1-75.5-66-5.7-9.8 5.7-9.1 16.3-30.3 1.8-3.7 .9-6.9-.5-9.7-1.4-2.8-12.5-30.1-17.1-41.2-4.5-10.8-9.1-9.3-12.5-9.5-3.2-.2-6.9-.2-10.6-.2-3.7 0-9.7 1.4-14.8 6.9-5.1 5.6-19.4 19-19.4 46.3 0 27.3 19.9 53.7 22.6 57.4 2.8 3.7 39.1 59.7 94.8 83.8 35.2 15.2 49 16.5 66.6 13.9 10.7-1.6 32.8-13.4 37.4-26.4 4.6-13 4.6-24.1 3.2-26.4-1.3-2.5-5-3.9-10.5-6.6z"/></svg>
                        Direct WhatsApp Delivery
                    </div>
                    <h3 class="font-bold text-gray-900 text-base sm:text-lg">Need {name} ({code}) Important Question Bank &amp; Notes?</h3>
                    <p class="text-xs sm:text-sm text-gray-600">Get chapter-wise repeated exam questions, model answers, and formula cheat sheets directly on WhatsApp.</p>
                </div>
                <div class="flex flex-wrap sm:flex-nowrap items-center gap-2.5 flex-shrink-0">
                    <a href="{WHATSAPP_IMP_URL}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-2 bg-green-600 hover:bg-green-700 text-white font-bold text-xs sm:text-sm px-4 py-2.5 rounded-xl shadow transition whitespace-nowrap">
                        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 448 512"><path d="M380.9 97.1C339 55.1 283.2 32 223.9 32c-122.4 0-222 99.6-222 222 0 39.1 10.2 77.3 29.6 111L0 480l117.7-30.9c32.4 17.7 68.9 27 106.1 27h.1c122.3 0 224.1-99.6 224.1-222 0-59.3-25.2-115-67.1-157zm-157 341.6c-33.2 0-65.7-8.9-94-25.7l-6.7-4-69.8 18.3L72 359.2l-4.4-7c-18.5-29.4-28.2-63.3-28.2-98.2 0-101.7 82.8-184.5 184.6-184.5 49.3 0 95.6 19.2 130.4 54.1 34.8 34.9 56.2 81.2 56.1 130.5 0 101.8-84.9 184.6-186.6 184.6zm101.2-138.2c-5.5-2.8-32.8-16.2-37.9-18-5.1-1.9-8.8-2.8-12.5 2.8-3.7 5.6-14.3 18-17.6 21.8-3.2 3.7-6.5 4.2-12 1.4-32.6-16.3-54-29.1-75.5-66-5.7-9.8 5.7-9.1 16.3-30.3 1.8-3.7 .9-6.9-.5-9.7-1.4-2.8-12.5-30.1-17.1-41.2-4.5-10.8-9.1-9.3-12.5-9.5-3.2-.2-6.9-.2-10.6-.2-3.7 0-9.7 1.4-14.8 6.9-5.1 5.6-19.4 19-19.4 46.3 0 27.3 19.9 53.7 22.6 57.4 2.8 3.7 39.1 59.7 94.8 83.8 35.2 15.2 49 16.5 66.6 13.9 10.7-1.6 32.8-13.4 37.4-26.4 4.6-13 4.6-24.1 3.2-26.4-1.3-2.5-5-3.9-10.5-6.6z"/></svg>
                        Get Question Bank ↗
                    </a>
                    {online_notes_btn_html}
                </div>
            </div>
        </div>"""

        # Bespoke SEO Title & Descriptions
        page_title = f"MSBTE {code} {name} ({abbr}) Question Paper PDF Download | K-Scheme PYQ"
        meta_desc = f"Download official MSBTE K-Scheme {name} ({code} - {abbr}) Summer 2026 & Winter 2025 previous year question papers. Free PDF direct download for {sem_name} {branches_short_str}."
        meta_keywords = ", ".join(keywords_list) if keywords_list else f"MSBTE {code} question paper, {code} pyq, {name} question paper summer 2026, {name} winter 2025 question paper, {code} msbte previous year papers, msbte k scheme pyq, {name} model answer paper, {sids_str}, msbte diploma exam papers"
        canonical_url = f"https://msbtenotes-info.netlify.app/pyq/{slug}.html"
        image_url = f"https://msbtenotes-info.netlify.app{thumb_url}"

        # JSON-LD Schemas
        schema_breadcrumb = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Home",
                    "item": "https://msbtenotes-info.netlify.app/"
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "Question Papers (PYQ)",
                    "item": "https://msbtenotes-info.netlify.app/pyq/"
                },
                {
                    "@type": "ListItem",
                    "position": 3,
                    "name": f"{code} - {name}"
                }
            ]
        }

        schema_course = {
            "@context": "https://schema.org",
            "@type": "Course",
            "name": f"{name} ({abbr} - {code})",
            "description": meta_desc,
            "courseCode": code,
            "provider": {
                "@type": "Organization",
                "name": "MSBTE Notes & Info",
                "sameAs": "https://msbtenotes-info.netlify.app"
            },
            "educationalCredentialAwarded": "MSBTE Diploma Engineering",
            "hasCourseInstance": {
                "@type": "CourseInstance",
                "courseMode": "Full-Time",
                "instructor": {
                    "@type": "Organization",
                    "name": "Maharashtra State Board of Technical Education (MSBTE)"
                }
            }
        }

        schema_faq = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": schema_faq_entities if schema_faq_entities else [
                {
                    "@type": "Question",
                    "name": f"How can I download MSBTE {code} {name} question papers?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": f"You can download free official MSBTE K-Scheme question papers for {name} ({code}) directly in PDF format from this page via 1-click Google Drive direct download links."
                    }
                },
                {
                    "@type": "Question",
                    "name": f"What is the passing criteria for {name} ({code})?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": f"Under the MSBTE K-Scheme, students must score at least 28 marks out of 70 (40%) in the End Semester Examination (ESE) theory paper to pass {name} ({code})."
                    }
                }
            ]
        }

        html_content = SUBJECT_PAGE_TEMPLATE.replace('__PAGE_TITLE__', page_title) \
                                            .replace('__META_DESC__', meta_desc) \
                                            .replace('__META_KEYWORDS__', meta_keywords) \
                                            .replace('__CANONICAL_URL__', canonical_url) \
                                            .replace('__IMAGE_URL__', image_url) \
                                            .replace('__SCHEMA_BREADCRUMB__', json.dumps(schema_breadcrumb, indent=2)) \
                                            .replace('__SCHEMA_COURSE__', json.dumps(schema_course, indent=2)) \
                                            .replace('__SCHEMA_FAQ__', json.dumps(schema_faq, indent=2)) \
                                            .replace('__NAV_HTML__', NAV_HTML) \
                                            .replace('__CODE__', code) \
                                            .replace('__NAME__', name) \
                                            .replace('__ABBR__', abbr) \
                                            .replace('__SEM_NAME__', sem_name) \
                                            .replace('__ACAD_YEAR__', acad_year) \
                                            .replace('__SUBJECT_TYPE_BADGE__', subject_type_badge) \
                                            .replace('__SUBJECT_TYPE__', subject_type) \
                                            .replace('__BRANCH_PILLS_HTML__', branch_pills_html) \
                                            .replace('__THUMB_URL__', thumb_url) \
                                            .replace('__WHATSAPP_CTA_HTML__', whatsapp_cta_html) \
                                            .replace('__DOWNLOAD_CARDS_HTML__', download_cards_html) \
                                            .replace('__PRIMARY_ID__', primary_id) \
                                            .replace('__SIZES_SUMMARY__', sizes_summary) \
                                            .replace('__BRANCHES_STR__', branches_str) \
                                            .replace('__SIDS_STR__', sids_str) \
                                            .replace('__SUBJECT_GUIDE_HTML__', subject_guide_html) \
                                            .replace('__SYLLABUS_CARDS_HTML__', syllabus_cards_html) \
                                            .replace('__REPEATED_QUESTIONS_HTML__', repeated_questions_html) \
                                            .replace('__FAQ_ITEMS_HTML__', faq_items_html) \
                                            .replace('__NAV_JS__', NAV_JS)

        # Write primary file: pyq/{slug}.html
        output_path = os.path.join(PYQ_DIR, f"{slug}.html")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        # Also create directory folder: pyq/{slug}/index.html so local servers never 404 on clean URLs
        clean_dir = os.path.join(PYQ_DIR, slug)
        os.makedirs(clean_dir, exist_ok=True)
        with open(os.path.join(clean_dir, "index.html"), 'w', encoding='utf-8') as f:
            f.write(html_content)

        # Build catalog entry with authentic PNG thumbnail and direct .html URL
        catalog_entries.append({
            'code': code,
            'title': f"{name} ({code}) Question Papers",
            'subject_name': name,
            'abbreviation': abbr,
            'semester': sem,
            'academic_year': acad_year,
            'subject_type': subject_type,
            'branches': branch_codes_sorted,
            'branches_str': branches_str,
            'slug': slug,
            'url': f"/pyq/{slug}.html",
            'image': thumb_url,
            'papers': papers
        })

    print(f"Generated {len(by_code)} subject pages and clean directory folders in {PYQ_DIR}")

    # Generate master hub portal
    generate_hub_page(by_code)

    # Save all 734 Drive files into pyq/all_drive_papers.json
    save_all_drive_papers()

    # Update catalogs
    update_resources_json(catalog_entries)

    # Update sitemap.xml
    update_sitemap(by_code)

    # Update _redirects
    update_redirects(sid_redirects)

    print("Generation complete! All assets and pages are fully synchronized.")


def generate_hub_page(by_code):
    """Generates the master portal pyq/index.html with authentic thumbnails & client search/filter."""
    cards_html = ""
    for code, data in sorted(by_code.items(), key=lambda x: (x[1]['sem'], x[1]['name'])):
        slug = data['slug']
        name = data['name']
        sem = data['sem']
        subj_type = data.get('subject_type', 'Core')
        branch_codes = sorted(list(data['branches']))
        branch_shorts = [BRANCH_INFO.get(b, {}).get('short', b) for b in branch_codes]
        branches_str = " ".join([b.lower() for b in branch_codes] + [s.lower() for s in branch_shorts])

        thumb_url = get_subject_thumbnail(code, name, slug, data['subject_ids'])

        paper_badges = []
        papers = data['papers']
        if 'Summer 2026' in papers:
            paper_badges.append('<span class="text-xs px-2 py-0.5 rounded bg-blue-50 text-blue-700 font-semibold border border-blue-200">☀️ Summer 2026</span>')
        if 'Winter 2025' in papers:
            paper_badges.append('<span class="text-xs px-2 py-0.5 rounded bg-indigo-50 text-indigo-700 font-semibold border border-indigo-200">❄️ Winter 2025</span>')
        elif sem == 6:
            paper_badges.append('<span class="text-xs px-2 py-0.5 rounded bg-gray-100 text-gray-600">Even Sem (Summer Only)</span>')

        branch_badges = "".join([
            f'<span class="text-xs px-2 py-0.5 rounded {BRANCH_INFO.get(b, {}).get("badge_bg", "bg-gray-100")} {BRANCH_INFO.get(b, {}).get("badge_text", "text-gray-700")} font-medium">{BRANCH_INFO.get(b, {}).get("short", b)}</span>'
            for b in branch_codes
        ])

        type_badge = f'<span class="px-2 py-0.5 rounded text-xs font-semibold {"bg-purple-100 text-purple-800" if subj_type == "Elective" else "bg-blue-100 text-blue-800"}">{"Elective" if subj_type == "Elective" else "Core"}</span>'

        # Note: All card links explicitly point to /pyq/{slug}.html to guarantee resolution on local dev servers & Netlify
        cards_html += f"""
        <article class="pyq-hub-card p-0 overflow-hidden"
                 data-code="{code}" data-name="{name.lower()}" data-sem="{sem}" data-branches="{branches_str}" data-type="{subj_type.lower()}">
            <div>
                <a href="/pyq/{slug}.html" class="block overflow-hidden bg-gray-100 aspect-video">
                    <img src="{thumb_url}" alt="{name} {code} PYQ" class="w-full h-full object-cover transform hover:scale-105 transition duration-300" loading="lazy" width="320" height="180">
                </a>
                <div class="p-5">
                    <div class="flex items-start justify-between gap-2 mb-2">
                        <span class="px-2.5 py-1 rounded-lg text-xs font-mono font-bold bg-blue-600 text-white">
                            {code}
                        </span>
                        <div class="flex items-center gap-1">
                            <span class="px-2 py-0.5 rounded text-xs font-semibold bg-gray-100 text-gray-700">
                                Sem {sem}
                            </span>
                            {type_badge}
                        </div>
                    </div>
                    <h3 class="text-base sm:text-lg font-bold text-gray-900 font-display mb-2 leading-snug line-clamp-2">
                        <a href="/pyq/{slug}.html" class="hover:text-blue-600 transition">{name}</a>
                    </h3>
                    <div class="flex flex-wrap gap-1 mb-3">
                        {branch_badges}
                    </div>
                </div>
            </div>
            <div class="p-5 pt-0">
                <div class="pt-3 border-t border-gray-100">
                    <div class="flex flex-wrap gap-1.5 mb-3">
                        {"".join(paper_badges)}
                    </div>
                    <a href="/pyq/{slug}.html" class="w-full bg-gray-50 hover:bg-blue-600 hover:text-white text-blue-600 text-xs font-bold py-2.5 px-3 rounded-xl transition text-center block border border-gray-200 hover:border-blue-600">
                        View Paper &amp; Solutions &rarr;
                    </a>
                </div>
            </div>
        </article>"""

    hub_html = HUB_PAGE_TEMPLATE.replace('__NAV_HTML__', NAV_HTML) \
                                .replace('__NAV_JS__', NAV_JS) \
                                .replace('__CARDS_COUNT__', str(len(by_code))) \
                                .replace('__CARDS_HTML__', cards_html)

    hub_output_path = os.path.join(PYQ_DIR, 'index.html')
    with open(hub_output_path, 'w', encoding='utf-8') as f:
        f.write(hub_html)

    print(f"Generated Master Hub at {hub_output_path}")


def save_all_drive_papers():
    """Reads the raw drive files and writes all_drive_papers.json into pyq/."""
    if os.path.exists(DRIVE_CSV_PATH):
        with open(DRIVE_CSV_PATH, 'r', encoding='utf-8', errors='ignore') as f:
            drive_rows = list(csv.DictReader(f))
        with open(ALL_DRIVE_PAPERS_PATH, 'w', encoding='utf-8') as f:
            json.dump(drive_rows, f, indent=2)
        print(f"Saved {len(drive_rows)} files into {ALL_DRIVE_PAPERS_PATH}")


def update_resources_json(catalog_entries):
    """Saves /pyq/resources.json and merges into /Notes/resources.json with direct .html URLs."""
    with open(PYQ_RESOURCES_PATH, 'w', encoding='utf-8') as f:
        json.dump(catalog_entries, f, indent=2)
    print(f"Updated {PYQ_RESOURCES_PATH} ({len(catalog_entries)} entries)")

    # Update Notes/resources.json
    existing_notes_entries = []
    if os.path.exists(NOTES_RESOURCES_PATH):
        try:
            with open(NOTES_RESOURCES_PATH, 'r', encoding='utf-8') as f:
                existing_notes_entries = json.load(f)
        except Exception:
            existing_notes_entries = []

    # Filter out previous pyq entries and merge new ones
    non_pyq_entries = [e for e in existing_notes_entries if not e.get('url', '').startswith('/pyq/')]
    merged = non_pyq_entries + catalog_entries

    with open(NOTES_RESOURCES_PATH, 'w', encoding='utf-8') as f:
        json.dump(merged, f, indent=2)
    print(f"Updated {NOTES_RESOURCES_PATH} (total entries: {len(merged)})")


def update_sitemap(by_code):
    """Updates sitemap.xml with all 116 subject URLs and /pyq/ hub with .html format."""
    if not os.path.exists(SITEMAP_PATH):
        print("Sitemap not found, skipping sitemap update.")
        return

    tree = ET.parse(SITEMAP_PATH)
    root = tree.getroot()

    # XML namespace
    ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')

    existing_locs = set()
    for url_tag in root.findall('ns:url', ns):
        loc = url_tag.find('ns:loc', ns)
        if loc is not None and loc.text:
            existing_locs.add(loc.text.strip())

    hub_url = "https://msbtenotes-info.netlify.app/pyq/"
    if hub_url not in existing_locs:
        url_elem = ET.SubElement(root, 'url')
        loc_elem = ET.SubElement(url_elem, 'loc')
        loc_elem.text = hub_url
        lastmod_elem = ET.SubElement(url_elem, 'lastmod')
        lastmod_elem.text = "2026-11-08"
        cf_elem = ET.SubElement(url_elem, 'changefreq')
        cf_elem.text = "weekly"
        prio_elem = ET.SubElement(url_elem, 'priority')
        prio_elem.text = "0.9"

    for code, data in by_code.items():
        sub_url = f"https://msbtenotes-info.netlify.app/pyq/{data['slug']}.html"
        if sub_url not in existing_locs:
            url_elem = ET.SubElement(root, 'url')
            loc_elem = ET.SubElement(url_elem, 'loc')
            loc_elem.text = sub_url
            lastmod_elem = ET.SubElement(url_elem, 'lastmod')
            lastmod_elem.text = "2026-11-08"
            cf_elem = ET.SubElement(url_elem, 'changefreq')
            cf_elem.text = "weekly"
            prio_elem = ET.SubElement(url_elem, 'priority')
            prio_elem.text = "0.8"

    tree.write(SITEMAP_PATH, encoding='utf-8', xml_declaration=True)
    print(f"Updated {SITEMAP_PATH}")


def update_redirects(sid_redirects):
    """Ensures clean URL rewrite /pyq/:slug -> /pyq/:slug.html and uppercase /PYQ/* exist in _redirects."""
    existing_content = ""
    if os.path.exists(REDIRECTS_PATH):
        with open(REDIRECTS_PATH, 'r', encoding='utf-8') as f:
            existing_content = f.read()

    new_rules = []
    if "/PYQ/*" not in existing_content:
        new_rules.append("/PYQ/*     /pyq/:splat     301!")
    if "/pyq " not in existing_content and "/pyq\t" not in existing_content:
        new_rules.append("/pyq       /pyq/           301!")

    clean_rewrite = "/pyq/:slug    /pyq/:slug.html    200"
    if "/pyq/:slug" not in existing_content:
        new_rules.append(clean_rewrite)

    alias_rules = []
    for sid_low, target_slug in sorted(sid_redirects.items()):
        rule_clean = f"/pyq/{sid_low}    /pyq/{target_slug}.html    301!"
        rule_html = f"/pyq/{sid_low}.html    /pyq/{target_slug}.html    301!"
        if f"/pyq/{sid_low} " not in existing_content and f"/pyq/{sid_low}\t" not in existing_content:
            alias_rules.append(rule_clean)
        if f"/pyq/{sid_low}.html" not in existing_content:
            alias_rules.append(rule_html)

    if new_rules or alias_rules:
        with open(REDIRECTS_PATH, 'a', encoding='utf-8') as f:
            if new_rules:
                f.write("\n# PYQ Uppercase and Rewrite Rules\n")
                f.write("\n".join(new_rules) + "\n")
            if alias_rules:
                f.write("\n# PYQ Subject ID Aliases to .html\n")
                f.write("\n".join(alias_rules) + "\n")
        print(f"Appended {len(new_rules) + len(alias_rules)} rules to {REDIRECTS_PATH}")
    else:
        print("Redirect rules already up to date.")


if __name__ == '__main__':
    main()
