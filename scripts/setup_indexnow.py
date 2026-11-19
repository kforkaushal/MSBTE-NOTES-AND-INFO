import uuid
import os
import glob
import re
import json

# Generate a consistent, clean 32-char hex IndexNow key
# Let's generate a dedicated key
key = "90f0981b055f4fb49ee8bf6b73c20543" # Matches conversation ID hex without hyphens!
key_filename = f"{key}.txt"

with open(key_filename, 'w', encoding='utf-8') as f:
    f.write(key)

print(f"Created IndexNow verification key file: {key_filename}")

# Gather all 602 URLs from the split sitemaps
sitemap_files = glob.glob('sitemap-*.xml')
all_urls = set()

for sm in sitemap_files:
    with open(sm, 'r', encoding='utf-8') as f:
        content = f.read()
    locs = re.findall(r'<loc>(.*?)</loc>', content)
    for loc in locs:
        all_urls.add(loc.strip())

sorted_urls = sorted(list(all_urls))
print(f"Collected {len(sorted_urls)} URLs for IndexNow submission.")

payload = {
    "host": "msbtenotes-info.netlify.app",
    "key": key,
    "keyLocation": f"https://msbtenotes-info.netlify.app/{key_filename}",
    "urlList": sorted_urls
}

with open('scripts/indexnow_payload.json', 'w', encoding='utf-8') as f:
    json.dump(payload, f, indent=2)

print("Saved scripts/indexnow_payload.json")
