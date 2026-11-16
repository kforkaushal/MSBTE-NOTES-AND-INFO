import json
from collections import defaultdict

with open('Notes/resources.json', 'r', encoding='utf-8') as f:
    resources = json.load(f)

print(f"Original resources count: {len(resources)}")

# Define the 13 consolidated entries for the duplicate URLs:
consolidated = {
    "/Notes/311303-communication-skills-english.html": {
        "title": "Communication Skills (English) (311303) — Comprehensive Notes, Grammar Guide & Question Bank",
        "description": "Download complete MSBTE K-Scheme Communication Skills (English) handwritten notes, applied grammar guide, business letter writing, unit 1-4 summaries, question bank, and lab manual.",
        "url": "/Notes/311303-communication-skills-english.html",
        "thumbnail": "/resourse/note-thumbs/311303-communication-skills-english.png",
        "category": "notes",
        "tags": ["Communication Skills", "English", "311303", "K-Scheme", "Semester 1", "Grammar", "Handwritten", "Lab Manual", "Question Bank"],
        "dateAdded": "2026-11-16",
        "code": "311303",
        "shortCode": "ENG",
        "semester": 1,
        "year": 1,
        "branches": ["COMMON", "CO", "IF", "AN", "ME", "CE", "EE", "EJ"]
    },
    "/Notes/312301-applied-mathematics.html": {
        "title": "Applied Mathematics (312301) — Calculus, Differential Equations & Question Bank",
        "description": "Download complete MSBTE K-Scheme Applied Mathematics (312301) calculus notes, differential equations formulas, solved question papers, and question bank.",
        "url": "/Notes/312301-applied-mathematics.html",
        "thumbnail": "/resourse/note-thumbs/312301-applied-mathematics.png",
        "category": "notes",
        "tags": ["Applied Mathematics", "Maths 2", "312301", "K-Scheme", "Semester 2", "Calculus", "Differential Equations", "Question Bank"],
        "dateAdded": "2026-11-16",
        "code": "312301",
        "shortCode": "M2",
        "semester": 2,
        "year": 1,
        "branches": ["COMMON", "CO", "IF", "AN", "ME", "CE", "EE", "EJ"]
    },
    "/Notes/312302-basic-electrical-and-electronics-engineering.html": {
        "title": "Basic Electrical & Electronics Engineering (312302) — Comprehensive Notes & Lab Manual",
        "description": "Download MSBTE K-Scheme Basic Electrical and Electronics Engineering (312302) core study notes, AC/DC circuits, semiconductor diodes, question bank, and lab manual.",
        "url": "/Notes/312302-basic-electrical-and-electronics-engineering.html",
        "thumbnail": "/resourse/note-thumbs/312302-basic-electrical-and-electronics-engineering.png",
        "category": "notes",
        "tags": ["BEEE", "Electrical", "Electronics", "312302", "K-Scheme", "Semester 2", "Lab Manual", "Question Bank"],
        "dateAdded": "2026-11-16",
        "code": "312302",
        "shortCode": "BEEE",
        "semester": 2,
        "year": 1,
        "branches": ["CO", "IF", "AN"]
    },
    "/Notes/312303-programming-in-c.html": {
        "title": "Programming in C (312303) — Complete Notes, Code Examples & Lab Manual",
        "description": "Download MSBTE K-Scheme Programming in C (312303) complete notes, control structures, arrays, pointers, functions, solved question bank, and practical lab manual.",
        "url": "/Notes/312303-programming-in-c.html",
        "thumbnail": "/resourse/note-thumbs/312303-programming-in-c.png",
        "category": "notes",
        "tags": ["Programming in C", "C Language", "PCI", "312303", "K-Scheme", "Semester 2", "Code Examples", "Lab Manual"],
        "dateAdded": "2026-11-16",
        "code": "312303",
        "shortCode": "PCI",
        "semester": 2,
        "year": 1,
        "branches": ["CO", "IF", "AN"]
    },
    "/Notes/312316-electronic-materials-and-components.html": {
        "title": "Electronic Materials and Components (312316) — Notes, Question Bank & Lab Manual",
        "description": "Download MSBTE K-Scheme Electronic Materials and Components (312316) complete notes, magnetic materials, dielectric materials, question bank, and lab manual.",
        "url": "/Notes/312316-electronic-materials-and-components.html",
        "thumbnail": "/resourse/note-thumbs/312316-electronic-materials-and-components.png",
        "category": "notes",
        "tags": ["Electronic Materials", "EMC", "312316", "K-Scheme", "Semester 2", "Lab Manual", "Question Bank"],
        "dateAdded": "2026-11-16",
        "code": "312316",
        "shortCode": "EMC",
        "semester": 2,
        "year": 1,
        "branches": ["EJ", "IE"]
    },
    "/Notes/312314-basic-electronics.html": {
        "title": "Basic Electronics (312314) — Complete Notes, Question Bank & Lab Manual",
        "description": "Download MSBTE K-Scheme Basic Electronics (312314) complete notes, PN junction diodes, rectifiers, transistors, question bank, and practical lab manual.",
        "url": "/Notes/312314-basic-electronics.html",
        "thumbnail": "/resourse/note-thumbs/312314-basic-electronics.png",
        "category": "notes",
        "tags": ["Basic Electronics", "BEL", "312314", "K-Scheme", "Semester 2", "Diodes", "Transistors", "Lab Manual"],
        "dateAdded": "2026-11-16",
        "code": "312314",
        "shortCode": "BEL",
        "semester": 2,
        "year": 1,
        "branches": ["EJ", "IE"]
    },
    "/Notes/312315-elements-of-electrical-engineering.html": {
        "title": "Elements of Electrical Engineering (312315) — Comprehensive Notes & Lab Manual",
        "description": "Download MSBTE K-Scheme Elements of Electrical Engineering (312315) reference e-book, core study notes, transformers, motors, question bank, and lab manual.",
        "url": "/Notes/312315-elements-of-electrical-engineering.html",
        "thumbnail": "/resourse/note-thumbs/312315-elements-of-electrical-engineering.png",
        "category": "notes",
        "tags": ["Elements of Electrical Engineering", "EEE", "312315", "K-Scheme", "Semester 2", "Transformers", "Lab Manual"],
        "dateAdded": "2026-11-16",
        "code": "312315",
        "shortCode": "EEE",
        "semester": 2,
        "year": 1,
        "branches": ["EJ", "IE"]
    },
    "/Notes/311305-basic-science.html": {
        "title": "Basic Science (Physics & Chemistry) (311305) — Complete Notes & Lab Manuals",
        "description": "Download MSBTE K-Scheme Basic Science (311305) complete notes for Physics (Units, SHM, Optics) and Chemistry (Metals, Corrosion, Water Treatment) with practical lab manuals.",
        "url": "/Notes/311305-basic-science.html",
        "thumbnail": "/resourse/note-thumbs/311305-basic-science.png",
        "category": "notes",
        "tags": ["Basic Science", "Physics", "Chemistry", "311305", "K-Scheme", "Semester 1", "Lab Manual", "Question Bank"],
        "dateAdded": "2026-11-16",
        "code": "311305",
        "shortCode": "BSC",
        "semester": 1,
        "year": 1,
        "branches": ["COMMON", "CO", "IF", "AN", "ME", "CE", "EE", "EJ"]
    },
    "/Notes/312308-applied-science.html": {
        "title": "Applied Science (Physics & Chemistry) (312308) — Complete Notes & Lab Manuals",
        "description": "Download MSBTE K-Scheme Applied Science (312308) complete study notes for Applied Physics and Applied Chemistry, solved previous year papers, and practical lab manuals.",
        "url": "/Notes/312308-applied-science.html",
        "thumbnail": "/resourse/note-thumbs/312308-applied-science.png",
        "category": "notes",
        "tags": ["Applied Science", "Physics", "Chemistry", "312308", "K-Scheme", "Semester 2", "Lab Manual", "Solved Papers"],
        "dateAdded": "2026-11-16",
        "code": "312308",
        "shortCode": "ASC",
        "semester": 2,
        "year": 1,
        "branches": ["ME", "CE", "EE"]
    },
    "/Notes/312310-fundamental-of-electrical-engineering.html": {
        "title": "Fundamental of Electrical Engineering (312310) — Complete Units, Revision Notes & Lab Manual",
        "description": "Download MSBTE K-Scheme Fundamental of Electrical Engineering (312310) complete unit notes (DC circuits, magnetic circuits), short revision notes in English & Hindi, and lab manual.",
        "url": "/Notes/312310-fundamental-of-electrical-engineering.html",
        "thumbnail": "/resourse/note-thumbs/312310-fundamental-of-electrical-engineering.png",
        "category": "notes",
        "tags": ["Fundamental of Electrical Engineering", "FEE", "312310", "K-Scheme", "Semester 2", "DC Circuits", "Revision Notes", "Lab Manual"],
        "dateAdded": "2026-11-16",
        "code": "312310",
        "shortCode": "FEE",
        "semester": 2,
        "year": 1,
        "branches": ["EE"]
    },
    "/Notes/312312-engineering-mechanics.html": {
        "title": "Engineering Mechanics (312312) — Handwritten Notes, Solved Papers & Lab Manual",
        "description": "Download MSBTE K-Scheme Engineering Mechanics (312312) complete handwritten notes, equilibrium, friction, centroids, solved previous year papers, and practical lab manual.",
        "url": "/Notes/312312-engineering-mechanics.html",
        "thumbnail": "/resourse/note-thumbs/312312-engineering-mechanics.png",
        "category": "notes",
        "tags": ["Engineering Mechanics", "Mechanics", "312312", "K-Scheme", "Semester 2", "Handwritten", "Solved Papers", "Lab Manual"],
        "dateAdded": "2026-11-16",
        "code": "312312",
        "shortCode": "EMS",
        "semester": 2,
        "year": 1,
        "branches": ["ME", "CE"]
    },
    "/Notes/312338-building-material-and-construction.html": {
        "title": "Building Material and Construction (312338) — Complete Notes & Lab Manual",
        "description": "Download MSBTE K-Scheme Building Material and Construction (312338) notes on stones, bricks, cement, concrete, building construction, and lab manual.",
        "url": "/Notes/312338-building-material-and-construction.html",
        "thumbnail": "/resourse/note-thumbs/312338-building-material-and-construction.png",
        "category": "notes",
        "tags": ["Building Material", "Construction", "BMC", "312338", "K-Scheme", "Semester 2", "Civil Engineering", "Lab Manual"],
        "dateAdded": "2026-11-16",
        "code": "312338",
        "shortCode": "BMC",
        "semester": 2,
        "year": 1,
        "branches": ["CE"]
    },
    "/Notes/312339-surveying.html": {
        "title": "Surveying (312339) — Comprehensive Notes & Lab Manual",
        "description": "Download MSBTE K-Scheme Surveying (312339) chain, compass, leveling notes, measurement guides, and practical lab manual.",
        "url": "/Notes/312339-surveying.html",
        "thumbnail": "/resourse/note-thumbs/312339-surveying.png",
        "category": "notes",
        "tags": ["Surveying", "SUR", "312339", "K-Scheme", "Semester 2", "Civil Engineering", "Leveling", "Lab Manual"],
        "dateAdded": "2026-11-16",
        "code": "312339",
        "shortCode": "SUR",
        "semester": 2,
        "year": 1,
        "branches": ["CE"]
    }
}

