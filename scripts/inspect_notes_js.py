with open('Notes/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = re.findall(r'<script.*?</script>', content, re.DOTALL)
print(f"Total script blocks in Notes/index.html: {len(matches)}")
for idx, m in enumerate(matches):
    if 'searchInput' in m or 'search' in m.lower():
        print(f"Script block {idx}:\n{m[:300]}...\n")
