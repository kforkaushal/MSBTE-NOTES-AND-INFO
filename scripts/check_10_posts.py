import re

posts = [
    'Blog/msbte-winter-2025-exam-form.html',
    'Blog/mahadbt-scholarship-error-solutions.html',
    'Blog/dpharm-exit-exam-cancelled-2026.html',
    'Blog/dse-admission-schedule-2026.html',
    'Blog/sppu-summer-2026-exam-roadmap.html',
    'Blog/post-matric-scholarship-obc.html',
    'Blog/msbte-summer-2026-exam-roadmap.html',
    'Blog/autonomous-engineering-colleges-maharashtra.html',
    'Blog/msbte-summer-2026-final-timetable-declared-diploma.html',
    'Blog/50-capstone-project-ideas-computer-engineering.html'
]

for p in posts:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    t = re.findall(r'<title>(.*?)</title>', content, re.DOTALL)
    d = re.findall(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', content, re.DOTALL)
    print(f"=== {p} ===")
    print("  TITLE:", t[0].strip() if t else 'None')
    print("  DESC:", d[0].strip()[:90] if d else 'None')
