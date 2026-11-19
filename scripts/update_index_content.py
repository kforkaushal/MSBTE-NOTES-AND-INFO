import re

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Replace Nana Patekar card in blogContainer
nana_card_pattern = r'<div class="bg-white rounded-xl shadow-lg overflow-hidden flex flex-col h-full hover:shadow-2xl transition duration-300 transform hover:-translate-y-2 group">\s*<div class="relative overflow-hidden aspect-video w-full" style="aspect-ratio: 16 / 9;">\s*<img src="/resourse/blog-resourse/nana-patekar-tribute\.webp".*?</div>\s*</div>\s*</div>'

winter_exam_card = '''<div
            class="bg-white rounded-xl shadow-lg overflow-hidden flex flex-col h-full hover:shadow-2xl transition duration-300 transform hover:-translate-y-2 group">
            <div class="relative overflow-hidden aspect-video w-full" style="aspect-ratio: 16 / 9;">
              <img src="/resourse/blog-resourse/msbte-winter-2025-exam-form.webp"
                alt="MSBTE Winter Exam Form 2026 Schedule & Guidelines"
                class="w-full h-full object-cover group-hover:scale-110 transition duration-500"
                width="640" height="360" loading="lazy" decoding="async">
              <div class="absolute top-4 left-4">
                <span
                  class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider shadow-md opacity-90 group-hover:opacity-100 transition duration-300">
                  Exam Form 2026
                </span>
              </div>
            </div>
            <div class="p-6 flex flex-col flex-grow">
              <div class="flex items-center text-xs text-blue-700 font-semibold mb-3">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                </svg>
                Nov 15, 2026
              </div>
              <h3
                class="text-xl font-bold text-gray-800 mb-3 group-hover:text-blue-600 transition duration-300 leading-snug line-clamp-2">
                MSBTE Winter Exam Form 2026: Last Date, Login Link & Fees
              </h3>
              <p class="text-gray-600 text-sm mb-6 line-clamp-3 leading-relaxed">
                Fill MSBTE Winter diploma exam form online. Direct login link, step-by-step instructions, regular & late fee schedules, and confirmation steps.
              </p>
              <div class="mt-auto">
                <a href="/blog/msbte-winter-2025-exam-form" aria-label="Read more about MSBTE Winter Exam Form 2026"
                  class="inline-flex items-center text-blue-600 font-bold text-sm group-hover:underline">
                  Read More
                  <svg class="w-4 h-4 ml-2 group-hover:translate-x-1 transition duration-300" fill="none"
                    stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3">
                    </path>
                  </svg>
                </a>
              </div>
            </div>
          </div>'''

c = re.sub(nana_card_pattern, winter_exam_card, c, count=1, flags=re.DOTALL)

# 2. Fix OSY card on index.html: 314319 4th sem -> 315319 5th sem
c = c.replace(
    'Free MSBTE K-Scheme 314319 – Operating System (OSY) unit-wise notes, important question bank, model\n                answers, and complete revision roadmaps for 4th Semester.',
    'Free MSBTE K-Scheme 315319 – Operating System (OSY) unit-wise notes, important question bank, model answers, and complete revision roadmaps for 5th Semester.'
)
c = c.replace('alt="Operating System OSY 314319 K Scheme Notes Thumbnail"', 'alt="Operating System OSY 315319 K Scheme Notes Thumbnail"')

# 3. Fix noscript obituaries
c = re.sub(
    r'<div class="p-4 bg-white rounded-xl shadow"><a href="/blog/nana-patekar-tribute\.html".*?</div>',
    '<div class="p-4 bg-white rounded-xl shadow"><a href="/blog/msbte-winter-2025-exam-form" class="font-bold text-blue-600 hover:underline">MSBTE Winter Exam Form 2026: Last Date, Login Link & Fees</a><p class="text-sm text-gray-600 mt-2">Fill MSBTE Winter diploma exam form online. Direct login link, step-by-step instructions, regular & late fee schedules, and confirmation steps.</p></div>',
    c, flags=re.DOTALL
)

c = re.sub(
    r'<div class="p-4 bg-white rounded-xl shadow"><a href="/blog/asha-bhosle-death-news\.html".*?</div>',
    '<div class="p-4 bg-white rounded-xl shadow"><a href="/blog/dpharm-exit-exam-cancelled-2026" class="font-bold text-blue-600 hover:underline">D.Pharm Exit Exam 2026 Cancelled: Latest Update & Next Steps</a><p class="text-sm text-gray-600 mt-2">PCI officially cancelled the D.Pharm Exit Exam for 2026. Complete notification breakdown, eligibility rules, and PCI registration guidelines.</p></div>',
    c, flags=re.DOTALL
)

# 4. Fix student count inconsistency: 1000+ -> 20,000+
c = c.replace(
    '<p class="text-gray-600 mb-4 text-lg">Trusted by 1000+ diploma students across Maharashtra</p>',
    '<p class="text-gray-600 mb-4 text-lg">Trusted by 20,000+ diploma students across Maharashtra</p>'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Updated index.html: cards, student count, and noscript.")
