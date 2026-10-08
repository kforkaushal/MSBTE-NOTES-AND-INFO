# Site Inventory: MSBTE Notes & Info

**Date:** 8 October 2026  
**Site:** `https://msbtenotes-info.netlify.app/`  
**Host & Deployment:** Netlify connected to GitHub repository (`origin/Public`)  
**Architecture:** Static HTML/CSS/JS with client-side JSON hydration and Netlify direct file serving / redirects.

---

## 1. File Count & Structure Overview

- **Total HTML files:** 469 files
- **Primary Directories & HTML counts:**
  - Root: 11 HTML pages (`index.html`, `about.html`, `contact.html`, `privacy-policy.html`, `services.html`, `sitemap.html`, `internships.html`, `videos.html`, `forum.html`, `links.html`, `404.html`)
  - `Blog/`: 179 HTML pages (Blog index + 178 posts)
  - `Notes/`: 72 HTML pages (`index.html`, subject guides, question banks, handwritten notes, `Manual/` subdirectory)
  - `Branches/`: 120 HTML pages (branch semester pages, subject syllabus pages, electives)
  - `CollegeInfo/`: 36 HTML pages (district & cut-off pages, `index.html`)
  - `Jobs/`: 19 HTML pages
  - `Courses/`: 14 HTML pages
  - `mock-tests/`: 5 HTML pages
  - `News/`: 4 HTML pages

---

## 2. Templates and Partials Used

There is no server-side templating engine (e.g., Hugo, Jekyll, Next.js); pages are static HTML. However, structural conventions and generator scripts exist:
- `Notes/note_page_template.html`: Template used for generating individual subject note pages.
- `CollegeInfo/article-template.html`: Template for college cut-off and district listing pages.
- `generate_notes_pages.py`: Python generator used for bulk subject notes generation.
- Shared JS components included across pages:
  - `whatsapp-popup.js`: Floating WhatsApp bottom banner and inquiry modal.
  - `related-blogs.js`: Injects related posts dynamically into blog articles.
  - `blog.js`: Handles searching, filtering, and rendering posts on `/blog/` and homepage.
  - `Notes/notes.js`: Handles search, filter, and rendering of study materials on `/notes/`.
  - `videos.js`: Video course renderer.
  - `main.js`: Core navigation toggles.

---

## 3. Data Sources

The site uses static JSON files loaded client-side via `fetch()`:
1. `blogs.json` (~69 KB): Contains all blog post IDs, titles, descriptions, image paths, read times, categories, and tags.
2. `Notes/resources.json` (~180 KB): Catalog of downloadable PDF notes, question banks, and lab manuals.
3. `videos.json` (~7 KB): Video course modules and lecture links.
4. `news.json` (~9 KB): Announcements and notification feed.
5. `Drive_Files_Sorted_SEO.csv`: Master metadata spreadsheet of notes files and Google Drive resources.

---

## 4. URL Conventions & Standards (Phase 2 Rule)

### Standard URL Format
- **Casing:** All lowercase paths across all internal links, sitemap entries, and canonicals (e.g., `/blog/`, `/notes/`, `/branches/`, `/collegeinfo/`).
- **Trailing Slash Convention:** Follow canonical tag convention established by core pages:
  - Section indexes with trailing slashes:
    - Home: `https://msbtenotes-info.netlify.app/`
    - Blog: `https://msbtenotes-info.netlify.app/blog/`
    - Notes: `https://msbtenotes-info.netlify.app/notes/`
    - Jobs: `https://msbtenotes-info.netlify.app/jobs/`
    - College Info: `https://msbtenotes-info.netlify.app/collegeinfo/`
    - Mock Tests: `https://msbtenotes-info.netlify.app/mock-tests/`
  - Content articles and detail pages without trailing slashes:
    - Blog posts: `https://msbtenotes-info.netlify.app/blog/<post-slug>`
    - Branch pages: `https://msbtenotes-info.netlify.app/branches/<branch-slug>`
    - Subject notes: `https://msbtenotes-info.netlify.app/notes/<subject-slug>`
    - Root pages without trailing slash or with `.html` matching existing canonicals: `/about.html`, `/contact.html`, `/privacy-policy.html`, `/sitemap`.

---

## 5. Routing & Server Configuration

- **`_redirects`**: Netlify redirect rules file handling 404 fallbacks and HTTPS enforcement.
- **`robots.txt`**: Declares crawl permissions and canonical sitemap link: `https://msbtenotes-info.netlify.app/sitemap.xml`.
- **`sitemap.xml`**: Main XML sitemap indexed by search engines.
