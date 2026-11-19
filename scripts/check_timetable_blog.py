with open('Blog/msbte-winter-2026-exam-timetable-final.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("og:image:", re.findall(r'<meta property="og:image" content="(.*?)"', text))
print("twitter:image:", re.findall(r'<meta name="twitter:image" content="(.*?)"', text))
print("img tags:", re.findall(r'<img[^>]+src="([^">]+)"', text)[:5])
