import os
import re

branches_dir = 'Branches'
files = [f for f in os.listdir(branches_dir) if f.endswith('.html')]
print(f"Total HTML files in Branches: {len(files)}")

canon_issues = []
for f in files:
    path = os.path.join(branches_dir, f)
    with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
        content = fp.read()
    m = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', content)
    if m:
        c = m.group(1)
        if c.endswith('.html') or any(cap in c for cap in ['/Branches/', '/Computer', '/Semester']):
            canon_issues.append((f, c))
    else:
        canon_issues.append((f, "NO CANONICAL"))

print(f"Branches canonical issues: {len(canon_issues)}")
for f, c in canon_issues[:15]:
    print(f"  {f} -> {c}")
