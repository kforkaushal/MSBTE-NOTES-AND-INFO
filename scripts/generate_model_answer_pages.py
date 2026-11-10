#!/usr/bin/env python3
"""
scripts/generate_model_answer_pages.py
Professional generator for 14 MSBTE K-Scheme Model Answer pages with:
- Authentic PNG thumbnails from resourse/msbte_subject_thumbnails
- Hallmark trust seals and official MSBTE evaluation marking schemes
- Quick Jump navigation, responsive .res-card downloads grid, and live Google Drive PDF viewer
- In-article and responsive Google AdSense placements
- Pro-Max SEO: TechArticle, Course, BreadcrumbList, and FAQPage JSON-LD schemas
- Master portal model-answer/index.html with branch & semester filter pills and real-time search
- Synchronization with Notes/resources.json, sitemap.xml, _redirects, and global navigation menus
"""

import os
import sys
import json
import re
import xml.etree.ElementTree as ET
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)
from scripts.subject_seo_data import SUBJECT_SEO

MODEL_DATA_PATH = os.path.join(BASE_DIR, 'data', 'model_answer_data.json')
OUTPUT_DIR = os.path.join(BASE_DIR, 'model-answer')
THUMBS_DIR = os.path.join(BASE_DIR, 'resourse', 'msbte_subject_thumbnails')
SITEMAP_PATH = os.path.join(BASE_DIR, 'sitemap.xml')
REDIRECTS_PATH = os.path.join(BASE_DIR, '_redirects')
NOTES_RES_PATH = os.path.join(BASE_DIR, 'Notes', 'resources.json')
INDEX_PATH = os.path.join(BASE_DIR, 'index.html')
PYQ_INDEX_PATH = os.path.join(BASE_DIR, 'pyq', 'index.html')

os.makedirs(OUTPUT_DIR, exist_ok=True)

