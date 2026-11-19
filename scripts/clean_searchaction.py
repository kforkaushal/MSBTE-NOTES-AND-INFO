import re

# 1. In index.html
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the first WebSite schema with potentialAction
pattern1 = r'<script type="application/ld\+json">\s*\{\s*"@context":\s*"https://schema\.org",\s*"@type":\s*"WebSite",\s*"name":\s*"MSBTE Notes & Info",\s*"url":\s*"https://msbtenotes-info\.netlify\.app/",\s*"potentialAction":\s*\{.*?"query-input":\s*"required name=search_term_string"\s*\}\s*\}\s*</script>'
text = re.sub(pattern1, '', text, flags=re.DOTALL)

# Replace the second WebSite schema to remove potentialAction
pattern2 = r'"potentialAction":\s*\{\s*"@type":\s*"SearchAction",\s*"target":\s*\{\s*"@type":\s*"EntryPoint",\s*"urlTemplate":\s*"https://msbtenotes-info\.netlify\.app\?search=\{search_term_string\}"\s*\},\s*"query-input":\s*"required name=search_term_string"\s*\},\s*'
text = re.sub(pattern2, '', text, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Removed SearchAction from index.html")

# 2. In Notes/index.html
with open('Notes/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pattern3 = r'"potentialAction":\s*\{\s*"@type":\s*"SearchAction",\s*"target":\s*"https://msbtenotes-info\.netlify\.app/notes/\?q=\{search_term_string\}",\s*"query-input":\s*"required name=search_term_string"\s*\}'
# Note that if followed by comma or not
text = re.sub(r',\s*' + pattern3, '', text, flags=re.DOTALL)
text = re.sub(pattern3 + r'\s*,?', '', text, flags=re.DOTALL)

with open('Notes/index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Removed SearchAction from Notes/index.html")
