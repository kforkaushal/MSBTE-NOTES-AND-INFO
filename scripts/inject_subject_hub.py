#!/usr/bin/env python3
"""
Inject Subject Hub Component (Additive Cross-linking)
MSBTE Notes & Information
Adds a self-contained <nav class="subject-hub"> block to all subject pages across:
  - Branches/{code}-{slug}.html
  - Notes/{code}-{slug}.html
  - pyq/{code}-{slug}.html & pyq/{code}-{slug}/index.html
  - model-answer/{code}-{slug}.html & model-answer/{code}-{slug}/index.html

Non-destructive guarantee:
  - Additive only: never modifies <head>, meta tags, titles, canonicals, or JSON-LD.
  - Only links to pages that actually exist on disk.
  - Fully idempotent: running multiple times safely replaces or skips.
"""

import os
import glob
import re
import sys

# Add scripts directory to path to import collect_subject_hub_data
sys.path.insert(0, os.path.dirname(__file__))
from generate_hub import collect_subject_hub_data

def build_subject_hub_block(subject, current_page_type):
    code = subject['code']
    name = subject['name']
    links = subject['links']
    
    # Generate cards for available resources
    items = []
    
    # 1. Syllabus & Guide
    if 'syllabus' in links:
        is_cur = (current_page_type == 'syllabus')
        if is_cur:
            items.append('''
                <div class="p-3 bg-blue-100/60 rounded-xl border border-blue-300 flex items-center justify-between min-h-[44px]">
                    <div class="flex items-center gap-2">
                        <span class="text-base">📖</span>
                        <span class="text-xs font-bold text-blue-900">Syllabus &amp; Guide</span>
                    </div>
                    <span class="text-[10px] font-bold text-blue-700 bg-white px-2 py-0.5 rounded shadow-xs">Current</span>
                </div>
            ''')
        else:
            items.append(f'''
                <a href="{links['syllabus']}" class="p-3 bg-white hover:bg-blue-50 rounded-xl border border-gray-200 hover:border-blue-300 transition flex items-center justify-between group min-h-[44px]">
                    <div class="flex items-center gap-2">
                        <span class="text-base">📖</span>
                        <span class="text-xs font-bold text-gray-900 group-hover:text-blue-600 transition">Syllabus &amp; Guide</span>
                    </div>
                    <span class="text-xs text-blue-600 font-semibold group-hover:translate-x-0.5 transition-transform">&rarr;</span>
                </a>
            ''')

    # 2. Unit Notes & IMPs
    if 'notes' in links:
        is_cur = (current_page_type == 'notes')
        if is_cur:
            items.append('''
                <div class="p-3 bg-blue-100/60 rounded-xl border border-blue-300 flex items-center justify-between min-h-[44px]">
                    <div class="flex items-center gap-2">
                        <span class="text-base">📝</span>
                        <span class="text-xs font-bold text-blue-900">Unit Notes &amp; IMPs</span>
                    </div>
                    <span class="text-[10px] font-bold text-blue-700 bg-white px-2 py-0.5 rounded shadow-xs">Current</span>
                </div>
            ''')
        else:
            items.append(f'''
                <a href="{links['notes']}" class="p-3 bg-white hover:bg-blue-50 rounded-xl border border-gray-200 hover:border-blue-300 transition flex items-center justify-between group min-h-[44px]">
                    <div class="flex items-center gap-2">
                        <span class="text-base">📝</span>
                        <span class="text-xs font-bold text-gray-900 group-hover:text-blue-600 transition">Unit Notes &amp; IMPs</span>
                    </div>
                    <span class="text-xs text-blue-600 font-semibold group-hover:translate-x-0.5 transition-transform">&rarr;</span>
                </a>
            ''')

    # 3. Previous Year Question Papers (PYQ)
    if 'pyq' in links:
        is_cur = (current_page_type == 'pyq')
        if is_cur:
            items.append('''
                <div class="p-3 bg-blue-100/60 rounded-xl border border-blue-300 flex items-center justify-between min-h-[44px]">
                    <div class="flex items-center gap-2">
                        <span class="text-base">📄</span>
                        <span class="text-xs font-bold text-blue-900">PYQ Question Papers</span>
                    </div>
                    <span class="text-[10px] font-bold text-blue-700 bg-white px-2 py-0.5 rounded shadow-xs">Current</span>
                </div>
            ''')
        else:
            items.append(f'''
                <a href="{links['pyq']}" class="p-3 bg-white hover:bg-rose-50 rounded-xl border border-gray-200 hover:border-rose-300 transition flex items-center justify-between group min-h-[44px]">
                    <div class="flex items-center gap-2">
                        <span class="text-base">📄</span>
                        <span class="text-xs font-bold text-gray-900 group-hover:text-rose-600 transition">PYQ Papers (Drive)</span>
                    </div>
                    <span class="text-xs text-rose-600 font-semibold group-hover:translate-x-0.5 transition-transform">&rarr;</span>
                </a>
            ''')

    # 4. Solved Model Answer
    if 'model_answer' in links:
        is_cur = (current_page_type == 'model_answer')
        if is_cur:
            items.append('''
                <div class="p-3 bg-blue-100/60 rounded-xl border border-blue-300 flex items-center justify-between min-h-[44px]">
                    <div class="flex items-center gap-2">
                        <span class="text-base">💡</span>
                        <span class="text-xs font-bold text-blue-900">Model Answer Papers</span>
                    </div>
                    <span class="text-[10px] font-bold text-blue-700 bg-white px-2 py-0.5 rounded shadow-xs">Current</span>
                </div>
            ''')
        else:
            items.append(f'''
                <a href="{links['model_answer']}" class="p-3 bg-white hover:bg-emerald-50 rounded-xl border border-gray-200 hover:border-emerald-300 transition flex items-center justify-between group min-h-[44px]">
                    <div class="flex items-center gap-2">
                        <span class="text-base">💡</span>
                        <span class="text-xs font-bold text-gray-900 group-hover:text-emerald-600 transition">Solved Model Answer</span>
                    </div>
                    <span class="text-xs text-emerald-600 font-semibold group-hover:translate-x-0.5 transition-transform">&rarr;</span>
                </a>
            ''')

    # 5. Lab Manual & Practicals
    if 'lab_manual' in links:
        is_cur = (current_page_type == 'lab_manual')
        if is_cur:
            items.append('''
                <div class="p-3 bg-blue-100/60 rounded-xl border border-blue-300 flex items-center justify-between min-h-[44px]">
                    <div class="flex items-center gap-2">
                        <span class="text-base">🔬</span>
                        <span class="text-xs font-bold text-blue-900">Lab Manual Answers</span>
                    </div>
                    <span class="text-[10px] font-bold text-blue-700 bg-white px-2 py-0.5 rounded shadow-xs">Current</span>
                </div>
            ''')
        else:
            items.append(f'''
                <a href="{links['lab_manual']}" class="p-3 bg-white hover:bg-purple-50 rounded-xl border border-gray-200 hover:border-purple-300 transition flex items-center justify-between group min-h-[44px]">
                    <div class="flex items-center gap-2">
                        <span class="text-base">🔬</span>
                        <span class="text-xs font-bold text-gray-900 group-hover:text-purple-600 transition">Lab Manual Answers</span>
                    </div>
                    <span class="text-xs text-purple-600 font-semibold group-hover:translate-x-0.5 transition-transform">&rarr;</span>
                </a>
            ''')

    # 6. Official Syllabus PDF
    if 'syllabus_pdf' in links:
        items.append(f'''
            <a href="{links['syllabus_pdf']}" target="_blank" rel="noopener noreferrer" class="p-3 bg-white hover:bg-gray-100 rounded-xl border border-gray-200 hover:border-gray-300 transition flex items-center justify-between group min-h-[44px]">
                <div class="flex items-center gap-2">
                    <span class="text-base">📥</span>
                    <span class="text-xs font-bold text-gray-900 group-hover:text-blue-600 transition">Official Syllabus PDF</span>
                </div>
                <span class="text-xs text-gray-400 group-hover:text-blue-600 transition">&nearr;</span>
            </a>
        ''')

    items_html = "".join(items)

    hub_block = f'''
        <!-- Subject Resource Hub Block (Additive Cross-linking) -->
        <nav class="subject-hub my-10 p-5 sm:p-6 bg-gradient-to-br from-blue-50/70 via-indigo-50/40 to-white rounded-2xl border border-blue-200/90 shadow-sm not-prose" aria-label="Subject Resources Hub">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2.5 mb-4 pb-3 border-b border-blue-200/70">
                <div>
                    <span class="text-[11px] font-bold uppercase tracking-wider text-blue-700 bg-blue-100/80 px-2 py-0.5 rounded">All-In-One Study Hub</span>
                    <h3 class="text-base sm:text-lg font-bold font-display text-gray-900 mt-1">Study Materials for {code} – {name}</h3>
                </div>
                <a href="/start.html" class="inline-flex items-center gap-1 text-xs font-semibold text-blue-600 hover:text-blue-800 transition">
                    <span>All Subjects Directory</span>
                    <span>&rarr;</span>
                </a>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2.5">
                {items_html}
            </div>
        </nav>
'''
    return hub_block

