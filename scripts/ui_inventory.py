#!/usr/bin/env python3
"""Snapshot everything that must survive a UI-only redesign, then diff two snapshots.

  python3 scripts/ui_inventory.py snap  notes/index.html  before.json
  python3 scripts/ui_inventory.py snap  notes/index.html  after.json
  python3 scripts/ui_inventory.py diff  before.json       after.json

Exit code 0 = nothing lost. Exit code 1 = something was removed or changed.
Additions (new classes, new CSS link, new wrapper divs) are allowed and only reported.
"""
import hashlib, json, re, sys
from collections import Counter

def norm(s):
    return re.sub(r"\s+", " ", s).strip()

def snap(path):
    html = open(path, encoding="utf-8").read()
    head = re.search(r"<head[^>]*>(.*?)</head>", html, re.S | re.I)
    head = head.group(1) if head else ""
    body = html[html.lower().find("<body"):]

    ld = [hashlib.sha1(norm(m).encode()).hexdigest()
          for m in re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', html, re.S | re.I)]
    metas = sorted(norm(m) for m in re.findall(r"<meta\b[^>]*>", head, re.I))
    links = sorted(norm(m) for m in re.findall(r"<link\b[^>]*>", head, re.I))
    titles = [norm(t) for t in re.findall(r"<title>(.*?)</title>", head, re.S | re.I)]
    scripts = sorted(norm(m) for m in re.findall(r"<script\b[^>]*\bsrc=[^>]*>", html, re.I))
    inline_js = sorted(hashlib.sha1(norm(m).encode()).hexdigest()
                       for m in re.findall(r"<script(?![^>]*\bsrc=)(?![^>]*ld\+json)[^>]*>(.*?)</script>", html, re.S | re.I))

    def tag_text(tag):  # visible text of headings, for "no copy lost"
        return [norm(re.sub(r"<[^>]+>", " ", t)) for t in re.findall(rf"<{tag}\b[^>]*>(.*?)</{tag}>", body, re.S | re.I)]

    return {
        "title": titles,
        "meta": metas,
        "head_links": links,
        "json_ld_hashes": ld,
        "script_src": scripts,
        "inline_script_hashes": inline_js,
        "ids": sorted(re.findall(r'\bid="([^"]+)"', body)),
        "data_attrs": sorted(re.findall(r'\b(data-[a-z0-9-]+="[^"]*")', body, re.I)),
        "hrefs": sorted(re.findall(r'\bhref="([^"]+)"', body)),
        "img_src_alt": sorted(re.findall(r'<img\b[^>]*?\bsrc="([^"]+)"[^>]*?\balt="([^"]*)"', body, re.I)),
        "onclick": sorted(re.findall(r'\bonclick="([^"]+)"', body)),
        "aria": sorted(re.findall(r'\b(aria-[a-z]+="[^"]*"|role="[^"]*")', body)),
        "h1": tag_text("h1"), "h2": tag_text("h2"), "h3": tag_text("h3"),
    }

def diff(a, b):
    bad = False
    for k in a:
        ca, cb = Counter(map(str, a[k])), Counter(map(str, b[k]))
        lost, added = ca - cb, cb - ca
        if lost:
            bad = True
            print(f"[LOST] {k}: {sum(lost.values())}")
            for x in list(lost)[:15]:
                print("   -", x[:160])
        if added:
            print(f"[added] {k}: {sum(added.values())}")
    print("RESULT:", "FAIL - something was removed or changed" if bad else "OK - nothing lost")
    return 1 if bad else 0

if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "snap":
        json.dump(snap(sys.argv[2]), open(sys.argv[3], "w"), indent=1)
        print("saved", sys.argv[3])
    elif len(sys.argv) == 4 and sys.argv[1] == "diff":
        sys.exit(diff(json.load(open(sys.argv[2])), json.load(open(sys.argv[3]))))
    else:
        print(__doc__)
