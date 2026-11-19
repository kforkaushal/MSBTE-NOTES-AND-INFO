import os

patterns = ['â€“', 'â‚¹', 'â€™', 'â€œ', 'â€\x9d', 'Â']
folders = ['Blog', 'Branches', 'CollegeInfo', 'Courses', 'Jobs', 'mock-tests', 'model-answer', 'News', 'Notes', 'pyq', 'scheme', 'video-course']
files_to_check = ['index.html', 'start.html', 'about.html', 'contact.html', 'sitemap.html']

for f in os.listdir('.'):
    if f.endswith('.html') or f.endswith('.json'):
        if f not in files_to_check:
            files_to_check.append(f)

for folder in folders:
    if os.path.exists(folder):
        for root, _, filenames in os.walk(folder):
            for f in filenames:
                if f.endswith('.html') or f.endswith('.json'):
                    files_to_check.append(os.path.join(root, f))

found = {}
for path in files_to_check:
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
            content = fp.read()
            for p in ['â€“', 'â‚¹', 'â€™', 'â€œ', 'Â ']:
                count = content.count(p)
                if count > 0:
                    found.setdefault(path, {})[p] = count
    except Exception as e:
        pass

for p, hits in list(found.items())[:20]:
    print(p, hits)
print('Total files with encoding artifacts:', len(found))
