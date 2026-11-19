import os
import re

candidates = [
    # Notes manuals
    'Notes/Manual',
    # Video courses
    'video-course',
    # Courses
    'Courses',
    # Jobs
    'Jobs',
    # News
    'News'
]

for folder in candidates:
    if os.path.exists(folder):
        print(f"\n=== Folder: {folder} ===")
        for f in os.listdir(folder):
            if f.endswith('.html'):
                fpath = os.path.join(folder, f)
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as fp:
                    content = fp.read()
                title = re.findall(r'<title>(.*?)</title>', content)
                canon = re.findall(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', content)
                robots = re.findall(r'<meta\s+name=["\']robots["\'][^>]+>', content)
                print(f"  {f} | Title: {title[0] if title else 'No Title'} | Canonical: {canon[0] if canon else 'No Canon'} | Robots: {robots}")
