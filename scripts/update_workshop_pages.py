import re

# 1. Update 311002 (Computer / IT / AI-ML)
with open('Notes/311002-engineering-workshop-practice.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace svg with png in banner
c = c.replace('/resourse/note-thumbs/311002-engineering-workshop-practice.svg', '/resourse/note-thumbs/311002-engineering-workshop-practice.png')
# Replace iframe preview
c = c.replace('12aPpjYpevgMMeQM4ZTs6zNxt4J-iMCL2/preview', '1KsfLwAkqV5QBX6rUV29EwacXFAtqgP7C/preview')
# Replace title and intro
c = c.replace(
    '<title>MSBTE 311002 Engineering Workshop Practice Notes & Study Material (K-Scheme)</title>',
    '<title>MSBTE 311002 Computer Engineering Workshop Practice Notes & Syllabus (K-Scheme)</title>'
)
c = c.replace(
    '<h1 class="text-3xl sm:text-4xl font-bold text-gray-900 font-display leading-tight">\n            Engineering Workshop Practice (311002) â€” MSBTE Notes &amp; Study Material\n        </h1>',
    '<h1 class="text-3xl sm:text-4xl font-bold text-gray-900 font-display leading-tight">\n            Computer Engineering Workshop Practice (311002) — MSBTE Notes &amp; Curriculum\n        </h1>'
)

# Replace download cards section
old_downloads = re.search(r'<section class="my-10" id="downloads">.*?</section>', c, re.DOTALL)
new_downloads = """<section class="my-10" id="downloads">
            <div class="border-b border-gray-200 pb-3 mb-6">
                <h2 class="text-2xl font-bold text-gray-900 font-display">
                    Available Study Notes &amp; Curriculum Files (2)
                </h2>
                <p class="text-sm text-gray-500 mt-1">
                    Verified practical guides, PC assembly manuals, and official MSBTE K-Scheme curriculum for Computer, IT &amp; AI-ML students.
                </p>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                
            <article class="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm hover:shadow-md transition flex flex-col justify-between">
                <div>
                    <div class="flex items-start justify-between gap-3 mb-3">
                        <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold bg-blue-100 text-blue-700">
                            Official Syllabus
                        </span>
                        <span class="text-xs text-gray-400 font-medium">#1 &bull; 2025</span>
                    </div>
                    <h3 class="text-lg font-bold text-gray-900 leading-snug mb-2 break-words">
                        Computer Workshop Practice (311002) — Official MSBTE K-Scheme Curriculum &amp; Practical Scheme
                    </h3>
                    <p class="text-xs text-gray-500 mb-4">
                        Curated by <span class="font-semibold text-gray-700">MSBTE Official Board</span> for Computer (CO), IT (IF) &amp; AI-ML (AN) branches.
                    </p>
                </div>
                <div class="pt-4 border-t border-gray-100 flex flex-col sm:flex-row gap-2">
                    <a href="https://drive.google.com/file/d/1KsfLwAkqV5QBX6rUV29EwacXFAtqgP7C/preview" target="_blank" rel="noopener noreferrer"
                        class="bg-blue-50 hover:bg-blue-100 text-blue-700 px-4 py-2.5 rounded-xl font-semibold text-sm transition flex items-center justify-center gap-1.5 w-full sm:w-1/2">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
                        Preview
                    </a>
                    <a href="https://drive.google.com/file/d/1KsfLwAkqV5QBX6rUV29EwacXFAtqgP7C/view?usp=drivesdk" target="_blank" rel="noopener noreferrer"
                        class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2.5 rounded-xl font-semibold text-sm transition flex items-center justify-center gap-1.5 shadow-sm w-full sm:w-1/2">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
                        Download PDF
                    </a>
                </div>
            </article>

            <article class="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm hover:shadow-md transition flex flex-col justify-between">
                <div>
                    <div class="flex items-start justify-between gap-3 mb-3">
                        <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold bg-indigo-100 text-indigo-700">
                            Practical Guide
                        </span>
                        <span class="text-xs text-gray-400 font-medium">#2 &bull; 2025</span>
                    </div>
                    <h3 class="text-lg font-bold text-gray-900 leading-snug mb-2 break-words">
                        Computer Hardware &amp; Networking Workshop Practical Guide (PC Assembly &amp; RJ-45 Crimping)
                    </h3>
                    <p class="text-xs text-gray-500 mb-4">
                        Step-by-step practical guides for motherboard, RAM, SMPS installation, RJ-45 LAN cable crimping &amp; OS setup.
                    </p>
                </div>
                <div class="pt-4 border-t border-gray-100 flex flex-col sm:flex-row gap-2">
                    <a href="/Branches/311002-engineering-workshop-practice.html"
                        class="bg-indigo-50 hover:bg-indigo-100 text-indigo-700 px-4 py-2.5 rounded-xl font-semibold text-sm transition flex items-center justify-center gap-1.5 w-full">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                        View Lab Syllabus &amp; Experiment Details
                    </a>
                </div>
            </article>
        
            </div>
        </section>"""
if old_downloads:
    c = c[:old_downloads.start()] + new_downloads + c[old_downloads.end():]

with open('Notes/311002-engineering-workshop-practice.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("Updated 311002")

# 2. Update 311005 (Mechanical & Electrical)
with open('Notes/311005-engineering-workshop-practice.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('/resourse/note-thumbs/311005-engineering-workshop-practice.svg', '/resourse/note-thumbs/311005-engineering-workshop-practice.png')
old_downloads = re.search(r'<section class="my-10" id="downloads">.*?</section>', c, re.DOTALL)
new_downloads = """<section class="my-10" id="downloads">
            <div class="border-b border-gray-200 pb-3 mb-6">
                <h2 class="text-2xl font-bold text-gray-900 font-display">
                    Available Study Notes &amp; Files (2)
                </h2>
                <p class="text-sm text-gray-500 mt-1">
                    Download full practical workshop guide and official MSBTE K-Scheme curriculum for Mechanical and Electrical Engineering.
                </p>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                
            <article class="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm hover:shadow-md transition flex flex-col justify-between">
                <div>
                    <div class="flex items-start justify-between gap-3 mb-3">
                        <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold bg-blue-100 text-blue-700">
                            Study Notes
                        </span>
                        <span class="text-xs text-gray-400 font-medium">#1 &bull; 2025</span>
                    </div>
                    <h3 class="text-lg font-bold text-gray-900 leading-snug mb-2 break-words">
                        Engineering Workshop Practice (311005) — Practical Project &amp; Job Work Guide (Fitting, Carpentry, Welding)
                    </h3>
                    <p class="text-xs text-gray-500 mb-4">
                        Curated by <span class="font-semibold text-gray-700">MSBTE Community</span> for Mechanical (ME) &amp; Electrical (EE) students.
                    </p>
                </div>
                <div class="pt-4 border-t border-gray-100 flex flex-col sm:flex-row gap-2">
                    <a href="https://drive.google.com/file/d/12aPpjYpevgMMeQM4ZTs6zNxt4J-iMCL2/preview" target="_blank" rel="noopener noreferrer"
                        class="bg-blue-50 hover:bg-blue-100 text-blue-700 px-4 py-2.5 rounded-xl font-semibold text-sm transition flex items-center justify-center gap-1.5 w-full sm:w-1/2">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
                        Preview
                    </a>
                    <a href="https://drive.google.com/file/d/12aPpjYpevgMMeQM4ZTs6zNxt4J-iMCL2/view?usp=drivesdk" target="_blank" rel="noopener noreferrer"
                        class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2.5 rounded-xl font-semibold text-sm transition flex items-center justify-center gap-1.5 shadow-sm w-full sm:w-1/2">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
                        Download PDF
                    </a>
                </div>
            </article>

            <article class="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm hover:shadow-md transition flex flex-col justify-between">
                <div>
                    <div class="flex items-start justify-between gap-3 mb-3">
                        <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold bg-indigo-100 text-indigo-700">
                            Official Syllabus
                        </span>
                        <span class="text-xs text-gray-400 font-medium">#2 &bull; 2025</span>
                    </div>
                    <h3 class="text-lg font-bold text-gray-900 leading-snug mb-2 break-words">
                        Engineering Workshop Practice (311005) — Official MSBTE K-Scheme Syllabus &amp; Guidelines
                    </h3>
                    <p class="text-xs text-gray-500 mb-4">
                        Official board syllabus outlining all 8 workshop jobs, marking schemes, safety norms, and practical exam pattern.
                    </p>
                </div>
                <div class="pt-4 border-t border-gray-100 flex flex-col sm:flex-row gap-2">
                    <a href="https://drive.google.com/file/d/12jBZjH_kSwnrsN8aKTdMbfYM-duqsJV4/preview" target="_blank" rel="noopener noreferrer"
                        class="bg-indigo-50 hover:bg-indigo-100 text-indigo-700 px-4 py-2.5 rounded-xl font-semibold text-sm transition flex items-center justify-center gap-1.5 w-full sm:w-1/2">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
                        Preview
                    </a>
                    <a href="https://drive.google.com/file/d/12jBZjH_kSwnrsN8aKTdMbfYM-duqsJV4/view?usp=drivesdk" target="_blank" rel="noopener noreferrer"
                        class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2.5 rounded-xl font-semibold text-sm transition flex items-center justify-center gap-1.5 shadow-sm w-full sm:w-1/2">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
                        Download PDF
                    </a>
                </div>
            </article>
        
            </div>
        </section>"""
if old_downloads:
    c = c[:old_downloads.start()] + new_downloads + c[old_downloads.end():]

with open('Notes/311005-engineering-workshop-practice.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("Updated 311005")

# 3. Update 311007 (Electronics & Telecom)
with open('Notes/311007-engineering-workshop-practice.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('/resourse/note-thumbs/311007-engineering-workshop-practice.svg', '/resourse/note-thumbs/311007-engineering-workshop-practice.png')
c = c.replace('12aPpjYpevgMMeQM4ZTs6zNxt4J-iMCL2/preview', '1bCrLTxgV4hjwMnBezlHhSuTec0kn3LPo/preview')
c = c.replace(
    '<title>MSBTE 311007 Engineering Workshop Practice Notes & Study Material (K-Scheme)</title>',
    '<title>MSBTE 311007 Electronics Engineering Workshop Practice Notes & Syllabus (K-Scheme)</title>'
)
c = c.replace(
    '<h1 class="text-3xl sm:text-4xl font-bold text-gray-900 font-display leading-tight">\n            Engineering Workshop Practice (311007) â€” MSBTE Notes &amp; Study Material\n        </h1>',
    '<h1 class="text-3xl sm:text-4xl font-bold text-gray-900 font-display leading-tight">\n            Electronics Engineering Workshop Practice (311007) — MSBTE Notes &amp; Curriculum\n        </h1>'
)
old_downloads = re.search(r'<section class="my-10" id="downloads">.*?</section>', c, re.DOTALL)
new_downloads = """<section class="my-10" id="downloads">
            <div class="border-b border-gray-200 pb-3 mb-6">
                <h2 class="text-2xl font-bold text-gray-900 font-display">
                    Available Study Notes &amp; Files (2)
                </h2>
                <p class="text-sm text-gray-500 mt-1">
                    Download electronics workshop practice notes, PCB soldering guides, and official MSBTE K-Scheme curriculum for EJ &amp; IE students.
                </p>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                
            <article class="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm hover:shadow-md transition flex flex-col justify-between">
                <div>
                    <div class="flex items-start justify-between gap-3 mb-3">
                        <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold bg-blue-100 text-blue-700">
                            Official Syllabus
                        </span>
                        <span class="text-xs text-gray-400 font-medium">#1 &bull; 2025</span>
                    </div>
                    <h3 class="text-lg font-bold text-gray-900 leading-snug mb-2 break-words">
                        Electronics Workshop Practice (311007) — Official MSBTE K-Scheme Curriculum &amp; Practical Scheme
                    </h3>
                    <p class="text-xs text-gray-500 mb-4">
                        Curated by <span class="font-semibold text-gray-700">MSBTE Official Board</span> for Electronics &amp; Telecommunication (EJ/IE).
                    </p>
                </div>
                <div class="pt-4 border-t border-gray-100 flex flex-col sm:flex-row gap-2">
                    <a href="https://drive.google.com/file/d/1bCrLTxgV4hjwMnBezlHhSuTec0kn3LPo/preview" target="_blank" rel="noopener noreferrer"
                        class="bg-blue-50 hover:bg-blue-100 text-blue-700 px-4 py-2.5 rounded-xl font-semibold text-sm transition flex items-center justify-center gap-1.5 w-full sm:w-1/2">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
                        Preview
                    </a>
                    <a href="https://drive.google.com/file/d/1bCrLTxgV4hjwMnBezlHhSuTec0kn3LPo/view?usp=drivesdk" target="_blank" rel="noopener noreferrer"
                        class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2.5 rounded-xl font-semibold text-sm transition flex items-center justify-center gap-1.5 shadow-sm w-full sm:w-1/2">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
                        Download PDF
                    </a>
                </div>
            </article>

            <article class="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm hover:shadow-md transition flex flex-col justify-between">
                <div>
                    <div class="flex items-start justify-between gap-3 mb-3">
                        <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold bg-indigo-100 text-indigo-700">
                            Practical Guide
                        </span>
                        <span class="text-xs text-gray-400 font-medium">#2 &bull; 2025</span>
                    </div>
                    <h3 class="text-lg font-bold text-gray-900 leading-snug mb-2 break-words">
                        Electronic Components, PCB Soldering &amp; Breadboard Prototyping Practical Manual
                    </h3>
                    <p class="text-xs text-gray-500 mb-4">
                        Comprehensive guide to resistor color codes, testing diodes/transistors, soldering irons, desoldering pumps &amp; CRO usage.
                    </p>
                </div>
                <div class="pt-4 border-t border-gray-100 flex flex-col sm:flex-row gap-2">
                    <a href="/Branches/311007-engineering-workshop-practice.html"
                        class="bg-indigo-50 hover:bg-indigo-100 text-indigo-700 px-4 py-2.5 rounded-xl font-semibold text-sm transition flex items-center justify-center gap-1.5 w-full">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                        View Lab Syllabus &amp; Experiment Details
                    </a>
                </div>
            </article>
        
            </div>
        </section>"""
if old_downloads:
    c = c[:old_downloads.start()] + new_downloads + c[old_downloads.end():]

with open('Notes/311007-engineering-workshop-practice.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("Updated 311007")

# 4. Update 311010 (Civil)
with open('Notes/311010-civil-engineering-workshop.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('/resourse/note-thumbs/311010-civil-engineering-workshop.svg', '/resourse/note-thumbs/311010-civil-engineering-workshop.png')
c = c.replace('12aPpjYpevgMMeQM4ZTs6zNxt4J-iMCL2/preview', '1K_j4_OQS93S4P3gIUSD3MehyIMVD0D-Y/preview')
old_downloads = re.search(r'<section class="my-10" id="downloads">.*?</section>', c, re.DOTALL)
new_downloads = """<section class="my-10" id="downloads">
            <div class="border-b border-gray-200 pb-3 mb-6">
                <h2 class="text-2xl font-bold text-gray-900 font-display">
                    Available Study Notes &amp; Files (2)
                </h2>
                <p class="text-sm text-gray-500 mt-1">
                    Download full practical guide and official MSBTE K-Scheme curriculum for Civil Engineering Workshop (311010).
                </p>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                
            <article class="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm hover:shadow-md transition flex flex-col justify-between">
                <div>
                    <div class="flex items-start justify-between gap-3 mb-3">
                        <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold bg-blue-100 text-blue-700">
                            Official Syllabus
                        </span>
                        <span class="text-xs text-gray-400 font-medium">#1 &bull; 2025</span>
                    </div>
                    <h3 class="text-lg font-bold text-gray-900 leading-snug mb-2 break-words">
                        Civil Engineering Workshop (311010) — Official MSBTE K-Scheme Curriculum &amp; Practical Scheme
                    </h3>
                    <p class="text-xs text-gray-500 mb-4">
                        Curated by <span class="font-semibold text-gray-700">MSBTE Official Board</span> for Civil Engineering (CE) diploma students.
                    </p>
                </div>
                <div class="pt-4 border-t border-gray-100 flex flex-col sm:flex-row gap-2">
                    <a href="https://drive.google.com/file/d/1K_j4_OQS93S4P3gIUSD3MehyIMVD0D-Y/preview" target="_blank" rel="noopener noreferrer"
                        class="bg-blue-50 hover:bg-blue-100 text-blue-700 px-4 py-2.5 rounded-xl font-semibold text-sm transition flex items-center justify-center gap-1.5 w-full sm:w-1/2">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
                        Preview
                    </a>
                    <a href="https://drive.google.com/file/d/1K_j4_OQS93S4P3gIUSD3MehyIMVD0D-Y/view?usp=drivesdk" target="_blank" rel="noopener noreferrer"
                        class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2.5 rounded-xl font-semibold text-sm transition flex items-center justify-center gap-1.5 shadow-sm w-full sm:w-1/2">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
                        Download PDF
                    </a>
                </div>
            </article>

            <article class="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm hover:shadow-md transition flex flex-col justify-between">
                <div>
                    <div class="flex items-start justify-between gap-3 mb-3">
                        <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold bg-indigo-100 text-indigo-700">
                            Practical Guide
                        </span>
                        <span class="text-xs text-gray-400 font-medium">#2 &bull; 2025</span>
                    </div>
                    <h3 class="text-lg font-bold text-gray-900 leading-snug mb-2 break-words">
                        Masonry Bonds, Plumbing Joints &amp; Construction Safety Practical Workshop Guide
                    </h3>
                    <p class="text-xs text-gray-500 mb-4">
                        Practical manual for English &amp; Flemish bonds, pipe threading, PVC plumbing joints, bar bending, and site safety.
                    </p>
                </div>
                <div class="pt-4 border-t border-gray-100 flex flex-col sm:flex-row gap-2">
                    <a href="/Branches/311010-civil-engineering-workshop.html"
                        class="bg-indigo-50 hover:bg-indigo-100 text-indigo-700 px-4 py-2.5 rounded-xl font-semibold text-sm transition flex items-center justify-center gap-1.5 w-full">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                        View Lab Syllabus &amp; Experiment Details
                    </a>
                </div>
            </article>
        
            </div>
        </section>"""
if old_downloads:
    c = c[:old_downloads.start()] + new_downloads + c[old_downloads.end():]

with open('Notes/311010-civil-engineering-workshop.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("Updated 311010")