PNG_THUMB_MAP = {
    "Data Structures Using C": "/resourse/msbte_subject_thumbnails/01_Data_Structures_Using_C.png",
    "Database Management System": "/resourse/msbte_subject_thumbnails/02_Database_Management_System.png",
    "Digital Techniques": "/resourse/msbte_subject_thumbnails/03_Digital_Techniques.png",
    "Object Oriented Programming": "/resourse/msbte_subject_thumbnails/04_Object_Oriented_Programming.png",
    "Operating System": "/resourse/msbte_subject_thumbnails/05_Operating_System.png",
    "Advanced Computer Network": "/resourse/msbte_subject_thumbnails/06_Advanced_Computer_Network.png",
    "Data Analytics": "/resourse/msbte_subject_thumbnails/07_Data_Analytics.png",
    "Advanced Database Management": "/resourse/msbte_subject_thumbnails/08_Advanced_Database_Management.png",
    "Software Engineering": "/resourse/msbte_subject_thumbnails/09_Software_Engineering.png",
    "Software Engineering and Testing": "/resourse/msbte_subject_thumbnails/10_Software_Engineering_and_Testing.png",
    "Cloud Computing": "/resourse/msbte_subject_thumbnails/11_Cloud_Computing.png",
    "Cloud Computing for Data Science": "/resourse/msbte_subject_thumbnails/12_Cloud_Computing_for_Data_Science.png",
    "AI & ML Algorithm": "/resourse/msbte_subject_thumbnails/13_AI_and_ML_Algorithm.png",
    "Natural Language Processing": "/resourse/msbte_subject_thumbnails/14_Natural_Language_Processing.png"
}

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
                        <div class="dropdown-menu absolute left-0 top-full -mt-1 w-60 bg-white rounded-xl shadow-xl border border-gray-100 py-2 hidden group-hover:block transition-all z-50">
                            <a href="/#notes" class="flex items-center gap-2.5 px-4 py-2.5 text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-600 font-medium transition">
                                <span class="text-base">📝</span>
                                <span>Subject Notes</span>
                            </a>
                            <a href="/pyq/" class="flex items-center gap-2.5 px-4 py-2.5 text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-600 font-medium transition">
                                <span class="text-base">📚</span>
                                <span>Question Papers (PYQ)</span>
                            </a>
                            <a href="/model-answer/" class="flex items-center gap-2.5 px-4 py-2.5 text-sm text-blue-600 font-bold hover:bg-blue-50 transition border-l-2 border-blue-600 bg-blue-50/40">
                                <span class="text-base">📑</span>
                                <span>Model Answer Papers</span>
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
                            <span class="text-xs font-sans font-semibold px-2 py-0.5 rounded-full bg-blue-100 text-blue-700">4 Links</span>
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
                        <a href="/pyq/" onclick="toggleMobileMenu()" class="flex items-center gap-2.5 py-2 px-3 rounded-lg text-base font-medium text-gray-700 hover:bg-blue-50 transition">
                            <span class="text-lg">📚</span>
                            <div>
                                <div class="font-semibold text-gray-900">Question Papers (PYQ)</div>
                                <div class="text-xs text-gray-500">Board question papers archive</div>
                            </div>
                        </a>
                        <a href="/model-answer/" onclick="toggleMobileMenu()" class="flex items-center gap-2.5 py-2 px-3 rounded-lg text-base font-bold text-blue-600 bg-blue-50 transition border border-blue-100">
                            <span class="text-lg">📑</span>
                            <div>
                                <div class="font-bold text-blue-700">Model Answer Papers</div>
                                <div class="text-xs text-blue-600">Official solved papers &amp; marking schemes</div>
                            </div>
                        </a>
                        <a href="/video-course/" onclick="toggleMobileMenu()" class="flex items-center gap-2.5 py-2 px-3 rounded-lg text-base font-medium text-gray-700 hover:bg-blue-50 hover:text-blue-600 transition">
                            <span class="text-lg">🎥</span>
                            <div>
                                <div class="font-semibold text-gray-900">Video Courses</div>
                                <div class="text-xs text-gray-500">Engineering tutorials &amp; concept walkthroughs</div>
                            </div>
                        </a>
                    </div>
                </div>

                <a href="/#departments" onclick="toggleMobileMenu()" class="text-xl font-display font-bold text-gray-900 border-b border-gray-100 pb-2">Departments</a>
                <a href="/#blogs" onclick="toggleMobileMenu()" class="text-xl font-display font-bold text-gray-900 border-b border-gray-100 pb-2">Blog</a>
                <a href="/news/" onclick="toggleMobileMenu()" class="text-xl font-display font-bold text-red-600 border-b border-gray-100 pb-2 flex items-center justify-between">
                    <span>🔴 Breaking News</span>
                    <span class="text-xs bg-red-100 text-red-600 font-semibold px-2 py-0.5 rounded-full uppercase tracking-wider">Live</span>
                </a>
                <a href="/collegeinfo/" onclick="toggleMobileMenu()" class="text-xl font-display font-bold text-gray-900 border-b border-gray-100 pb-2">Colleges</a>

                <!-- Jobs & Career Mobile Submenu (Accordion) -->
                <div class="border-b border-gray-100 pb-2">
                    <button type="button" onclick="toggleMobileSubmenu('mobileJobsSubmenu', 'mobileJobsArrow')" class="w-full flex items-center justify-between text-xl font-display font-bold text-gray-900 py-1.5 focus:outline-none">
                        <span class="flex items-center gap-2">
                            <span>Jobs &amp; Career</span>
                            <span class="text-xs font-sans font-semibold px-2 py-0.5 rounded-full bg-blue-100 text-blue-700">2 Links</span>
                        </span>
                        <svg id="mobileJobsArrow" class="w-5 h-5 text-gray-500 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                        </svg>
                    </button>
                    <div id="mobileJobsSubmenu" class="hidden space-y-1 pl-2 pt-1 pb-1 transition-all">
                        <a href="/jobs/index.html" onclick="toggleMobileMenu()" class="flex items-center gap-2.5 py-2 px-3 rounded-lg text-base font-medium text-gray-700 hover:bg-blue-50 hover:text-blue-600 transition">
                            <span class="text-lg">💼</span>
                            <div>
                                <div class="font-semibold text-gray-900">Jobs Portal</div>
                                <div class="text-xs text-gray-500">MSBTE diploma jobs &amp; freshers hiring</div>
                            </div>
                        </a>
                        <a href="/internships.html" onclick="toggleMobileMenu()" class="flex items-center gap-2.5 py-2 px-3 rounded-lg text-base font-medium text-gray-700 hover:bg-blue-50 hover:text-blue-600 transition">
                            <span class="text-lg">🎓</span>
                            <div>
                                <div class="font-semibold text-gray-900">Internships</div>
                                <div class="text-xs text-gray-500">Paid &amp; verified summer engineering internships</div>
                            </div>
                        </a>
                    </div>
                </div>

                <a href="/about.html" onclick="toggleMobileMenu()" class="text-xl font-display font-bold text-gray-900 border-b border-gray-100 pb-2">About</a>
                <a href="/contact.html" onclick="toggleMobileMenu()" class="text-xl font-display font-bold text-gray-900 border-b border-gray-100 pb-2">Contact</a>
            </div>
        </div>
    </nav>"""

FOOTER_HTML = """    <!-- Site Footer -->
    <footer class="bg-blue-600 text-white mt-16">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
                <div>
                    <h3 class="text-lg font-bold font-display mb-3">MSBTE Notes &amp; Info</h3>
                    <p class="text-blue-100 text-sm mb-4">Empowering Maharashtra polytechnic diploma students with verified K-Scheme model answers, previous year papers, and academic resources.</p>
                    <a href="https://www.producthunt.com/products/msbte-notes-info?utm_source=badge-follow&utm_medium=badge&utm_souce=badge-msbte&#0045;notes&#0045;info" target="_blank" rel="noopener noreferrer">
                        <img src="https://api.producthunt.com/widgets/embed-image/v1/follow.svg?product_identifier=msbte-notes-info&theme=light" alt="MSBTE Notes &amp; Info on Product Hunt" width="160" height="36" />
                    </a>
                </div>
                <div>
                    <h4 class="text-sm font-semibold uppercase tracking-wider text-blue-200 mb-3">Study Resources</h4>
                    <ul class="space-y-2 text-sm text-blue-100">
                        <li><a href="/#notes" class="hover:underline">Subject Notes</a></li>
                        <li><a href="/pyq/" class="hover:underline">Question Papers (PYQ)</a></li>
                        <li><a href="/model-answer/" class="hover:underline font-bold text-white">Model Answer Papers</a></li>
                        <li><a href="/video-course/" class="hover:underline">Video Courses</a></li>
                    </ul>
                </div>
                <div>
                    <h4 class="text-sm font-semibold uppercase tracking-wider text-blue-200 mb-3">Departments</h4>
                    <ul class="space-y-2 text-sm text-blue-100">
                        <li><a href="/#departments" class="hover:underline">Computer Engineering</a></li>
                        <li><a href="/#departments" class="hover:underline">Information Technology</a></li>
                        <li><a href="/#departments" class="hover:underline">AI &amp; Machine Learning</a></li>
                        <li><a href="/#departments" class="hover:underline">Mechanical &amp; Civil</a></li>
                    </ul>
                </div>
                <div>
                    <h4 class="text-sm font-semibold uppercase tracking-wider text-blue-200 mb-3">Community &amp; Help</h4>
                    <ul class="space-y-2 text-sm text-blue-100">
                        <li><a href="https://wa.me/917083236221" target="_blank" rel="noopener noreferrer" class="hover:underline">WhatsApp Support</a></li>
                        <li><a href="https://www.youtube.com/@msbte-notes-and-info" target="_blank" rel="noopener noreferrer" class="hover:underline">YouTube Channel</a></li>
                        <li><a href="/about.html" class="hover:underline">About Us</a></li>
                        <li><a href="/contact.html" class="hover:underline">Contact</a></li>
                    </ul>
                </div>
            </div>
            <div class="border-t border-blue-500 pt-6 text-center text-sm text-blue-200">
                <p>&copy; 2026 MSBTE Notes &amp; Info. Non-official independent student learning initiative.</p>
            </div>
        </div>
    </footer>

    <!-- Interactive Dropdown & Mobile Drawer Logic -->
    <script>
        function toggleMobileMenu() {
            const menu = document.getElementById('mobileNav');
            const menuIcon = document.getElementById('menuIcon');
            const closeIcon = document.getElementById('closeIcon');
            if (!menu) return;
            const isClosed = menu.classList.contains('translate-x-full');
            if (isClosed) {
                menu.classList.remove('translate-x-full');
                if (menuIcon) menuIcon.classList.add('hidden');
                if (closeIcon) closeIcon.classList.remove('hidden');
                document.body.style.overflow = 'hidden';
            } else {
                menu.classList.add('translate-x-full');
                if (menuIcon) menuIcon.classList.remove('hidden');
                if (closeIcon) closeIcon.classList.add('hidden');
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

        document.addEventListener('click', function(e) {
            if (!e.target.closest('.nav-dropdown')) {
                document.querySelectorAll('.nav-dropdown').forEach(d => {
                    d.classList.remove('is-open');
                    const b = d.querySelector('button[aria-expanded]');
                    if (b) b.setAttribute('aria-expanded', 'false');
                });
            }
        });

        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                document.querySelectorAll('.nav-dropdown').forEach(d => {
                    d.classList.remove('is-open');
                    const b = d.querySelector('button[aria-expanded]');
                    if (b) b.setAttribute('aria-expanded', 'false');
                });
            }
        });

        function toggleFaq(el) {
            const answer = el.nextElementSibling;
            const chev = el.querySelector('.chev');
            if (!answer) return;
            answer.classList.toggle('hidden');
            if (chev) {
                chev.classList.toggle('rotate-180');
            }
        }
    </script>"""

def generate_subject_page(name, info, idx):
    code = info['code']
    slug = info['slug']
    abbr = info['abbr']
    sem = info['sem']
    year = info['year']
    branches_list = info['branches']
    branch_names = info['branch_names']
    branches_str = ", ".join(branches_list)
    papers = info.get('papers', {})
    
    # Authentic PNG Thumbnail
    thumb_url = PNG_THUMB_MAP.get(name, f"/resourse/msbte_subject_thumbnails/{idx+1:02d}_{name.replace(' ', '_').replace('&', 'and')}.png")
    
    # Get SEO units, questions, FAQs
    seo = SUBJECT_SEO.get(code, {})
    units = seo.get('units', [
        ["Unit 1: Fundamentals & System Overview", "Theoretical foundation, essential concepts, and industrial practices.", "12 Marks"],
        ["Unit 2: Core Principles & Operations", "Fundamental structures, processing mechanisms, and standards.", "14 Marks"],
        ["Unit 3: Applied Methodologies & Design", "Design patterns, algorithmic implementation, and analytical methods.", "14 Marks"],
        ["Unit 4: Advanced Architectures & Protocols", "Integration, protocol hierarchies, and system coordination.", "14 Marks"],
        ["Unit 5: Emerging Industrial Trends & Applications", "Real-world case studies, future developments, and deployment scenarios.", "16 Marks"]
    ])
    repeated_questions = seo.get('repeated_questions', [
        {"q": f"Explain the fundamental architecture and working principles of {name} ({code}) with a neat schematic diagram.", "marks": "6 Marks"},
        {"q": f"Differentiate between key operations and design methods in {abbr} with standard comparison parameters.", "marks": "4 Marks"},
        {"q": f"State the core advantages, design constraints, and industrial applications of {abbr} in modern engineering.", "marks": "4 Marks"},
        {"q": f"Draw a neat labelled block diagram and explain step-by-step execution in {abbr}.", "marks": "6 Marks"},
        {"q": f"Solve typical design and implementation problem for {abbr} using standard MSBTE procedure.", "marks": "6 Marks"}
    ])
    custom_faqs = seo.get('custom_faq', [
        {
            "q": f"How can I score 65+ marks in MSBTE {name} ({code})?",
            "a": f"Review all official model answer papers on this page, practice the 5 high-frequency questions, memorize syllabus formulas, and draw neat pencil diagrams with labels."
        },
        {
            "q": f"Does MSBTE award step marks for partially correct answers in {abbr}?",
            "a": f"Yes! MSBTE examiners use official model answer marking keys. You receive points for correct formulas, diagrams, intermediate derivations, and proper units."
        }
    ])
    
    # Find latest paper for live preview
    latest_exam = list(papers.keys())[0] if papers else None
    latest_paper = papers[latest_exam] if latest_exam else None
    latest_drive_id = latest_paper['drive_id'] if latest_paper else ""
    
    # Download cards HTML
    cards_html = []
    for exam_name, p in papers.items():
        cards_html.append(f"""                <div class="res-card bg-white p-6 rounded-3xl border border-gray-200/90 shadow-sm flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between gap-2 mb-3">
                            <span class="px-3.5 py-1 rounded-full text-xs font-bold bg-blue-100 text-blue-800 tracking-wide">{exam_name}</span>
                            <span class="inline-flex items-center gap-1.5 text-xs font-semibold text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-full border border-emerald-200">
                                <svg class="w-3.5 h-3.5 text-emerald-600" fill="currentColor" viewBox="0 0 448 512"><path d="M438.6 105.4c12.5 12.5 12.5 32.8 0 45.3l-256 256c-12.5 12.5-32.8 12.5-45.3 0l-128-128c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0L160 338.7 393.4 105.4c12.5-12.5 32.8-12.5 45.3 0z"/></svg>
                                Verified Solution
                            </span>
                        </div>
                        <h3 class="text-lg font-bold text-gray-900 mb-1">{p['file_name']}</h3>
                        <p class="text-xs text-gray-500 mb-5">MSBTE Official Board Model Answer Paper &amp; Marking Key</p>
                    </div>
                    <div class="flex flex-col sm:flex-row gap-2.5 pt-3 border-t border-gray-100">
                        <a href="{p['download_link']}" target="_blank" rel="noopener noreferrer" class="flex-1 inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-semibold text-sm shadow-sm transition">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
                            Download PDF
                        </a>
                        <a href="{p['view_link']}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center justify-center gap-1.5 px-4 py-2.5 rounded-xl bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold text-sm transition">
                            <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
                            View
                        </a>
                    </div>
                </div>""")
    download_cards_str = "\n".join(cards_html)
    
    # Units HTML
    units_rows = []
    for u_idx, u in enumerate(units, 1):
        if isinstance(u, (list, tuple)):
            u_title = u[0]
            u_desc = u[1] if len(u) > 1 else ""
            u_marks = u[2] if len(u) > 2 else "14 Marks"
        elif isinstance(u, dict):
            u_title = u.get('title', '')
            u_desc = u.get('desc', '')
            u_marks = u.get('marks', '14 Marks')
        else:
            u_title = str(u)
            u_desc = ""
            u_marks = "14 Marks"
            
        units_rows.append(f"""                        <tr class="hover:bg-blue-50/40 transition">
                            <td class="px-5 py-3.5 font-bold text-gray-900 border-b border-gray-100">Unit {u_idx}</td>
                            <td class="px-5 py-3.5 text-gray-800 border-b border-gray-100">
                                <div class="font-semibold text-gray-900">{u_title}</div>
                                {f'<div class="text-xs text-gray-500 mt-0.5">{u_desc}</div>' if u_desc else ''}
                            </td>
                            <td class="px-5 py-3.5 text-center font-bold text-blue-600 border-b border-gray-100 whitespace-nowrap">{u_marks}</td>
                        </tr>""")
    units_html_str = "\n".join(units_rows)
    
    # Questions HTML
    q_items = []
    for q_idx, q in enumerate(repeated_questions, 1):
        q_text = q.get('q', '') if isinstance(q, dict) else str(q)
        q_marks = q.get('marks', '4 Marks') if isinstance(q, dict) else '4 Marks'
        badge_cls = "bg-purple-100 text-purple-700 border-purple-200" if "6" in str(q_marks) else "bg-blue-100 text-blue-700 border-blue-200"
        q_items.append(f"""                <div class="bg-white p-5 rounded-2xl border border-gray-200 shadow-sm flex items-start justify-between gap-4">
                    <div class="flex items-start gap-3">
                        <span class="w-8 h-8 rounded-xl bg-blue-50 text-blue-600 font-bold text-sm flex items-center justify-center flex-shrink-0 mt-0.5 font-display">{q_idx}</span>
                        <div>
                            <p class="text-gray-900 font-semibold text-base leading-snug">{q_text}</p>
                            <p class="text-xs text-gray-500 mt-1">Frequently asked in MSBTE Summer &amp; Winter Board Exams</p>
                        </div>
                    </div>
                    <span class="px-3 py-1 rounded-full text-xs font-bold border {badge_cls} flex-shrink-0">{q_marks}</span>
                </div>""")
    questions_html_str = "\n".join(q_items)
    
    # FAQ HTML & Schema
    faq_items = [
        {
            "q": f"Where can I download MSBTE K-Scheme model answers for {name} ({code})?",
            "a": f"You can download verified MSBTE model answer papers with official solutions for {name} ({code}) directly on this page for Summer and Winter board examination sessions."
        },
        {
            "q": f"How do MSBTE examiners award marks based on model answer papers?",
            "a": f"MSBTE examiners follow step-wise marking schemes detailed in these official model answer keys. Partial credit is given for correct formulas, circuit diagrams, flowcharts, code syntax, and final calculated answers."
        },
        {
            "q": f"Are these model answers updated for K-Scheme curriculum?",
            "a": f"Yes, all provided papers and model solutions strictly align with the latest MSBTE K-Scheme syllabus patterns and course outcomes for {branch_names} students."
        }
    ] + custom_faqs
    
    faq_html = []
    faq_json_entities = []
    for f in faq_items:
        faq_html.append(f"""                <div class="border border-gray-200 rounded-2xl overflow-hidden bg-white shadow-sm">
                    <button type="button" onclick="toggleFaq(this)" class="w-full text-left px-5 py-4 font-bold text-gray-900 flex justify-between items-center hover:bg-gray-50 focus:outline-none transition">
                        <span>{f['q']}</span>
                        <svg class="chev w-5 h-5 text-gray-400 transition-transform duration-200 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                    </button>
                    <div class="hidden px-5 pb-4 text-sm text-gray-600 border-t border-gray-100 pt-3">
                        <p>{f['a']}</p>
                    </div>
                </div>""")
        faq_json_entities.append({
            "@type": "Question",
            "name": f['q'],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": f['a']
            }
        })
    faq_html_str = "\n".join(faq_html)
    faq_schema_str = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faq_json_entities
    }, indent=2)

    canonical_url = f"https://msbtenotes-info.netlify.app/model-answer/{slug}.html"
    page_title = f"{name} ({code}) Model Answer Papers — MSBTE K-Scheme Solved Papers"
    meta_desc = f"Download authentic MSBTE K-Scheme model answer papers, step-wise solved solutions, and official marking schemes for {name} ({code}) - Semester {sem} ({branches_str})."

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Consent default (deny until user chooses) -->
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('consent', 'default', {{ 'ad_storage': 'denied', 'analytics_storage': 'denied' }});
    </script>
    <!-- Google Tag & Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-H5G5CCD95W"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'G-H5G5CCD95W');
    </script>
    <!-- Google AdSense -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9227354288966999" crossorigin="anonymous"></script>

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    <meta name="description" content="{meta_desc}">
    <meta name="keywords" content="MSBTE {code} model answer, {name} model answer paper, {abbr} solved question paper, MSBTE K-Scheme model answer, MSBTE marking scheme {code}">
    <link rel="canonical" href="{canonical_url}">

    <!-- Open Graph -->
    <meta property="og:title" content="{page_title}">
    <meta property="og:description" content="{meta_desc}">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:image" content="https://msbtenotes-info.netlify.app{thumb_url}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:type" content="article">
    <meta property="og:locale" content="en_IN">
    <meta property="og:site_name" content="MSBTE Notes &amp; Info">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:site" content="@msbtenotes">
    <meta name="twitter:title" content="{page_title}">
    <meta name="twitter:description" content="{meta_desc}">
    <meta name="twitter:image" content="https://msbtenotes-info.netlify.app{thumb_url}">

    <!-- Styles -->
    <link rel="stylesheet" href="/style.css">
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link href="https://api.fontshare.com/v2/css?f[]=clash-display@600,700&display=swap" rel="stylesheet">

    <!-- JSON-LD Structured Data: TechArticle -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": "{page_title}",
        "description": "{meta_desc}",
        "url": "{canonical_url}",
        "image": "https://msbtenotes-info.netlify.app{thumb_url}",
        "author": {{
            "@type": "Organization",
            "name": "MSBTE Notes & Info Team",
            "url": "https://msbtenotes-info.netlify.app/"
        }},
        "publisher": {{
            "@type": "Organization",
            "name": "MSBTE Notes & Info",
            "logo": {{
                "@type": "ImageObject",
                "url": "https://msbtenotes-info.netlify.app/resourse/android-chrome-512x512.png"
            }}
        }},
        "datePublished": "2026-11-10",
        "dateModified": "2026-11-10"
    }}
    </script>

    <!-- JSON-LD Structured Data: Course -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Course",
        "name": "{name}",
        "courseCode": "{code}",
        "description": "{meta_desc}",
        "provider": {{
            "@type": "Organization",
            "name": "MSBTE Notes & Info",
            "sameAs": "https://msbtenotes-info.netlify.app/"
        }},
        "educationalCredentialAwarded": "Maharashtra State Board of Technical Education Diploma",
        "hasCourseInstance": {{
            "@type": "CourseInstance",
            "courseMode": "Full-Time Diploma Engineering",
            "instructor": {{
                "@type": "Organization",
                "name": "MSBTE Board Certified Faculty"
            }}
        }}
    }}
    </script>

    <!-- JSON-LD Structured Data: BreadcrumbList -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
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
                "name": "Model Answer Papers",
                "item": "https://msbtenotes-info.netlify.app/model-answer/"
            }},
            {{
                "@type": "ListItem",
                "position": 3,
                "name": "{name} ({code})",
                "item": "{canonical_url}"
            }}
        ]
    }}
    </script>

    <!-- JSON-LD Structured Data: FAQPage -->
    <script type="application/ld+json">
    {faq_schema_str}
    </script>

    <style>
        .font-display {{ font-family: 'Clash Display', sans-serif; }}
        .res-card {{
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        }}
        .res-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 12px 28px -6px rgba(0, 0, 0, 0.1);
        }}
        .no-scrollbar::-webkit-scrollbar {{ display: none; }}
        .no-scrollbar {{ -ms-overflow-style: none; scrollbar-width: none; }}
    </style>
</head>
<body class="bg-gray-50 text-gray-900 pt-16">

{NAV_HTML}

    <!-- Breadcrumb -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <nav class="flex text-sm text-gray-500 font-medium" aria-label="Breadcrumb">
            <ol class="inline-flex items-center space-x-1 md:space-x-2">
                <li><a href="/" class="hover:text-blue-600 transition flex items-center gap-1">
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z"></path></svg>
                    Home
                </a></li>
                <li class="flex items-center"><span class="mx-2 text-gray-400">/</span><a href="/model-answer/" class="hover:text-blue-600 transition">Model Answers</a></li>
                <li class="flex items-center"><span class="mx-2 text-gray-400">/</span><span class="text-gray-900 font-semibold">{abbr} ({code})</span></li>
            </ol>
        </nav>
    </div>

    <!-- Hero Section -->
    <header class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-2 pb-6">
        <div class="bg-white rounded-3xl p-6 sm:p-10 border border-gray-200/90 shadow-sm relative overflow-hidden">
            <div class="absolute -right-20 -top-20 w-72 h-72 bg-blue-100/60 rounded-full blur-3xl pointer-events-none"></div>

            <div class="flex flex-wrap items-center gap-2 mb-4">
                <span class="px-3.5 py-1 rounded-full text-xs font-bold bg-blue-600 text-white uppercase tracking-wider shadow-sm">K-Scheme</span>
                <span class="px-3.5 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 uppercase tracking-wider border border-emerald-200">Official Solved Papers</span>
                <span class="px-3.5 py-1 rounded-full text-xs font-bold bg-gray-100 text-gray-700">Semester {sem}</span>
                <span class="px-3.5 py-1 rounded-full text-xs font-bold bg-purple-100 text-purple-700">{year}</span>
                <span class="px-3.5 py-1 rounded-full text-xs font-bold bg-yellow-100 text-yellow-800">Branches: {branches_str}</span>
            </div>

            <h1 class="text-3xl sm:text-4xl lg:text-5xl font-black text-gray-900 font-display tracking-tight mb-3">
                {name} <span class="text-blue-600">({code})</span>
            </h1>
            <p class="text-base sm:text-lg text-gray-600 max-w-4xl leading-relaxed mb-6">
                Official MSBTE solved question papers with step-wise model solutions, evaluation marking schemes, and summer/winter board exam solutions for Maharashtra polytechnic diploma students.
            </p>

            <!-- Hallmark Seal Banner -->
            <div class="bg-gradient-to-r from-blue-50 to-indigo-50/60 border border-blue-200/80 rounded-2xl p-4 sm:p-5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-6">
                <div class="flex items-center gap-3.5">
                    <div class="w-11 h-11 rounded-2xl bg-blue-600 text-white flex items-center justify-center text-xl flex-shrink-0 shadow-md">
                        🛡️
                    </div>
                    <div>
                        <div class="text-sm font-bold text-blue-900 flex items-center gap-2">
                            <span>MSBTE Hallmark Quality Guarantee</span>
                            <span class="px-2 py-0.5 rounded text-2xs font-extrabold bg-blue-600 text-white uppercase tracking-wider">Verified</span>
                        </div>
                        <p class="text-xs text-blue-800/80 mt-0.5">100% verified model answers with examiner step-marking points, formula derivations, and standard diagrams.</p>
                    </div>
                </div>
                <div class="flex items-center gap-2 text-xs font-semibold text-blue-700 whitespace-nowrap">
                    <span class="inline-block w-2 h-2 rounded-full bg-emerald-500 animate-ping"></span>
                    <span>Updated for 2026/2025 Board Exams</span>
                </div>
            </div>

            <!-- Quick Jump Nav -->
            <div class="flex items-center gap-2 overflow-x-auto py-2 no-scrollbar text-sm border-t border-gray-100 pt-5">
                <span class="text-xs font-bold text-gray-400 uppercase tracking-wider flex-shrink-0">Jump To:</span>
                <a href="#download-section" class="px-3.5 py-1.5 rounded-full bg-blue-50 text-blue-700 font-semibold hover:bg-blue-100 transition whitespace-nowrap">📥 Solved Papers ({len(papers)})</a>
                <a href="#preview-section" class="px-3.5 py-1.5 rounded-full bg-gray-100 text-gray-700 font-medium hover:bg-gray-200 transition whitespace-nowrap">👁️ Live Preview</a>
                <a href="#marking-scheme" class="px-3.5 py-1.5 rounded-full bg-gray-100 text-gray-700 font-medium hover:bg-gray-200 transition whitespace-nowrap">⚖️ Marking Scheme</a>
                <a href="#syllabus-units" class="px-3.5 py-1.5 rounded-full bg-gray-100 text-gray-700 font-medium hover:bg-gray-200 transition whitespace-nowrap">📚 Units &amp; Marks</a>
                <a href="#repeated-questions" class="px-3.5 py-1.5 rounded-full bg-gray-100 text-gray-700 font-medium hover:bg-gray-200 transition whitespace-nowrap">⭐ Repeated Questions</a>
                <a href="#faqs" class="px-3.5 py-1.5 rounded-full bg-gray-100 text-gray-700 font-medium hover:bg-gray-200 transition whitespace-nowrap">❓ FAQs</a>
            </div>
        </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">

        <!-- Authentic Thumbnail Card Banner -->
        <div class="overflow-hidden rounded-3xl border border-gray-200/90 shadow-md bg-white">
            <img src="{thumb_url}" alt="MSBTE {name} ({code}) Model Answer Paper Thumbnail Banner" class="w-full h-auto object-cover max-h-96" loading="eager">
        </div>

        <!-- 1. Download Model Answer Papers Section -->
        <section id="download-section">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-6">
                <div>
                    <h2 class="text-2xl font-bold font-display text-gray-900 flex items-center gap-2">
                        <span class="w-8 h-8 rounded-xl bg-blue-100 text-blue-600 flex items-center justify-center text-base">📑</span>
                        Available Model Answer Papers
                    </h2>
                    <p class="text-sm text-gray-500 mt-1">Download official board solutions with step-wise marks distribution</p>
                </div>
                <div class="text-xs font-semibold px-3 py-1.5 bg-blue-50 text-blue-700 rounded-full border border-blue-100 w-max">
                    Total Available: {len(papers)} Exams
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
{download_cards_str}
            </div>
        </section>

        <!-- In-Article AdSense Ad -->
        <div class="my-8 text-center">
            <ins class="adsbygoogle" style="display:block; text-align:center;" data-ad-layout="in-article"
                data-ad-format="fluid" data-ad-client="ca-pub-9227354288966999" data-ad-slot="7917907402"></ins>
            <script>
                (adsbygoogle = window.adsbygoogle || []).push({{}});
            </script>
        </div>

        <!-- 2. Interactive Live PDF Preview -->
        <section id="preview-section" class="bg-white p-6 sm:p-8 rounded-3xl border border-gray-200/90 shadow-sm">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4">
                <div>
                    <h2 class="text-xl font-bold font-display text-gray-900 flex items-center gap-2">
                        <span class="w-8 h-8 rounded-xl bg-indigo-100 text-indigo-600 flex items-center justify-center text-base">👁️</span>
                        Live Solution Preview ({latest_exam})
                    </h2>
                    <p class="text-xs text-gray-500 mt-0.5">Read paper directly without leaving the page</p>
                </div>
                <a href="{latest_paper['download_link'] if latest_paper else '#'}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1.5 text-sm font-semibold text-blue-600 hover:text-blue-700 transition">
                    <span>Download This PDF</span>
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
                </a>
            </div>
            <div class="w-full rounded-2xl overflow-hidden border border-gray-200 bg-gray-50 relative" style="height: 540px;">
                <iframe src="https://drive.google.com/file/d/{latest_drive_id}/preview" class="w-full h-full border-0" allow="autoplay" loading="lazy"></iframe>
            </div>
        </section>

        <!-- YouTube Banner -->
        <section class="bg-gradient-to-r from-red-600 via-red-600 to-rose-700 rounded-3xl p-6 sm:p-8 text-white shadow-lg flex flex-col md:flex-row items-center justify-between gap-6">
            <div class="space-y-2 text-center md:text-left">
                <span class="px-3 py-1 rounded-full text-xs font-bold bg-white/20 uppercase tracking-wider">Official YouTube Channel</span>
                <h3 class="text-2xl sm:text-3xl font-black font-display">Watch {abbr} Video Solutions &amp; Tips</h3>
                <p class="text-red-100 text-sm max-w-xl">Subscribe to MSBTE Notes &amp; Info on YouTube for detailed question-by-question walkthroughs, paper presentation hacks, and exam tips.</p>
            </div>
            <a href="https://www.youtube.com/@msbte-notes-and-info?sub_confirmation=1" target="_blank" rel="noopener noreferrer" class="px-6 py-3.5 rounded-2xl bg-white text-red-600 hover:bg-red-50 font-bold text-sm shadow-md transition flex items-center gap-2 flex-shrink-0">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 576 512"><path d="M549.655 124.083c-6.281-23.65-24.787-42.276-48.284-48.597C458.781 64 288 64 288 64S117.22 64 74.629 75.486c-23.497 6.322-42.003 24.947-48.284 48.597-11.412 42.867-11.412 132.305-11.412 132.305s0 89.438 11.412 132.305c6.281 23.65 24.787 41.5 48.284 47.821C117.22 448 288 448 288 448s170.78 0 213.371-11.486c23.497-6.321 42.003-24.171 48.284-47.821 11.412-42.867 11.412-132.305 11.412-132.305s0-89.438-11.412-132.305zm-317.51 213.583V174.334l142.039 81.666-142.039 81.666z"/></svg>
                Subscribe on YouTube
            </a>
        </section>

        <!-- 3. MSBTE Marking Scheme & Strategy -->
        <section id="marking-scheme" class="bg-white p-6 sm:p-8 rounded-3xl border border-gray-200/90 shadow-sm space-y-4">
            <h2 class="text-2xl font-bold font-display text-gray-900 flex items-center gap-2">
                <span class="w-8 h-8 rounded-xl bg-emerald-100 text-emerald-600 flex items-center justify-center text-base">⚖️</span>
                MSBTE Step-Wise Marking Methodology for {abbr}
            </h2>
            <p class="text-gray-600 leading-relaxed text-sm">
                MSBTE examiners evaluate answer sheets based on rigorous step-wise marking guidelines issued with each model answer paper. Here is how marks are distributed across question types:
            </p>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
                <div class="bg-blue-50/50 p-5 rounded-2xl border border-blue-100">
                    <h3 class="font-bold text-blue-900 text-base mb-1">Diagrams &amp; Schematics</h3>
                    <p class="text-xs text-blue-800 leading-relaxed">Up to 40%–50% of total marks in a question are reserved for a correct, labelled diagram. Always draw diagrams in dark pencil with distinct pin/node labels.</p>
                </div>
                <div class="bg-emerald-50/50 p-5 rounded-2xl border border-emerald-100">
                    <h3 class="font-bold text-emerald-900 text-base mb-1">Formulas &amp; Derivations</h3>
                    <p class="text-xs text-emerald-800 leading-relaxed">Stating the governing equation earns 1 mark, substitution earns 1–2 marks, and correct arithmetic with SI units receives final marks.</p>
                </div>
                <div class="bg-purple-50/50 p-5 rounded-2xl border border-purple-100">
                    <h3 class="font-bold text-purple-900 text-base mb-1">Code &amp; Algorithm Syntax</h3>
                    <p class="text-xs text-purple-800 leading-relaxed">Minor syntax errors are forgiven if algorithm logic, comments, and data flow are intact. Always include input, process, and output stages.</p>
                </div>
            </div>
        </section>

        <!-- 4. Syllabus Units & Weightage -->
        <section id="syllabus-units" class="bg-white p-6 sm:p-8 rounded-3xl border border-gray-200/90 shadow-sm">
            <h2 class="text-2xl font-bold font-display text-gray-900 flex items-center gap-2 mb-4">
                <span class="w-8 h-8 rounded-xl bg-blue-100 text-blue-600 flex items-center justify-center text-base">📚</span>
                Syllabus Units &amp; Marks Distribution
            </h2>
            <div class="overflow-x-auto rounded-2xl border border-gray-200">
                <table class="w-full text-left text-sm text-gray-600">
                    <thead class="bg-gray-50 text-xs uppercase font-bold text-gray-500 border-b border-gray-200">
                        <tr>
                            <th class="px-5 py-3">Unit</th>
                            <th class="px-5 py-3">Unit Title</th>
                            <th class="px-5 py-3 text-center">Exam Weightage</th>
                        </tr>
                    </thead>
                    <tbody>
{units_html_str}
                    </tbody>
                </table>
            </div>
        </section>

        <!-- 5. Repeated Board Questions -->
        <section id="repeated-questions">
            <div class="mb-6">
                <h2 class="text-2xl font-bold font-display text-gray-900 flex items-center gap-2">
                    <span class="w-8 h-8 rounded-xl bg-yellow-100 text-yellow-600 flex items-center justify-center text-base">⭐</span>
                    High-Frequency Repeated Board Questions
                </h2>
                <p class="text-sm text-gray-500 mt-1">Questions appearing in multiple MSBTE board exams with verified solutions</p>
            </div>
            <div class="space-y-3">
{questions_html_str}
            </div>
        </section>

        <!-- WhatsApp CTA -->
        <section class="bg-emerald-50 border border-emerald-200 rounded-3xl p-6 sm:p-8 flex flex-col sm:flex-row items-center justify-between gap-6 shadow-sm">
            <div class="flex items-center gap-4">
                <div class="w-12 h-12 rounded-2xl bg-emerald-500 text-white flex items-center justify-center text-2xl flex-shrink-0 shadow-md">
                    💬
                </div>
                <div>
                    <h3 class="text-xl font-bold text-gray-900 font-display">Get {abbr} Important Questions on WhatsApp</h3>
                    <p class="text-sm text-gray-600">Join 15,000+ MSBTE students receiving unit test question banks &amp; exam updates.</p>
                </div>
            </div>
            <a href="https://wa.me/917083236221?text=Hello%2C%20I%20want%20the%20MSBTE%20{abbr}%20{code}%20Important%20Question%20Bank" target="_blank" rel="noopener noreferrer" class="px-6 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-sm transition shadow-sm flex items-center gap-2 flex-shrink-0">
                Send Message (+91 70832 36221)
            </a>
        </section>

        <!-- Bottom Responsive AdSense Ad -->
        <div class="my-8 text-center">
            <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-9227354288966999"
                data-ad-slot="1275037071" data-ad-format="auto" data-full-width-responsive="true"></ins>
            <script>
                (adsbygoogle = window.adsbygoogle || []).push({{}});
            </script>
        </div>

        <!-- 6. FAQs Accordion -->
        <section id="faqs" class="bg-white p-6 sm:p-8 rounded-3xl border border-gray-200/90 shadow-sm">
            <h2 class="text-2xl font-bold font-display text-gray-900 flex items-center gap-2 mb-6">
                <span class="w-8 h-8 rounded-xl bg-purple-100 text-purple-600 flex items-center justify-center text-base">❓</span>
                Frequently Asked Questions
            </h2>
            <div class="space-y-3">
{faq_html_str}
            </div>
        </section>

    </main>

{FOOTER_HTML}

</body>
</html>"""
    return html

