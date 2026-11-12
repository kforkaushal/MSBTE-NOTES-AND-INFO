#!/usr/bin/env python3
import os
import re
import glob

def check_link(href):
    if href.startswith(('http://', 'https://', '#', 'mailto:', 'tel:')):
        return True
    clean = href.split('?')[0].split('#')[0].strip('/')
    if not clean:
        return True
    if os.path.exists(clean):
        return True
    if os.path.exists(clean + '.html'):
        return True
    if os.path.exists(os.path.join(clean, 'index.html')):
        return True
    return False

def main():
    href_pattern = re.compile(r'href=[\'"]([^\'"]+)[\'"]')
    script_pattern = re.compile(r'<script.*?</script>', re.DOTALL | re.IGNORECASE)
    style_pattern = re.compile(r'<style.*?</style>', re.DOTALL | re.IGNORECASE)

    # 1. Check start.html (DOM only, excluding script contents)
    with open('start.html', 'r', encoding='utf-8') as f:
        content = f.read()

    dom_content = script_pattern.sub('', style_pattern.sub('', content))
    hrefs = href_pattern.findall(dom_content)
    bad_start = [h for h in hrefs if not check_link(h)]
    print(f'Total DOM links in start.html: {len(hrefs)}')
    print(f'Broken DOM links in start.html: {len(bad_start)}')
    if bad_start:
        for b in bad_start:
            print(f'  Bad link in start.html: {b}')

    # 2. Check all subject hub links
    all_html = (
        glob.glob('Branches/*.html') +
        glob.glob('Notes/*.html') +
        glob.glob('pyq/*.html') +
        glob.glob('pyq/*-*/index.html') +
        glob.glob('model-answer/*.html') +
        glob.glob('model-answer/*-*/index.html')
    )

    total_hub_links = 0
    broken_hub_links = 0

    hub_pattern = re.compile(r'<nav[^>]*class=[\'"][^\'"]*subject-hub[^\'"]*[\'"][^>]*>.*?</nav>', re.DOTALL)

    for p in all_html:
        with open(p, 'r', encoding='utf-8') as f:
            c = f.read()
        m = hub_pattern.search(c)
        if m:
            hub_hrefs = href_pattern.findall(m.group(0))
            for h in hub_hrefs:
                total_hub_links += 1
                if not check_link(h):
                    broken_hub_links += 1
                    print(f'Broken hub link in {p}: {h}')

    print(f'Total subject-hub links verified: {total_hub_links}')
    print(f'Broken subject-hub links: {broken_hub_links}')

if __name__ == '__main__':
    main()

