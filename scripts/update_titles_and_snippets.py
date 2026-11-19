import re

# 1. Update K-Scheme Guide
with open('Blog/msbte-notes-k-scheme-2025-26.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = re.sub(
    r'<title>.*?</title>',
    '<title>MSBTE K-Scheme Notes 2026-27: All Branches, Free PDF</title>',
    c, flags=re.DOTALL
)
c = re.sub(
    r'<meta\s+name=["\']description["\']\s+content=["\'].*?["\']\s*/?>',
    '<meta name="description" content="Branch-wise MSBTE K-Scheme notes, syllabus, lab manuals and question banks for Computer, IT, Civil, Mechanical, Electrical and E&TC. Free PDF download." />',
    c, flags=re.DOTALL
)
c = re.sub(
    r'<meta\s+property=["\']og:title["\']\s+content=["\'].*?["\']\s*/?>',
    '<meta property="og:title" content="MSBTE K-Scheme Notes 2026-27: All Branches, Free PDF" />',
    c, flags=re.DOTALL
)
c = re.sub(
    r'<meta\s+name=["\']twitter:title["\']\s+content=["\'].*?["\']\s*/?>',
    '<meta name="twitter:title" content="MSBTE K-Scheme Notes 2026-27: All Branches, Free PDF" />',
    c, flags=re.DOTALL
)

