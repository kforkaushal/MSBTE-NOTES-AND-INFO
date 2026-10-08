# SEO Audit & Technical Fixes Changelog

**Repository:** `MSBTE-NOTES-AND-INFO`  
**Branch:** `seo-fixes`  
**Target:** Safe, zero-visual-impact technical and SEO enhancements.

---

## Changes Log

### Phase 0: Recon and Safety Net
- **Commit:** `4ac2704`
- **Branch Created**: `seo-fixes` branched from current working tree.
- **Owner Decisions Loaded**: Ingested all owner answers from `needs-owner-decision.md`.
- **Baseline Snapshots**:
  - Saved visible text for 12 representative pages in `baseline/`.
  - Extracted URL inventory of all 469 HTML pages in `baseline/urls_inventory.txt`.
  - Analyzed and classified 543 links across representative pages into `baseline/links.csv`.
- **Site Inventory**: Documented structure, files, data sources, and URL conventions in `inventory.md`.

### Phase 1: Zero-Visual-Impact Metadata & Baseline Fixes
- **Commit `d4ade9d` (1.1):** Removed obsolete meta tags (`revisit-after`, `expires`, `distribution`, `coverage`, `rating`) and redundant keywords from `index.html`, `Blog/msbte-result-update-jan-2025.html`, `Courses/DSA-Basic.html`, and `Notes/4th-sem-computer-microprojects.html`.
- **Commit `2e8eeea` (1.2):** Removed placeholder `google-site-verification` from `Notes/index.html` and `Blog/msbte-result-update-jan-2025.html`.
- **Commit `9414a52` (1.3):** Standardized Twitter handles across all 114 HTML files to `@msbtenotes` (confirmed owner handle).
- **Commit `fe336d3` (1.4):** Set `og:locale` to `en_IN` on `index.html`.
- **Commit `810b369` (1.5):** Aligned home canonical to `https://msbtenotes-info.netlify.app/` matching `og:url` and `sitemap.xml`.
- **Commit `70308c1` (1.6):** Replaced SVG `og:image` with fallback PNG `https://msbtenotes-info.netlify.app/resourse/MSBTE%20NOTES%20AND%20INFORMATION.png` across 242 branch pages; added missing `robots` and `twitter:*` tags.
- **Commit `3ff06f6` (1.7):** Shortened `/blog/` meta description to 156 characters.
- **Commit `3083baf` (1.8):** Standardized footer copyright to `2026` across all 357 HTML pages.
- **Commit `e6c8032` (1.9):** Removed "Official Resources" claims from 42 branch meta descriptions.
- **Commit `76a4184` (1.10):** Added descriptive alt text to reviewer avatars on `index.html` (`Avatar of Ritika Patil`, etc.).
- **Commit `5964ba9` (1.11):** Updated `/ #blogs` breadcrumbs to canonical `/blog/` in 81 files.
- **Commit `e2bb7b9` (1.12):** Changed home footer `#internships` link to `/internships`.
- **Commit `d00963e` (1.13):** Fixed internal link in `Branches/Computer-Semester-5.html` to `315004-internship-12-weeks.html`; added 301 redirects in `_redirects` for `315004-internship12-weeks` and `316326-emerging-trends-in-electrical-engineering`.
- **Phase 1 Acceptance:** Verified with automated visible text diff (`verify_phase1_text.py`); confirmed zero unintended visible text changes across all 12 representative baseline pages.

### Phase 2: URLs, Canonicals & Redirects
- **Commit `76dd717`:**
  - Standardized internal link casing across 162 files to lowercase paths (`/blog/`, `/notes/`, `/branches/`, `/collegeinfo/`, `/jobs/`, `/courses/`).
  - Added uppercase-to-lowercase 301 wildcard rules in `_redirects` (Netlify case-sensitive redirect rules).
  - Aligned `sitemap.html` canonical to `/sitemap`.
  - Fixed mechanical elective typo (`315367` instead of `315363`) in `sitemap.html` and `sitemap.xml`.
- **Commit `8263c79`:** Added `rel="noopener noreferrer"` to all external `target="_blank"` links in 443 HTML files.
- **External PDF Links Audit:** Tested `http://bvcoelp.bharatividyapeeth.edu/` PDF links; identified SSL hostname mismatch on external server. Left on HTTP per owner's explicit decision Q8.1 and cataloged 78 affected URLs for owner review.

