import os
import re
import csv
from html.parser import HTMLParser

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_DIR = os.path.join(BASE_DIR, "docs", "seo-audit")
BASELINE_DIR = os.path.join(DOCS_DIR, "baseline")

os.makedirs(BASELINE_DIR, exist_ok=True)

REPRESENTATIVE_PAGES = [
    ("home", "index.html"),
    ("notes_index", "Notes/index.html"),
    ("blog_index", "Blog/index.html"),
    ("blog_post_1", "Blog/engineering-admissions-institute-level-round-merit-based-2026.html"),
    ("blog_post_2", "Blog/nana-patekar-tribute.html"),
    ("branch_comp_sem5", "Branches/Computer-Semester-5.html"),
    ("branch_it_sem5", "Branches/Information-Technology-Semester-5.html"),
    ("subject_osy", "Notes/osy-k-scheme-notes.html"),
    ("subject_c_prog", "Notes/312303-programming-in-c.html"),
    ("lab_manual_dte", "Notes/dte-lab-manual.html"),
    ("college_info", "CollegeInfo/index.html"),
    ("sitemap", "sitemap.html")
]

class HTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.ignore_tags = {'script', 'style', 'noscript', 'svg'}
        self.current_ignore = 0

    def handle_starttag(self, tag, attrs):
        if tag.lower() in self.ignore_tags:
            self.current_ignore += 1

    def handle_endtag(self, tag):
        if tag.lower() in self.ignore_tags and self.current_ignore > 0:
            self.current_ignore -= 1

    def handle_data(self, data):
        if self.current_ignore == 0:
            cleaned = data.strip()
            if cleaned:
                self.text_parts.append(cleaned)

    def get_text(self):
        return "\n".join(self.text_parts)

class HTMLLinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag.lower() == 'a' and 'href' in attrs_dict:
            self.links.append(attrs_dict['href'])

print("Extracting visible text for 12 representative pages...")
for slug, rel_path in REPRESENTATIVE_PAGES:
    full_path = os.path.join(BASE_DIR, rel_path.replace("/", os.sep))
    if os.path.exists(full_path):
        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        extractor = HTMLTextExtractor()
        extractor.feed(content)
        text = extractor.get_text()
        out_file = os.path.join(BASELINE_DIR, f"{slug}_text.txt")
        with open(out_file, "w", encoding="utf-8") as out:
            out.write(text)
        print(f"  [OK] {slug} -> {len(text.splitlines())} lines")
    else:
        print(f"  [MISSING] {full_path}")

print("\nExtracting all HTML files in repo...")
all_html_files = []
for root, dirs, files in os.walk(BASE_DIR):
    # skip .git, .venv, node_modules
    if any(p in root for p in [".git", ".venv", "node_modules", ".agents"]):
        continue
    for f in files:
        if f.lower().endswith(".html"):
            rel = os.path.relpath(os.path.join(root, f), BASE_DIR).replace("\\", "/")
            all_html_files.append(rel)

all_html_files.sort()
urls_file = os.path.join(BASELINE_DIR, "urls_inventory.txt")
with open(urls_file, "w", encoding="utf-8") as f:
    f.write(f"Total HTML files found: {len(all_html_files)}\n\n")
    for u in all_html_files:
        f.write(u + "\n")
print(f"Saved {len(all_html_files)} files to urls_inventory.txt")

print("\nExtracting and checking links across representative pages...")
checked_links = []
for slug, rel_path in REPRESENTATIVE_PAGES:
    full_path = os.path.join(BASE_DIR, rel_path.replace("/", os.sep))
    if not os.path.exists(full_path):
        continue
    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    link_extractor = HTMLLinkExtractor()
    link_extractor.feed(content)
    for href in set(link_extractor.links):
        checked_links.append((rel_path, href))

# Analyze internal links
links_csv_file = os.path.join(BASELINE_DIR, "links.csv")
with open(links_csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["SourcePage", "Href", "Type", "Status", "Notes"])
    for source, href in checked_links:
        link_type = "external" if href.startswith("http://") or href.startswith("https://") or href.startswith("//") else "internal"
        if href.startswith("mailto:") or href.startswith("tel:") or href.startswith("javascript:"):
            link_type = "special"
        
        status = "unknown"
        notes = ""
        if link_type == "internal":
            clean_href = href.split("#")[0].split("?")[0]
            if not clean_href:
                status = "anchor-only"
            else:
                # Resolve relative or root-relative path
                if clean_href.startswith("/"):
                    target_rel = clean_href.lstrip("/")
                else:
                    source_dir = os.path.dirname(source)
                    target_rel = os.path.normpath(os.path.join(source_dir, clean_href)).replace("\\", "/")
                
                # Check target file
                target_full = os.path.join(BASE_DIR, target_rel.replace("/", os.sep))
                target_html = target_full + ".html" if not target_full.endswith(".html") else target_full
                target_index = os.path.join(target_full, "index.html")
                
                if os.path.isfile(target_full):
                    status = "200_exact"
                elif os.path.isfile(target_html):
                    status = "200_html_extension"
                elif os.path.isfile(target_index):
                    status = "200_directory_index"
                else:
                    status = "404_potential"
                    notes = f"Target {target_rel} not found"
        elif link_type == "external":
            if href.startswith("http://"):
                notes = "insecure_http"
            status = "external_unverified"
            
        writer.writerow([source, href, link_type, status, notes])

print(f"Saved link audit to links.csv ({len(checked_links)} links analyzed)")