def generate_hub_page(subjects_data):
    cards_html = []
    for idx, (name, info) in enumerate(subjects_data.items()):
        code = info['code']
        slug = info['slug']
        abbr = info['abbr']
        sem = info['sem']
        branches = info['branches']
        branches_str = ", ".join(branches)
        papers = info.get('papers', {})
        paper_count = len(papers)
        thumb_url = PNG_THUMB_MAP.get(name, f"/resourse/msbte_subject_thumbnails/{idx+1:02d}_{name.replace(' ', '_').replace('&', 'and')}.png")
        
        branch_badges = " ".join([f'<span class="px-2 py-0.5 rounded text-xs font-semibold bg-gray-100 text-gray-700">{b}</span>' for b in branches])
        
        cards_html.append(f"""            <div class="res-card bg-white rounded-3xl border border-gray-200/90 shadow-sm overflow-hidden flex flex-col justify-between" 
                 data-name="{name.lower()}" 
                 data-code="{code}" 
                 data-abbr="{abbr.lower()}" 
                 data-sem="{sem}" 
                 data-branches="{','.join(branches)}">
                <div>
                    <a href="/model-answer/{slug}.html" class="block overflow-hidden bg-gray-100 relative group">
                        <img src="{thumb_url}" alt="{name} {code} Model Answer Thumbnail" class="w-full h-48 object-cover transform group-hover:scale-105 transition-transform duration-300" loading="lazy">
                        <div class="absolute top-3 left-3 flex gap-1.5 flex-wrap">
                            <span class="px-2.5 py-1 rounded-full text-xs font-bold bg-blue-600 text-white shadow-sm">K-Scheme</span>
                            <span class="px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-600 text-white shadow-sm">{paper_count} Solved Papers</span>
                        </div>
                    </a>
                    <div class="p-6">
                        <div class="flex items-center justify-between gap-2 mb-2">
                            <span class="text-xs font-bold uppercase tracking-wider text-blue-600">Sem {sem} &bull; Code {code}</span>
                            <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-purple-50 text-purple-700 border border-purple-200">{abbr}</span>
                        </div>
                        <h3 class="text-xl font-bold font-display text-gray-900 mb-2 leading-snug">
                            <a href="/model-answer/{slug}.html" class="hover:text-blue-600 transition">{name}</a>
                        </h3>
                        <div class="flex flex-wrap gap-1 mt-3">
                            {branch_badges}
                        </div>
                    </div>
                </div>
                <div class="px-6 pb-6 pt-2 border-t border-gray-100">
                    <a href="/model-answer/{slug}.html" class="w-full inline-flex items-center justify-center gap-2 py-3 px-4 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-semibold text-sm transition shadow-sm">
                        <span>View Solved Papers</span>
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
                    </a>
                </div>
            </div>""")

    all_cards_str = "\n".join(cards_html)
    canonical_url = "https://msbtenotes-info.netlify.app/model-answer/"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Consent default (deny until user chooses) -->
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('consent', 'default', {{ 'ad_storage': 'denied', 'analytics_storage': 'denied' }});
    </script>
    <!-- Google Tag & Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-H5G5CCD95W"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'G-H5G5CCD95W');
    </script>
    <!-- Google AdSense -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9227354288966999" crossorigin="anonymous"></script>

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MSBTE Model Answer Papers K-Scheme — Download Solved Question Papers</title>
    <meta name="description" content="Download official MSBTE K-Scheme model answer papers, summer &amp; winter solved solutions, and step-wise marking schemes for Computer, IT, and AI &amp; ML diploma courses.">
    <meta name="keywords" content="MSBTE model answer, MSBTE model answer paper, MSBTE solved question paper, MSBTE K scheme model answer, MSBTE computer engineering model answer">
    <link rel="canonical" href="{canonical_url}">

    <!-- Open Graph -->
    <meta property="og:title" content="MSBTE Model Answer Papers K-Scheme — Download Solved Question Papers">
    <meta property="og:description" content="Download official MSBTE K-Scheme model answer papers, summer &amp; winter solved solutions, and step-wise marking schemes for Computer, IT, and AI &amp; ML diploma courses.">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:image" content="https://msbtenotes-info.netlify.app/resourse/msbte_subject_thumbnails/01_Data_Structures_Using_C.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:type" content="website">

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:site" content="@msbtenotes">
    <meta name="twitter:title" content="MSBTE Model Answer Papers K-Scheme — Download Solved Question Papers">
    <meta name="twitter:description" content="Download official MSBTE K-Scheme model answer papers, summer &amp; winter solved solutions, and step-wise marking schemes for Computer, IT, and AI &amp; ML diploma courses.">
    <meta name="twitter:image" content="https://msbtenotes-info.netlify.app/resourse/msbte_subject_thumbnails/01_Data_Structures_Using_C.png">

    <!-- Styles -->
    <link rel="stylesheet" href="/style.css">
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link href="https://api.fontshare.com/v2/css?f[]=clash-display@600,700&display=swap" rel="stylesheet">

    <!-- JSON-LD: CollectionPage -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "MSBTE Model Answer Papers K-Scheme",
        "description": "Download official MSBTE K-Scheme model answer papers and solved solutions for Maharashtra diploma engineering.",
        "url": "{canonical_url}",
        "publisher": {{
            "@type": "Organization",
            "name": "MSBTE Notes & Info",
            "logo": {{
                "@type": "ImageObject",
                "url": "https://msbtenotes-info.netlify.app/resourse/android-chrome-512x512.png"
            }}
        }}
    }}
    </script>

    <style>
        .font-display {{ font-family: 'Clash Display', sans-serif; }}
        .res-card {{
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        }}
        .res-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 12px 28px -6px rgba(0, 0, 0, 0.1);
        }}
    </style>
