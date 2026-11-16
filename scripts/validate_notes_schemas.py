import glob
import re
import json

html_files = [
    'Notes/msbte-first-year-diploma-notes.html',
    'Notes/311002-engineering-workshop-practice.html',
    'Notes/311005-engineering-workshop-practice.html',
    'Notes/311007-engineering-workshop-practice.html',
    'Notes/311010-civil-engineering-workshop.html',
    'Notes/index.html'
]

errors = 0
for f in html_files:
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    schemas = re.findall(r'<script\s+type=["\']application/ld\+json["\']\s*>(.*?)</script>', c, re.DOTALL)
    print(f"\nChecking {f} ({len(schemas)} schemas):")
    for i, s in enumerate(schemas):
        try:
            data = json.loads(s.strip())
            t = data.get('@type', 'Unknown')
            print(f"  Schema {i+1} [{t}]: VALID JSON")
        except Exception as e:
            print(f"  Schema {i+1}: INVALID JSON -> {e}")
            errors += 1

print(f"\nTotal schema errors: {errors}")
