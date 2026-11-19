import os
import re

vc_dir = 'video-course'
for f in os.listdir(vc_dir):
    if f.endswith('.html') and f != 'topic-template.html':
        fpath = os.path.join(vc_dir, f)
        with open(fpath, 'r', encoding='utf-8') as fp:
            content = fp.read()
        
        slug = f[:-5].lower()
        if f == 'index.html':
            canon_url = 'https://msbtenotes-info.netlify.app/video-course/'
        else:
            canon_url = f'https://msbtenotes-info.netlify.app/video-course/{slug}'
        
        if '<link rel="canonical"' in content:
            content = re.sub(r'<link\s+rel=["\']canonical["\'][^>]+>', f'<link rel="canonical" href="{canon_url}" />', content)
        else:
            content = re.sub(r'(<head[^>]*>)', rf'\1\n    <link rel="canonical" href="{canon_url}" />', content, count=1)
        
        with open(fpath, 'w', encoding='utf-8') as fp:
            fp.write(content)
        print(f"Added canonical to {fpath} -> {canon_url}")