</head>
<body class="bg-gray-50 text-gray-900 pt-16">

{NAV_HTML}

    <!-- Hero Section -->
    <header class="bg-gradient-to-b from-blue-50 to-gray-50 border-b border-gray-200/80 py-12 sm:py-16">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <span class="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full text-xs font-bold bg-blue-100 text-blue-800 uppercase tracking-wider mb-4 shadow-sm">
                ✨ Official Board Solutions &bull; K-Scheme Curriculum
            </span>
            <h1 class="text-3xl sm:text-5xl font-black font-display text-gray-900 tracking-tight mb-4">
                MSBTE <span class="text-blue-600">Model Answer Papers</span>
            </h1>
            <p class="text-base sm:text-lg text-gray-600 max-w-2xl mx-auto leading-relaxed mb-8">
                Download verified MSBTE official model solutions with step-wise marks distribution, examiner evaluation keys, and question papers for diploma engineering.
            </p>

            <!-- Search and Filter Bar -->
            <div class="max-w-2xl mx-auto">
                <div class="relative">
                    <input type="text" id="modelSearchInput" oninput="filterCards()" placeholder="Search by subject name, 6-digit code (e.g. 313301), or abbr..." class="w-full px-5 py-4 pl-12 rounded-2xl border border-gray-300 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-base text-gray-900 bg-white" />
                    <svg class="w-5 h-5 text-gray-400 absolute left-4 top-4.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                </div>

                <!-- Filter Pills -->
                <div class="flex flex-wrap items-center justify-center gap-2 mt-4 text-xs font-semibold">
                    <span class="text-gray-400 uppercase tracking-wider mr-1">Filter Branch:</span>
                    <button type="button" onclick="setBranchFilter('all', this)" class="branch-filter-btn px-3.5 py-1.5 rounded-full bg-blue-600 text-white font-bold transition shadow-sm">All</button>
                    <button type="button" onclick="setBranchFilter('CO', this)" class="branch-filter-btn px-3.5 py-1.5 rounded-full bg-white text-gray-700 border border-gray-200 hover:bg-gray-100 transition">Computer (CO)</button>
                    <button type="button" onclick="setBranchFilter('IF', this)" class="branch-filter-btn px-3.5 py-1.5 rounded-full bg-white text-gray-700 border border-gray-200 hover:bg-gray-100 transition">IT (IF)</button>
                    <button type="button" onclick="setBranchFilter('AN', this)" class="branch-filter-btn px-3.5 py-1.5 rounded-full bg-white text-gray-700 border border-gray-200 hover:bg-gray-100 transition">AI &amp; ML (AN)</button>
                </div>

                <div class="flex flex-wrap items-center justify-center gap-2 mt-2 text-xs font-semibold">
                    <span class="text-gray-400 uppercase tracking-wider mr-1">Filter Semester:</span>
                    <button type="button" onclick="setSemFilter('all', this)" class="sem-filter-btn px-3.5 py-1.5 rounded-full bg-blue-600 text-white font-bold transition shadow-sm">All Semesters</button>
                    <button type="button" onclick="setSemFilter('3', this)" class="sem-filter-btn px-3.5 py-1.5 rounded-full bg-white text-gray-700 border border-gray-200 hover:bg-gray-100 transition">Semester 3</button>
                    <button type="button" onclick="setSemFilter('5', this)" class="sem-filter-btn px-3.5 py-1.5 rounded-full bg-white text-gray-700 border border-gray-200 hover:bg-gray-100 transition">Semester 5</button>
                </div>
            </div>
        </div>
    </header>

    <!-- Main Content Grid -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div class="flex items-center justify-between mb-8">
            <h2 class="text-2xl font-bold font-display text-gray-900 flex items-center gap-2">
                <span>Available Subjects</span>
                <span id="subjectCountBadge" class="text-xs px-2.5 py-0.5 rounded-full bg-blue-100 text-blue-700 font-bold">{len(subjects_data)}</span>
            </h2>
            <span class="text-xs text-gray-500">Official step-wise marking schemes</span>
        </div>

        <div id="modelCardsContainer" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
{all_cards_str}
        </div>

        <div id="noResultsNotice" class="hidden text-center py-16">
            <p class="text-gray-400 text-lg font-medium">No matching model answer papers found.</p>
            <button onclick="resetFilters()" class="mt-3 text-sm font-semibold text-blue-600 hover:underline">Reset search and filters</button>
        </div>

        <!-- Explanatory Guide Section -->
        <section class="mt-20 bg-white rounded-3xl p-8 sm:p-12 border border-gray-200 shadow-sm space-y-6">
            <h2 class="text-2xl sm:text-3xl font-bold font-display text-gray-900">
                Why MSBTE Model Answer Papers are Essential for High Scores
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm text-gray-600 leading-relaxed">
                <div>
                    <h3 class="font-bold text-gray-900 text-base mb-2">1. Step-Wise Marks Breakdown</h3>
                    <p>MSBTE examiners use the official model answer as their sole evaluation standard. Reviewing model solutions reveals exactly which definitions, formulas, and diagrams earn guaranteed partial credit.</p>
                </div>
                <div>
                    <h3 class="font-bold text-gray-900 text-base mb-2">2. Standard Presentation Style</h3>
                    <p>Learn how top students format comparative answers into tables, write clean algorithms with proper indentation, and sketch high-scoring engineering diagrams with labeled pins.</p>
                </div>
                <div>
                    <h3 class="font-bold text-gray-900 text-base mb-2">3. Identifying Repeated Patterns</h3>
                    <p>Comparing 3 to 5 successive board exam model answers reveals the recurring 4-mark and 6-mark questions that account for more than 60% of every question paper.</p>
                </div>
            </div>
        </section>
    </main>

