import glob
import re

for html in ['index.html', 'Notes/index.html', 'pyq/index.html', 'model-answer/index.html', 'Blog/index.html']:
    try:
        with open(html, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'SearchAction' in content:
            print(f"Found SearchAction in {html}")
    except Exception as e:
        pass
