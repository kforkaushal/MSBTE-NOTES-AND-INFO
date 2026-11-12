r"""
Replace corrupted Bharati Vidyapeeth syllabus PDF links with Google Drive Preview links
from D:\FlutterProjects\academia\docs\all_subjects_syllabus_drive_links.csv
and D:\FlutterProjects\academia\docs\consolidated_subjects_syllabus_drive_links.csv
"""

import os
import glob
import re
import csv
import json

CSV_ALL = r"D:\FlutterProjects\academia\docs\all_subjects_syllabus_drive_links.csv"
CSV_CONSOLIDATED = r"D:\FlutterProjects\academia\docs\consolidated_subjects_syllabus_drive_links.csv"

# 1. Load mappings
branch_subject_map = {}
with open(CSV_ALL, encoding='utf-8') as f:
    for r in csv.DictReader(f):
        b = r['branch_code'].strip().upper()
        c = r['subject_code'].strip()
        url = r['syllabus_preview_url'].strip()
        branch_subject_map[(b, c)] = url

code_map = {}
with open(CSV_CONSOLIDATED, encoding='utf-8') as f:
    for r in csv.DictReader(f):
        c = r['subject_code'].strip()
        url = r['primary_syllabus_preview_url'].strip()
        code_map[c] = url

print(f"Loaded {len(branch_subject_map)} branch-subject preview URLs from all_subjects CSV")
print(f"Loaded {len(code_map)} consolidated preview URLs")

# Branch slug mapping for branch semester pages
BRANCH_SLUG_MAP = {
    'ai-ml': 'AN',
    'civil': 'CE',
    'computer': 'CM',
    'etc-engineering': 'EJ',
    'electrical-engineering': 'EE',
    'information-technology': 'IF',
    'mechanical-engineering': 'ME',
}

def is_test_paper(url):
    return bool(re.search(r'(\bunit[-_]?test\b|\bqb\b|[_-]ut[1-2]?([_-]|$)|test[-_]?[1-2])', url, re.IGNORECASE))

def get_preview_url(code, branch_code=None):
    if branch_code and (branch_code.upper(), code) in branch_subject_map:
        return branch_subject_map[(branch_code.upper(), code)]
    return code_map.get(code)

total_files_modified = 0
total_links_replaced = 0

def replace_in_file(fpath, branch_code=None):
    global total_files_modified, total_links_replaced
    
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    count_in_file = 0
    
    def replacer(match):
        nonlocal count_in_file
        url = match.group(0)
        
        # Skip question banks / test papers
        if is_test_paper(url):
            return url
        
        # Look for subject code: 5 or 6 digits followed by a hyphen
        cm = re.search(r'/(\d{5,6})-', url)
        if cm:
            code = cm.group(1)
            new_url = get_preview_url(code, branch_code)
            if new_url:
                count_in_file += 1
                return new_url
        return url

    # Match all bharatividyapeeth URLs
    new_content = re.sub(r'https?://[^\x22\x27\s<>,;]+bharatividyapeeth[^\x22\x27\s<>,;]*\.pdf', replacer, content)
    
    if count_in_file > 0 and new_content != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        total_files_modified += 1
        total_links_replaced += count_in_file
        return count_in_file
    return 0

# 1. Update Branch Semester pages: Branches/*-Semester-*.html
print("\n--- Processing Branch Semester pages ---")
for fpath in glob.glob("Branches/*-Semester-*.html"):
    fname = os.path.basename(fpath).lower()
    branch_slug = fname.split('-semester-')[0]
    b_code = BRANCH_SLUG_MAP.get(branch_slug)
    n = replace_in_file(fpath, b_code)
    if n > 0:
        print(f"Updated {fpath}: {n} links replaced (Branch: {b_code})")

# 2. Update Subject Guide pages: Branches/[0-9]*.html and Branches/elective-*.html
print("\n--- Processing Subject Guide pages in Branches/ ---")
for fpath in glob.glob("Branches/[0-9]*.html") + glob.glob("Branches/elective-*.html"):
    n = replace_in_file(fpath)
    if n > 0:
        print(f"Updated {fpath}: {n} links replaced")

# 3. Update Branches/msbte_k_scheme_syllabus.csv
print("\n--- Processing Branches/msbte_k_scheme_syllabus.csv ---")
if os.path.exists("Branches/msbte_k_scheme_syllabus.csv"):
    rows = []
    replaced_csv = 0
    with open("Branches/msbte_k_scheme_syllabus.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows.append(header)
        for r in reader:
            if len(r) >= 4:
                branch, sem, subj, pdf_url = r[0], r[1], r[2], r[3]
                m = re.search(r'^(\d{5,6})-', subj.strip())
                if m:
                    code = m.group(1)
                    new_url = get_preview_url(code)
                    if new_url:
                        pdf_url = new_url
                        replaced_csv += 1
                rows.append([branch, sem, subj, pdf_url])
            else:
                rows.append(r)
    with open("Branches/msbte_k_scheme_syllabus.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print(f"Updated Branches/msbte_k_scheme_syllabus.csv: {replaced_csv} links replaced")
    total_files_modified += 1
    total_links_replaced += replaced_csv

# 4. Update data/msbte_k_scheme_subjects.csv
print("\n--- Processing data/msbte_k_scheme_subjects.csv ---")
if os.path.exists("data/msbte_k_scheme_subjects.csv"):
    rows = []
    replaced_csv2 = 0
    with open("data/msbte_k_scheme_subjects.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows.append(header)
        for r in reader:
            if len(r) >= 5:
                branch, sem, code, name, pdf_link = r[0], r[1], r[2].strip(), r[3], r[4]
                if code in code_map:
                    pdf_link = get_preview_url(code)
                    replaced_csv2 += 1
                rows.append([branch, sem, code, name, pdf_link])
            else:
                rows.append(r)
    with open("data/msbte_k_scheme_subjects.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print(f"Updated data/msbte_k_scheme_subjects.csv: {replaced_csv2} links replaced")
    total_files_modified += 1
    total_links_replaced += replaced_csv2

# 5. Update scheme/Kscheme.json
print("\n--- Processing scheme/Kscheme.json ---")
if os.path.exists("scheme/Kscheme.json"):
    try:
        with open("scheme/Kscheme.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        replaced_json_box = [0]
        
        def update_json_links(obj):
            if isinstance(obj, dict):
                code = obj.get("subject_code", "")
                link = obj.get("link", "")
                if code and "bharatividyapeeth" in link:
                    new_url = get_preview_url(code)
                    if new_url:
                        obj["link"] = new_url
                        replaced_json_box[0] += 1
                for v in obj.values():
                    update_json_links(v)
            elif isinstance(obj, list):
                for item in obj:
                    update_json_links(item)
                    
        update_json_links(data)
        with open("scheme/Kscheme.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"Updated scheme/Kscheme.json: {replaced_json_box[0]} links replaced")
        total_files_modified += 1
        total_links_replaced += replaced_json_box[0]
    except Exception as e:
        print(f"Error updating scheme/Kscheme.json: {e}")

# 6. Update pyq, model-answer, Notes subject hub blocks
print("\n--- Processing pyq, model-answer, Notes ---")
for folder in ["pyq", "model-answer", "Notes"]:
    for fpath in glob.glob(f"{folder}/**/*.html", recursive=True):
        replace_in_file(fpath)

print(f"\n==========================================")
print(f"DONE! Total files modified: {total_files_modified}")
print(f"Total links replaced: {total_links_replaced}")
print(f"==========================================")