{FOOTER_HTML}

    <!-- Filtering script -->
    <script>
        let currentBranch = 'all';
        let currentSem = 'all';

        function filterCards() {{
            const query = (document.getElementById('modelSearchInput').value || '').toLowerCase().trim();
            const cards = document.querySelectorAll('#modelCardsContainer .res-card');
            let visibleCount = 0;

            cards.forEach(card => {{
                const name = card.getAttribute('data-name');
                const code = card.getAttribute('data-code');
                const abbr = card.getAttribute('data-abbr');
                const sem = card.getAttribute('data-sem');
                const branches = (card.getAttribute('data-branches') || '').split(',');

                const matchesQuery = !query || name.includes(query) || code.includes(query) || abbr.includes(query);
                const matchesBranch = currentBranch === 'all' || branches.includes(currentBranch);
                const matchesSem = currentSem === 'all' || sem === currentSem;

                if (matchesQuery && matchesBranch && matchesSem) {{
                    card.style.display = '';
                    visibleCount++;
                }} else {{
                    card.style.display = 'none';
                }}
            }});

            const noResults = document.getElementById('noResultsNotice');
            if (noResults) {{
                noResults.classList.toggle('hidden', visibleCount > 0);
            }}
            const countBadge = document.getElementById('subjectCountBadge');
            if (countBadge) {{
                countBadge.innerText = visibleCount;
            }}
        }}

        function setBranchFilter(branch, btn) {{
            currentBranch = branch;
            document.querySelectorAll('.branch-filter-btn').forEach(b => {{
                b.className = 'branch-filter-btn px-3.5 py-1.5 rounded-full bg-white text-gray-700 border border-gray-200 hover:bg-gray-100 transition';
            }});
            btn.className = 'branch-filter-btn px-3.5 py-1.5 rounded-full bg-blue-600 text-white font-bold transition shadow-sm';
            filterCards();
        }}

        function setSemFilter(sem, btn) {{
            currentSem = sem;
            document.querySelectorAll('.sem-filter-btn').forEach(b => {{
                b.className = 'sem-filter-btn px-3.5 py-1.5 rounded-full bg-white text-gray-700 border border-gray-200 hover:bg-gray-100 transition';
            }});
            btn.className = 'sem-filter-btn px-3.5 py-1.5 rounded-full bg-blue-600 text-white font-bold transition shadow-sm';
            filterCards();
        }}

        function resetFilters() {{
            document.getElementById('modelSearchInput').value = '';
            currentBranch = 'all';
            currentSem = 'all';
            document.querySelectorAll('.branch-filter-btn').forEach((b, i) => {{
                b.className = i === 0 ? 'branch-filter-btn px-3.5 py-1.5 rounded-full bg-blue-600 text-white font-bold transition shadow-sm' : 'branch-filter-btn px-3.5 py-1.5 rounded-full bg-white text-gray-700 border border-gray-200 hover:bg-gray-100 transition';
            }});
            document.querySelectorAll('.sem-filter-btn').forEach((b, i) => {{
                b.className = i === 0 ? 'sem-filter-btn px-3.5 py-1.5 rounded-full bg-blue-600 text-white font-bold transition shadow-sm' : 'sem-filter-btn px-3.5 py-1.5 rounded-full bg-white text-gray-700 border border-gray-200 hover:bg-gray-100 transition';
            }});
            filterCards();
        }}
    </script>
