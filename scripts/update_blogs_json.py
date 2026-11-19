import json

with open('blogs.json', 'r', encoding='utf-8') as f:
    blogs = json.load(f)

for b in blogs:
    # Update K-scheme guide
    if b.get('id') == 'msbte-notes-k-scheme-2025-26':
        b['title'] = 'MSBTE K-Scheme Notes 2026-27: All Branches, Free PDF'
        b['shortTitle'] = 'MSBTE K-Scheme Notes 2026-27'
        b['description'] = 'Branch-wise MSBTE K-Scheme notes, syllabus, lab manuals and question banks for Computer, IT, Civil, Mechanical, Electrical and E&TC. Free PDF download.'
    
    # Update URLs in blogs.json to clean lowercase without .html
    url = b.get('url', '')
    if url:
        url = url.replace('/Blog/', '/blog/')
        if url.endswith('.html'):
            url = url[:-5]
        b['url'] = url

with open('blogs.json', 'w', encoding='utf-8') as f:
    json.dump(blogs, f, indent=2, ensure_ascii=False)

print("Updated blogs.json with clean URLs and K-Scheme 2026-27 guide info.")
