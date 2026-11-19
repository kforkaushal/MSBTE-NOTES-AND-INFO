import re

check_files = [
    'scheme/i-scheme.html',
    'scheme/k-scheme.html',
    'internships.html',
    'pyq/316308-design-of-rcc-and-steel-structures.html',
    'pyq/314323-utilization-of-electrical-energy.html',
    'model-answer/315326-data-analytics.html'
]

for fpath in check_files:
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        canon = re.findall(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', content)
        print(f"{fpath} -> canonical: {canon}")
    except Exception as e:
        print(f"{fpath} -> Error: {e}")
