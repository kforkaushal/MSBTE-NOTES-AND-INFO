import os
import re

man_dir = 'Notes/Manual'
for f in os.listdir(man_dir):
    if f.endswith('.html') and f != 'manual-blank.html':
        fpath = os.path.join(man_dir, f)
        with open(fpath, 'r', encoding='utf-8') as fp:
            content = fp.read()
        
        slug = f[:-5].lower()
        canon_url = f'https://msbtenotes-info.netlify.app/notes/manual/{slug}'
        
        if '<link rel="canonical"' in content:
            content = re.sub(r'<link\s+rel=["\']canonical["\'][^>]+>', f'<link rel="canonical" href="{canon_url}" />', content)
        else:
            content = re.sub(r'(<head[^>]*>)', rf'\1\n    <link rel="canonical" href="{canon_url}" />', content, count=1)
        
        with open(fpath, 'w', encoding='utf-8') as fp:
            fp.write(content)
        print(f"Verified canonical for {fpath} -> {canon_url}")
