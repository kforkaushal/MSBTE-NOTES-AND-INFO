import urllib.request
import re

urls = [
    'https://msbtenotes-info.netlify.app/scheme/i-scheme',
    'https://msbtenotes-info.netlify.app/internships',
    'https://msbtenotes-info.netlify.app/pyq/316308-design-of-rcc-and-steel-structures',
    'https://msbtenotes-info.netlify.app/model-answer/315326-data-analytics',
    'https://msbtenotes-info.netlify.app/blog/dpharm-exit-exam-cancelled-2026'
]

for url in urls:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1)'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            canons = re.findall(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', content)
            print(f"{url} -> Live Canonical: {canons}")
    except Exception as e:
        print(f"{url} -> Error: {e}")
