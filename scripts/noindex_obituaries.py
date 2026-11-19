import re

files = [
    'Blog/nana-patekar-tribute.html',
    'Blog/asha-bhosle-death-news.html',
    'Blog/ajit-pawar-death-news.html'
]

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '<meta name="robots"' in content:
        content = re.sub(r'<meta name="robots"[^>]*>', '<meta name="robots" content="noindex, follow">', content)
    else:
        # insert right after <head>
        content = re.sub(r'(<head[^>]*>)', r'\1\n    <meta name="robots" content="noindex, follow">', content, count=1)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Added noindex to {file}")
