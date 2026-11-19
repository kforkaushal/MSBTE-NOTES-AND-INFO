import os
import re

branches = [
    'Branches/Computer.html',
    'Branches/Computer-Semester-1.html',
    'Branches/Information-Technology.html',
    'Branches/Information-Technology-Semester-1.html',
    'Branches/AI-ML.html',
    'Branches/AI-ML-Semester-1.html',
    'Branches/Civil.html',
    'Branches/Civil-Semester-1.html',
    'Branches/Electrical-Engineering.html',
    'Branches/Electrical-Engineering-Semester-1.html',
    'Branches/ETC-Engineering.html',
    'Branches/ETC-Engineering-Semester-1.html',
    'Branches/Mechanical-Engineering.html',
    'Branches/Mechanical-Engineering-Semester-1.html'
]

for b in branches:
    with open(b, 'r', encoding='utf-8') as f:
        content = f.read()
    m = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', content)
    print(f"{b} -> Canonical: {m.group(1) if m else 'None'}")
