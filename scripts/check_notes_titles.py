import re

notes_files = [
    'Notes/dbms-k-scheme-notes.html',
    'Notes/dsu-k-scheme-notes.html',
    'Notes/dte-k-scheme-notes.html',
    'Notes/oop-k-scheme-notes.html',
    'Notes/java-k-scheme-notes.html',
    'Notes/dcn-k-scheme-notes.html',
    'Notes/mic-k-scheme-notes.html'
]

for p in notes_files:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    t = re.findall(r'<title>(.*?)</title>', content, re.DOTALL)
    d = re.findall(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', content, re.DOTALL)
    print(f"=== {p} ===")
    print("  TITLE:", t[0].strip() if t else 'None')
    print("  DESC:", d[0].strip()[:90] if d else 'None')