</body>
</html>"""
    return html

def update_notes_resources_json(subjects_data):
    """Adds the 14 model answer items to Notes/resources.json as requested."""
    if not os.path.exists(NOTES_RES_PATH):
        print("Notes/resources.json not found!")
        return

    with open(NOTES_RES_PATH, 'r', encoding='utf-8') as f:
        notes_res = json.load(f)

    # Filter out existing model-answer items if re-running
    notes_res = [item for item in notes_res if not item.get('url', '').startswith('/model-answer/')]

    for idx, (name, info) in enumerate(subjects_data.items()):
        code = info['code']
        slug = info['slug']
        abbr = info['abbr']
        sem = info['sem']
        branches = info['branches']
        papers = info.get('papers', {})
        thumb_url = PNG_THUMB_MAP.get(name, f"/resourse/msbte_subject_thumbnails/{idx+1:02d}_{name.replace(' ', '_').replace('&', 'and')}.png")

        entry = {
            "title": f"{name} ({code}) Model Answer Papers & Solved Solutions",
            "description": f"Download official MSBTE K-Scheme model answer papers with step-wise solutions, evaluation marking schemes, and exam keys for {name} ({code}) - Semester {sem}.",
            "url": f"/model-answer/{slug}.html",
            "thumbnail": thumb_url,
            "category": "model-answer",
            "tags": [abbr, str(code), "Model Answer", f"Sem {sem}", "K-Scheme"] + branches,
            "code": code,
            "abbreviation": abbr,
            "semester": sem,
            "academic_year": info['year'],
            "branches": branches,
            "branches_str": info['branch_names'],
            "slug": slug,
            "papers_count": len(papers),
            "dateAdded": "2026-11-10"
        }
        notes_res.append(entry)

    with open(NOTES_RES_PATH, 'w', encoding='utf-8') as f:
        json.dump(notes_res, f, indent=2)
    print(f"Updated Notes/resources.json with {len(subjects_data)} model answer entries (Total items: {len(notes_res)}).")

def update_sitemap(subjects_data):
    """Updates sitemap.xml to include /model-answer/ and all 14 subject pages."""
    if not os.path.exists(SITEMAP_PATH):
        print("sitemap.xml not found!")
        return

    ET.register_namespace('', "http://www.sitemaps.org/schemas/sitemap/0.9")
    tree = ET.parse(SITEMAP_PATH)
    root = tree.getroot()
    ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

    existing_locs = set(elem.text.strip() for elem in root.findall('ns:url/ns:loc', ns) if elem.text)
    today = datetime.now().strftime("%Y-%m-%d")

    new_urls = [
        ("https://msbtenotes-info.netlify.app/model-answer/", "0.9")
    ]
    for idx, (name, info) in enumerate(subjects_data.items()):
        slug = info['slug']
        new_urls.append((f"https://msbtenotes-info.netlify.app/model-answer/{slug}.html", "0.8"))

    added_count = 0
    for loc, priority in new_urls:
        if loc not in existing_locs:
            url_elem = ET.SubElement(root, 'url')
            loc_elem = ET.SubElement(url_elem, 'loc')
            loc_elem.text = loc
            lastmod_elem = ET.SubElement(url_elem, 'lastmod')
            lastmod_elem.text = today
            changefreq_elem = ET.SubElement(url_elem, 'changefreq')
            changefreq_elem.text = 'weekly'
            priority_elem = ET.SubElement(url_elem, 'priority')
            priority_elem.text = priority
            added_count += 1

    tree.write(SITEMAP_PATH, encoding='utf-8', xml_declaration=True)
    print(f"Updated sitemap.xml with {added_count} new model-answer URLs.")

def update_redirects():
    """Updates _redirects to include /model-answer/ clean URLs and uppercase redirects."""
    if not os.path.exists(REDIRECTS_PATH):
        return

    with open(REDIRECTS_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Uppercase and alias rules
    if "/model-answer/*" not in content and "/Model-Answer/*" not in content:
        target_marker = "# ------------------------------------------\n# PYQ Subject ID Aliases"
        replacement = """/Model-Answer/*    /model-answer/:splat    301!
/model-answers/*   /model-answer/:splat    301!
/model-answers     /model-answer/          301!

# ------------------------------------------
# PYQ Subject ID Aliases"""
        if target_marker in content:
            content = content.replace(target_marker, replacement)
        else:
            content = content.replace("/PYQ/*     /pyq/:splat     301!", "/PYQ/*     /pyq/:splat     301!\n/Model-Answer/*    /model-answer/:splat    301!\n/model-answers/*   /model-answer/:splat    301!\n/model-answers     /model-answer/          301!")

    # 200 rewrite rule before 404
    if "/model-answer/:slug" not in content:
        rewrite_rule = "/model-answer/:slug    /model-answer/:slug.html    200\n"
        content = content.replace("# 5. Proper 404 catch-all", rewrite_rule + "\n# 5. Proper 404 catch-all")

    with open(REDIRECTS_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated _redirects with model-answer routing rules.")

def main():
    print("Starting generation of MSBTE K-Scheme Model Answer pages with authentic PNG thumbnails...")
    with open(MODEL_DATA_PATH, 'r', encoding='utf-8') as f:
        subjects_data = json.load(f)

    catalog_entries = []

    # 1. Generate individual subject pages
    for idx, (name, info) in enumerate(subjects_data.items()):
        slug = info['slug']
        code = info['code']
        thumb_url = PNG_THUMB_MAP.get(name, f"/resourse/msbte_subject_thumbnails/{idx+1:02d}_{name.replace(' ', '_').replace('&', 'and')}.png")
        print(f"Generating [{idx+1}/{len(subjects_data)}] {name} ({code}) -> {slug} using {thumb_url}...")
        
        page_html = generate_subject_page(name, info, idx)
        
        # Save as model-answer/{slug}.html
        file_path = os.path.join(OUTPUT_DIR, f"{slug}.html")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(page_html)
            
        # Save as model-answer/{slug}/index.html for dual routing
        folder_path = os.path.join(OUTPUT_DIR, slug)
        os.makedirs(folder_path, exist_ok=True)
        with open(os.path.join(folder_path, "index.html"), 'w', encoding='utf-8') as f:
            f.write(page_html)

        catalog_entries.append({
            "code": code,
            "title": f"{name} ({code}) Model Answer Papers",
            "subject_name": name,
            "abbreviation": info['abbr'],
            "semester": info['sem'],
            "academic_year": info['year'],
            "branches": info['branches'],
            "branches_str": info['branch_names'],
            "slug": slug,
            "url": f"/model-answer/{slug}.html",
            "image": thumb_url,
            "papers": info.get('papers', {})
        })

    # 2. Save model-answer/resources.json
    res_path = os.path.join(OUTPUT_DIR, "resources.json")
    with open(res_path, 'w', encoding='utf-8') as f:
        json.dump(catalog_entries, f, indent=2)
    print(f"Saved {res_path} ({len(catalog_entries)} entries)")

    # 3. Generate master portal model-answer/index.html
    portal_html = generate_hub_page(subjects_data)
    portal_path = os.path.join(OUTPUT_DIR, "index.html")
    with open(portal_path, 'w', encoding='utf-8') as f:
        f.write(portal_html)
    print(f"Saved master portal {portal_path}")

    # 4. Update Notes/resources.json
    update_notes_resources_json(subjects_data)

    # 5. Update sitemap.xml
    update_sitemap(subjects_data)

    # 6. Update _redirects
    update_redirects()

    print("Model answer pages generation completed successfully with 100% theme alignment and pro SEO!")

if __name__ == '__main__':
    main()
