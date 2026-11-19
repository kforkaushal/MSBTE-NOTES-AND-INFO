with open('about.html', 'r', encoding='utf-8') as f:
    text = f.read()

author_section = '''            <h2 class="text-2xl font-bold text-gray-900 font-display mt-8 mb-4">Editorial Team & Leadership</h2>
            <div class="bg-blue-50 border border-blue-200 rounded-xl p-6 my-6 flex flex-col md:flex-row gap-6 items-center">
                <div class="w-20 h-20 rounded-full bg-blue-600 text-white flex items-center justify-center text-2xl font-bold font-display shadow-md">
                    KP
                </div>
                <div>
                    <h3 class="text-xl font-bold text-gray-900">Kaushal Patil</h3>
                    <p class="text-sm text-blue-700 font-semibold mb-2">Founder & Lead Curator | MSBTE Diploma in Computer Engineering</p>
                    <p class="text-sm text-gray-700 leading-relaxed">
                        Kaushal Patil founded MSBTE Notes & Info to help Maharashtra polytechnic students navigate the MSBTE K-Scheme & I-Scheme curricula. With hands-on diploma engineering experience, Kaushal reviews, curates, and verifies unit-wise notes, model answer papers, and technical project roadmaps for over 20,000+ diploma learners across Maharashtra.
                    </p>
                </div>
            </div>'''

target = '<p>Whether you’re preparing for exams, working on projects, or exploring new skills, MSBTE Notes & Info is\n                here to empower your journey with reliable content and'
if target in text:
    # insert before target or after the introductory paragraphs
    pass

import re
# Insert author_section right before the "Why Choose Us" or after the intro
text = re.sub(
    r'(<p>Founded by passionate educators and professionals.*?</p>)',
    r'\1\n\n' + author_section,
    text,
    flags=re.DOTALL
)

# Also update meta author to Kaushal Patil
text = text.replace(
    '<meta name="author" content="MSBTE Notes & Info Team" />',
    '<meta name="author" content="Kaushal Patil, MSBTE Notes & Info" />'
)

# Add Person schema
person_schema = '''    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Person",
      "@id": "https://msbtenotes-info.netlify.app/about#author",
      "name": "Kaushal Patil",
      "jobTitle": "Lead Curator & Founder",
      "description": "MSBTE Diploma in Computer Engineering graduate and lead curator of MSBTE Notes & Info.",
      "url": "https://msbtenotes-info.netlify.app/about",
      "worksFor": {
        "@type": "Organization",
        "name": "MSBTE Notes & Info",
        "url": "https://msbtenotes-info.netlify.app/"
      }
    }
    </script>
'''

text = text.replace('</head>', person_schema + '</head>')

with open('about.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated about.html with Kaushal Patil author section and Person schema.")