### Phase 3: Crawlability of JS-Loaded Content
- **Commit `1ebd782` & `7225676`:**
  - Converted home "What We Provide" cards into accessible `<a>` anchor links.
  - Added Amazon Associate disclosure (`As an Amazon Associate, we may earn from qualifying purchases.`) below book scroller and shop section on `Notes/index.html`.
  - Added `aria-hidden="true"` to duplicate clone cards in book scroller.
  - Injected pre-rendered crawlable HTML cards and `<noscript>` fallback links into `Blog/index.html` (`#blogContainer`), `Notes/index.html` (`#resource-grid`), and `index.html` (`#notesGrid`, `#blogContainer`).

### Phase 4: Structured Data & Trust Additions
- **Commit `545b703`:**
  - In `index.html`: updated `Organization` logo to `/resourse/android-chrome-512x512.png`.
  - Added `sameAs` array with YouTube, Product Hunt, Telegram, WhatsApp Channel.
  - Added `WebSite` schema with sitelinks searchbox potentialAction.
  - Removed unsupported `AggregateRating` from `Organization` schema.
  - Added subtle disclaimer in home page footer: *"Not affiliated with or endorsed by MSBTE. Official information is available at msbte.ac.in."*
- **Commit `6d13833`:**
  - Added missing `BreadcrumbList` schema to 16 blog posts and 13 lab manuals in `Notes/Manual/`.
  - Added missing `Article` schema to `Blog/all-india-ncat-2026.html`, `Blog/naukri-young-turks-2025.html`, and `Blog/mahadbt-scholarship-error-solutions.html`.
  - Added missing `dateModified` to `Blog/5-Free-Courses.html`, `Blog/engineering-day-2025.html`, `Blog/msbte-winter-2025-study-strategies.html`, and `Blog/skills-2025.html`.

### Phase 5: Audit Documentation for Site Owner
- Generated complete audit reports in `docs/seo-audit/`:
  - `cannibalization.md`: In-depth analysis of 4 competing clusters (Programming in C, Summer 2026 Results, Winter 2025 Results, College Rankings) with intent mapping and canonical recommendations.
  - `stale-posts.md`: Audit of time-sensitive exam schedules, past result forecasts, and expired contest deadlines with maintenance frameworks.
  - `thin-pages.md`: Analysis of 294 pages under 150 words (subject stubs, lab manuals, video courses, dynamic shells) with remediation roadmap.
  - `off-topic.md`: Evaluation of non-core celebrity/political posts within the E-E-A-T and AdSense frameworks following the owner's editorial expansion decision.
  - `needs-owner-decision.md`: Updated with full inventory of 78 insecure external PDF links that failed HTTPS verification.

### Phase 6: Footer Audit & Precise Restoration
- **Commit `eab868f` & `4ff5f4a`:**
  - Audited all 469 HTML pages against original branch `main` (`origin/Public`).
  - Restored inline footer code across all 448 pages to match `main` byte-for-byte, retaining strictly authorized changes: consistent 2026 copyright year, `/internships` link, canonical link casing, and subtle home disclaimer.
  - Removed unauthorized `rel="noopener noreferrer"` additions and line-wrapping inside footer blocks.
  - Documented complete inventory in `docs/footer-check/pages.md` and page-by-page audit report in `docs/footer-check/report.md`.

### Phase 7: Sitemap, Slug, Redirects & Repository Security
- **Commit `e9abab6`:** Removed non-sitemap `llms.txt` entry from `robots.txt`, leaving only `sitemap.xml`.
- **Commit `c6d4c43`:**
  - Renamed `Ads.txt` to lowercase `ads.txt` and added `/Ads.txt /ads.txt 301!` redirect.
  - Reordered `_redirects` so that 301 redirects and uppercase rules precede the `/* /404.html 404` catch-all at the bottom.
  - Added `brain/` to `.gitignore` and removed cached Antigravity artifact files from git.
- **Commit `e68e9d4`:**
  - Corrected electrical engineering elective slug from typo `3316326` to official MSBTE code `316326` in `Branches/`, `sitemap.html`, and `sitemap.xml`. Added 301 redirect for legacy `3316326` slug.
  - Added newly created tribute post `/blog/nana-patekar-tribute` to both `sitemap.html` and `sitemap.xml`.
  - Standardized remaining `/News/` nav links in `index.html` and `News/index.html` to canonical lowercase `/news/`.
  - Replaced bulk static dates with authentic commit dates in `sitemap.xml` `lastmod` tags.
  - Verified `database.rules.json`: confirmed Firebase Realtime Database rules prevent open public writes.