def inject_hub_into_file(filepath, subject, page_type):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Generate hub block
    hub_html = build_subject_hub_block(subject, page_type)

    # Check if already injected
    if '<!-- Subject Resource Hub Block' in content or '<nav class="subject-hub"' in content:
        # Replace existing block cleanly
        new_content = re.sub(
            r'<!-- Subject Resource Hub Block.*?<\/nav>\s*',
            hub_html,
            content,
            flags=re.DOTALL
        )
    else:
        # Insert before </main> or before </article> or before <footer
        if '</main>' in content:
            new_content = content.replace('</main>', f'{hub_html}\n    </main>', 1)
        elif '</article>' in content:
            new_content = content.replace('</article>', f'{hub_html}\n    </article>', 1)
        elif '<footer' in content:
            new_content = content.replace('<footer', f'{hub_html}\n    <footer', 1)
        else:
            new_content = content.replace('</body>', f'{hub_html}\n</body>', 1)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def run_injection():
    subjects = {s['code']: s for s in collect_subject_hub_data()}
    print(f"Total subjects indexed: {len(subjects)}")

    updated_count = 0

    # 1. Branches/*.html
    for f in glob.glob('Branches/*.html'):
        m = re.match(r'^(\d{5,6})-(.+)\.html$', os.path.basename(f))
        if m:
            code = m.group(1)
            if code in subjects and len(subjects[code]['links']) > 1:
                if inject_hub_into_file(f, subjects[code], 'syllabus'):
                    updated_count += 1

    # 2. Notes/*.html
    for f in glob.glob('Notes/*.html'):
        m = re.match(r'^(\d{5,6})-(.+)\.html$', os.path.basename(f))
        if m:
            code = m.group(1)
            if code in subjects and len(subjects[code]['links']) > 1:
                if inject_hub_into_file(f, subjects[code], 'notes'):
                    updated_count += 1

    # 3. pyq/*.html & pyq/*-*/index.html
    for f in glob.glob('pyq/*.html'):
        m = re.match(r'^(\d{5,6})-(.+)\.html$', os.path.basename(f))
        if m:
            code = m.group(1)
            if code in subjects and len(subjects[code]['links']) > 1:
                if inject_hub_into_file(f, subjects[code], 'pyq'):
                    updated_count += 1

    for f in glob.glob('pyq/*-*/index.html'):
        dir_name = os.path.basename(os.path.dirname(f))
        m = re.match(r'^(\d{5,6})-(.+)$', dir_name)
        if m:
            code = m.group(1)
            if code in subjects and len(subjects[code]['links']) > 1:
                if inject_hub_into_file(f, subjects[code], 'pyq'):
                    updated_count += 1

    # 4. model-answer/*.html & model-answer/*-*/index.html
    for f in glob.glob('model-answer/*.html'):
        m = re.match(r'^(\d{5,6})-(.+)\.html$', os.path.basename(f))
        if m:
            code = m.group(1)
            if code in subjects and len(subjects[code]['links']) > 1:
                if inject_hub_into_file(f, subjects[code], 'model_answer'):
                    updated_count += 1

    for f in glob.glob('model-answer/*-*/index.html'):
        dir_name = os.path.basename(os.path.dirname(f))
        m = re.match(r'^(\d{5,6})-(.+)$', dir_name)
        if m:
            code = m.group(1)
            if code in subjects and len(subjects[code]['links']) > 1:
                if inject_hub_into_file(f, subjects[code], 'model_answer'):
                    updated_count += 1

    print(f"Injection complete! Successfully updated {updated_count} subject pages.")

if __name__ == '__main__':
    run_injection()