# Distinct Workshop entries
workshop_updates = {
    "/Notes/311002-engineering-workshop-practice.html": {
        "title": "Computer Engineering Workshop Practice (311002) — Official Curriculum & Lab Guide",
        "description": "Download MSBTE K-Scheme Computer Engineering Workshop Practice (311002) official curriculum, PC assembly guide, network cabling, and OS setup notes.",
        "url": "/Notes/311002-engineering-workshop-practice.html",
        "thumbnail": "/resourse/note-thumbs/311002-engineering-workshop-practice.png",
        "category": "notes",
        "tags": ["Engineering Workshop", "Computer Workshop", "311002", "K-Scheme", "Semester 1", "PC Assembly", "Networking"],
        "dateAdded": "2026-11-16",
        "code": "311002",
        "shortCode": "EWP-CO",
        "semester": 1,
        "year": 1,
        "branches": ["CO", "IF", "AN"]
    },
    "/Notes/311005-engineering-workshop-practice.html": {
        "title": "Engineering Workshop Practice (311005) — Practical Workshop Guide (Fitting, Carpentry, Welding)",
        "description": "Download MSBTE K-Scheme Engineering Workshop Practice (311005) practical project guide, fitting, welding, carpentry, sheet metal jobs, and official syllabus.",
        "url": "/Notes/311005-engineering-workshop-practice.html",
        "thumbnail": "/resourse/note-thumbs/311005-engineering-workshop-practice.png",
        "category": "notes",
        "tags": ["Engineering Workshop", "Workshop Practice", "311005", "K-Scheme", "Semester 1", "Fitting", "Welding", "Carpentry"],
        "dateAdded": "2026-11-16",
        "code": "311005",
        "shortCode": "EWP-ME",
        "semester": 1,
        "year": 1,
        "branches": ["ME", "EE"]
    },
    "/Notes/311007-engineering-workshop-practice.html": {
        "title": "Electronics Engineering Workshop Practice (311007) — Soldering, PCB & Circuit Guide",
        "description": "Download MSBTE K-Scheme Electronics Workshop Practice (311007) practical guide, PCB soldering, electronic component testing, and breadboard prototyping.",
        "url": "/Notes/311007-engineering-workshop-practice.html",
        "thumbnail": "/resourse/note-thumbs/311007-engineering-workshop-practice.png",
        "category": "notes",
        "tags": ["Engineering Workshop", "Electronics Workshop", "311007", "K-Scheme", "Semester 1", "Soldering", "PCB", "Components"],
        "dateAdded": "2026-11-16",
        "code": "311007",
        "shortCode": "EWP-EJ",
        "semester": 1,
        "year": 1,
        "branches": ["EJ", "IE"]
    },
    "/Notes/311010-civil-engineering-workshop.html": {
        "title": "Civil Engineering Workshop (311010) — Masonry, Plumbing & Construction Guide",
        "description": "Download MSBTE K-Scheme Civil Engineering Workshop (311010) practical guide, brick masonry bonds, plumbing joints, bar bending, and site safety.",
        "url": "/Notes/311010-civil-engineering-workshop.html",
        "thumbnail": "/resourse/note-thumbs/311010-civil-engineering-workshop.png",
        "category": "notes",
        "tags": ["Civil Workshop", "311010", "K-Scheme", "Semester 1", "Masonry", "Plumbing", "Bar Bending", "Construction"],
        "dateAdded": "2026-11-16",
        "code": "311010",
        "shortCode": "CEW",
        "semester": 1,
        "year": 1,
        "branches": ["CE"]
    }
}

new_resources = []
seen_urls = set()

for item in resources:
    url = item.get('url', '').strip()
    
    if url in consolidated:
        if url not in seen_urls:
            new_resources.append(consolidated[url])
            seen_urls.add(url)
    elif url in workshop_updates:
        if url not in seen_urls:
            new_resources.append(workshop_updates[url])
            seen_urls.add(url)
    else:
        if url and url in seen_urls:
            print(f"Skipping unexpected duplicate: {url} -> {item.get('title')}")
            continue
        if url:
            seen_urls.add(url)
        new_resources.append(item)

print(f"Cleaned resources count: {len(new_resources)}")

# Check duplicate URLs again
url_counts = defaultdict(int)
for item in new_resources:
    u = item.get('url', '').strip()
    if u:
        url_counts[u] += 1

dups = {u: cnt for u, cnt in url_counts.items() if cnt > 1}
print(f"Remaining duplicate URLs: {len(dups)}")
if dups:
    print(dups)
else:
    # Save back to Notes/resources.json
    with open('Notes/resources.json', 'w', encoding='utf-8') as f:
        json.dump(new_resources, f, indent=2, ensure_ascii=False)
    print("Successfully updated Notes/resources.json with zero duplicates!")
