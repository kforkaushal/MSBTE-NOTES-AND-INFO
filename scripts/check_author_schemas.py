import glob
import re

count = 0
for html in glob.glob('**/*.html', recursive=True):
    with open(html, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    if '"author":' in content:
        count += 1
        m = re.findall(r'"author":\s*(\{[^}]+\}|"[^"]+")', content)
        if count <= 5:
            print(f"{html}: {m}")

print(f"Total files with 'author' in schema: {count}")
