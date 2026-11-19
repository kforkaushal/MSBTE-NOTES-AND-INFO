import os
import re

all_html = []
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'brain', '.gemini', '.system_generated'}]
    for f in files:
        if f.endswith('.html'):
            p = os.path.relpath(os.path.join(root, f), '.').replace('\\', '/')
            all_html.append(p)

print(f"Total HTML files on disk: {len(all_html)}")

# Categorize
known_verification_or_system = {
    '404.html',
    'googlef85124961115b472.html',
    'yandex_7a3f92ea9dc08f64.html',
    'pinterest-9961f.html'
}

templates_or_blank = {
    'Notes/Manual/manual-blank.html',
    'video-course/topic-template.html',
    'CollegeInfo/article-template.html',
    'Courses/test.html',
    'Courses/certificate.html', # certificate generator page (has noindex)
    'Jobs/apply-redirect.html', # redirector
    'Jobs/success-redirect.html',
    'Jobs/jobs.html', # duplicate of /jobs/
    'Jobs/bookmarked-jobs.html',
    'Jobs/job-detail.html',
    'form/student-data.html',
    'form/success.html',
    'mock-tests/admin.html',
    'mock-tests/profile.html'
}

noindexed_obits = {
    'Blog/nana-patekar-tribute.html',
    'Blog/asha-bhosle-death-news.html',
    'Blog/ajit-pawar-death-news.html'
}

# Also note duplicate folder index files in pyq and model-answer
duplicate_folder_indices = []
for f in all_html:
    if ('pyq/' in f or 'model-answer/' in f) and f.endswith('/index.html') and f != 'pyq/index.html' and f != 'model-answer/index.html':
        duplicate_folder_indices.append(f)

print(f"Duplicate folder index files: {len(duplicate_folder_indices)}")

# Check canonical of each remaining
indexable = []
for f in all_html:
    if f in known_verification_or_system or f in templates_or_blank or f in noindexed_obits or f in duplicate_folder_indices:
        continue
    indexable.append(f)

print(f"True indexable HTML files: {len(indexable)}")