with open('Blog/msbte-notes-k-scheme-2025-26.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Updated Blog/msbte-notes-k-scheme-2025-26.html")

# 2. Update 10 High-Impression Posts for CTR Boost
posts_meta = {
    'Blog/msbte-winter-2025-exam-form.html': (
        'MSBTE Winter Exam Form 2026: Last Date, Login Link & Fees',
        'Fill MSBTE Winter diploma exam form online. Direct login link, step-by-step instructions, regular & late fee schedules, and confirmation steps.'
    ),
    'Blog/mahadbt-scholarship-error-solutions.html': (
        'MahaDBT Scholarship Errors: Causes & Step-by-Step Fixes',
        'Fix common MahaDBT scholarship errors: Aadhaar bank seeding failed, applicant already registered, biometric errors and document upload issues.'
    ),
    'Blog/dpharm-exit-exam-cancelled-2026.html': (
        'D.Pharm Exit Exam 2026 Cancelled: Latest Update & Next Steps',
        'PCI officially cancelled the D.Pharm Exit Exam for 2026. Complete notification breakdown, eligibility rules, and PCI registration guidelines.'
    ),
    'Blog/dse-admission-schedule-2026.html': (
        'DSE Admission 2026-27 Maharashtra: Dates, CAP & Documents',
        'Direct Second Year Engineering (DSE) 2026-27 schedule in Maharashtra: CAP round registration dates, merit list, cutoffs and document checklist.'
    ),
    'Blog/sppu-summer-2026-exam-roadmap.html': (
        'SPPU Summer 2026 Exam Roadmap: Study Plan & Timetable',
        'Step-by-step SPPU Summer 2026 exam preparation roadmap: branch-wise scoring strategies, timetable analysis, and scoring 8+ SGPA in end-sem exams.'
    ),
    'Blog/post-matric-scholarship-obc.html': (
        'Post Matric Scholarship for OBC Maharashtra: Eligibility & Apply',
        'Complete guide to Post Matric Scholarship for OBC students in Maharashtra: income limits, fee concession benefits, required documents and MahaDBT portal link.'
    ),
    'Blog/msbte-summer-2026-exam-roadmap.html': (
        'MSBTE Summer 2026 Exam Roadmap: Scoring Guide & Schedule',
        'Comprehensive preparation roadmap for MSBTE Summer 2026 diploma exams: unit-wise planning, passing marks criteria, and K-Scheme scoring tactics.'
    ),
    'Blog/autonomous-engineering-colleges-maharashtra.html': (
        'Autonomous Engineering Colleges in Maharashtra: Top List 2026',
        'Verified list of autonomous engineering colleges in Maharashtra: cutoff trends, autonomous vs SPPU/MSBTE differences, placement data and CAP options.'
    ),
    'Blog/msbte-summer-2026-final-timetable-declared-diploma.html': (
        'MSBTE Summer 2026 Final Timetable Declared: Direct PDF Link',
        'Download official MSBTE Summer 2026 final theory exam timetable PDF for all diploma branches: exam dates, shift slots, and hall ticket schedule.'
    ),
    'Blog/50-capstone-project-ideas-computer-engineering.html': (
        '50 Capstone Project Ideas for Computer Engineering Diploma',
        'Explore 50 unique capstone project ideas for Computer & IT diploma students: AI/ML, IoT, Web, Python, and Android projects with report formats.'
    )
}

for path, (t, d) in posts_meta.items():
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(r'<title>.*?</title>', f'<title>{t}</title>', content, flags=re.DOTALL)
    content = re.sub(r'<meta\s+name=["\']description["\']\s+content=["\'].*?["\']\s*/?>', f'<meta name="description" content="{d}" />', content, flags=re.DOTALL)
    content = re.sub(r'<meta\s+property=["\']og:title["\']\s+content=["\'].*?["\']\s*/?>', f'<meta property="og:title" content="{t}" />', content, flags=re.DOTALL)
    content = re.sub(r'<meta\s+name=["\']twitter:title["\']\s+content=["\'].*?["\']\s*/?>', f'<meta name="twitter:title" content="{t}" />', content, flags=re.DOTALL)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated CTR snippet for {path}")

# 3. Update Subject Notes Titles (P1-1 formula)
notes_meta = {
    'Notes/dbms-k-scheme-notes.html': (
        'DBMS 313302 Database Management System Notes PDF – MSBTE K-Scheme',
        'Free MSBTE K-Scheme Database Management System (DBMS 313302) unit 1-5 notes, IMP question bank and Winter 2023 solved papers for 3rd Sem Computer & IT.'
    ),
    'Notes/dsu-k-scheme-notes.html': (
        'DSU 313301 Data Structures Using C Notes PDF – MSBTE K-Scheme',
        'Free MSBTE K-Scheme Data Structures Using C (DSU 313301) unit-wise notes, algorithms, flowcharts and IMP question bank for 3rd Sem.'
    ),
    'Notes/dte-k-scheme-notes.html': (
        'DTE 313303 Digital Techniques Notes PDF – MSBTE K-Scheme',
        'Free MSBTE K-Scheme Digital Techniques (DTE 313303) unit-wise notes, logic gates, K-Map numericals and IMP question bank for 3rd Sem.'
    ),
    'Notes/oop-k-scheme-notes.html': (
        'OOP 313304 Object Oriented Programming with C++ Notes PDF – MSBTE K-Scheme',
        'Free MSBTE K-Scheme Object Oriented Programming with C++ (OOP 313304) unit 1-5 notes, code samples and solved question papers for 3rd Sem.'
    ),
    'Notes/java-k-scheme-notes.html': (
        'JPR 314317 Java Programming Notes PDF – MSBTE K-Scheme',
        'Free MSBTE K-Scheme Java Programming (JPR 314317) unit 1-6 notes, Super 25 question bank, viva Q&A and solved model answers for 4th Sem.'
    ),
    'Notes/dcn-k-scheme-notes.html': (
        'DCN 314318 Data Communication & Computer Network Notes PDF – MSBTE K-Scheme',
        'Free MSBTE K-Scheme Data Communication & Computer Network (DCN 314318) complete unit-wise notes, OSI reference model guide and IMP questions.'
    ),
    'Notes/mic-k-scheme-notes.html': (
        'MIC 314321 Microprocessor Notes PDF – MSBTE K-Scheme',
        'Free MSBTE K-Scheme Microprocessor (MIC 314321) unit-wise notes, 8086 pin diagrams, instruction sets and IMP question bank for 4th Sem.'
    )
}

for path, (t, d) in notes_meta.items():
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(r'<title>.*?</title>', f'<title>{t}</title>', content, flags=re.DOTALL)
    content = re.sub(r'<meta\s+name=["\']description["\']\s+content=["\'].*?["\']\s*/?>', f'<meta name="description" content="{d}" />', content, flags=re.DOTALL)
    content = re.sub(r'<meta\s+property=["\']og:title["\']\s+content=["\'].*?["\']\s*/?>', f'<meta property="og:title" content="{t}" />', content, flags=re.DOTALL)
    content = re.sub(r'<meta\s+name=["\']twitter:title["\']\s+content=["\'].*?["\']\s*/?>', f'<meta name="twitter:title" content="{t}" />', content, flags=re.DOTALL)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated Subject Notes formula for {path}")
