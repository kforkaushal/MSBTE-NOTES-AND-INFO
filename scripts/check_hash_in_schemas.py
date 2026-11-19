import os
import re

folders = ['Blog', 'Branches', 'CollegeInfo', 'Courses', 'Jobs', 'mock-tests', 'model-answer', 'News', 'Notes', 'pyq', 'scheme', 'video-course']
schemas_found = set()

for folder in folders:
    if os.path.exists(folder):
        for root, _, filenames in os.walk(folder):
            for f in filenames:
                if f.endswith('.html'):
                    p = os.path.join(root, f)
                    with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                        content = fp.read()
                        for m in re.finditer(r'"item":\s*"([^"]+)"', content):
                            url = m.group(1)
                            if '#' in url:
                                schemas_found.add(url)

print("Schema URLs with hash:")
for u in sorted(schemas_found):
    print(" ", u)
