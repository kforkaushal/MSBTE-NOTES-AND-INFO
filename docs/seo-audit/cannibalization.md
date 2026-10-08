# Keyword Cannibalization Audit: MSBTE Notes & Info

**Date:** 8 October 2026  
**Auditor:** Antigravity AI Engineering  
**Branch:** `seo-fixes`  
**Site:** `https://msbtenotes-info.netlify.app/`

---

## Executive Summary

Keyword cannibalization occurs when multiple URLs on the same domain target the same or substantially overlapping search intents, keywords, and audience queries. On MSBTE Notes & Info, four major clusters exhibit significant cannibalization risk:

1. **Programming in C (312303) Cluster** (3 competing URLs)
2. **Summer 2026 Examination & Result Cluster** (4 competing URLs)
3. **Winter 2025 Examination & Result Cluster** (4 competing URLs)
4. **Engineering College Rankings & Directories** (4+ competing URLs across `/blog/` and `/collegeinfo/`)

Per the site owner's policy in `docs/seo-audit/needs-owner-decision.md` (*"if same content keep one, if different do not touch"* and *"keep declared one as main, keep others on blog"*), we provide the exact URL mapping, intent analysis, content comparison, and actionable recommendations.

---

## 1. Programming in C (Course Code: 312303) Cluster

### Competing URLs

| URL | Title | Type | Word Count | Canonical Target |
|---|---|---|---|---|
| `/notes/312303-programming-in-c` | Programming in C (312303) Question Bank & Notes PDF | Resource Hub | ~521 words | Self (`/notes/312303-programming-in-c`) |
| `/blog/programming-in-c-312303` | Programming in C (312303) Notes PDF \| MSBTE K-Scheme 2nd Sem | Blog Post | ~1,121 words | Self (`/blog/programming-in-c-312303`) |
| `/blog/programming-in-c-312303-v2` | 312303 Programming in C Notes, PPT, Question Bank & Model Answers | Blog Post (v2) | ~919 words | Self (`/blog/programming-in-c-312303-v2`) |

### Search Intent Analysis
- **Primary Keyword:** `MSBTE 312303 programming in c notes pdf`
- **Secondary Keywords:** `programming in c question bank 312303 k scheme`, `msbte c programming model answer paper`.
- All three URLs target the exact same 2nd-semester MSBTE diploma computer engineering subject.
- `/notes/312303-programming-in-c` acts as a quick download portal (embeds PDFs, syllabus, direct download button).
- `/blog/programming-in-c-312303` is a long-form introductory guide with chapter breakdowns and study tips.
- `/blog/programming-in-c-312303-v2` duplicates the structure of the first blog post, adding PPT slides and repeated question bank links.

### Content Overlap
- **High overlap (~70% common intent):** Google alternates rankings between `/notes/312303-programming-in-c` and `/blog/programming-in-c-312303-v2`, splitting backlink equity and click-through signals.

### Recommendations & Owner Decision
- **Owner Directive (Q10.1):** Retain different content; do not delete arbitrarily.
- **Recommended Action:**
  1. **Primary Authority URL:** Designate `/notes/312303-programming-in-c` as the core landing page for students seeking syllabus downloads and PDF question banks.
  2. **Blog Cross-Linking:** In both `/blog/programming-in-c-312303` and `/blog/programming-in-c-312303-v2`, place a prominent contextual banner at the top: *"Looking for the official 312303 Notes & Question Bank PDF? Access the main download hub here: `/notes/312303-programming-in-c`"*.
  3. **Future Consolidation:** Merge the best unique study tips from `/blog/programming-in-c-312303` into `/blog/programming-in-c-312303-v2`, then add a 301 redirect from `/blog/programming-in-c-312303` to `/blog/programming-in-c-312303-v2`.

---

## 2. Summer 2026 Result Cluster

### Competing URLs

| URL | Title | Date Published | Word Count |
|---|---|---|---|
| `/blog/msbte-summer-2026-result-declared` | MSBTE Summer 2026 Result Declared: Direct Link & Updates | June 2026 | ~974 words |
| `/blog/msbte-summer-2026-expected-result-date` | MSBTE Summer 2026 Result Date OUT? \| Check Expected Date | May 2026 | ~1,163 words |
| `/blog/msbte-summer-2026-photocopy-reevaluation` | MSBTE Summer 2026 Photocopy & Re-Evaluation \| Dates | June 2026 | ~1,126 words |
| `/blog/msbte-notes-summer-exam-2026` | MSBTE Notes For Summer Exam 2026 \| Free & Paid | March 2026 | ~790 words |

### Search Intent Analysis
- Before results are announced, users search for `msbte summer 2026 result date expected`.
- Once results are announced, query volume shifts completely to `msbte summer 2026 result link`, `msbte result declared link`, and `msbte photocopy revaluation form date`.
- Currently, `/blog/msbte-summer-2026-expected-result-date` and `/blog/msbte-summer-2026-result-declared` compete directly for `msbte summer 2026 result`.

### Recommendations & Owner Decision
- **Owner Directive (Q10.2):** Keep `/blog/msbte-summer-2026-result-declared` as the main page; keep secondary pages live in the blog index.
- **Recommended Action:**
  1. **Canonical Strategy:** Keep self-canonicals as requested by owner, but insert an alert box at the top of `/blog/msbte-summer-2026-expected-result-date`: *"Summer 2026 results have now been declared. Click here to check the live result portal: `/blog/msbte-summer-2026-result-declared`"*.
  2. **Interlink Photocopy Guide:** `/blog/msbte-summer-2026-result-declared` must link prominently to `/blog/msbte-summer-2026-photocopy-reevaluation` in the "Next Steps / Re-checking" section.

---

## 3. Winter 2025 Result Cluster

### Competing URLs

| URL | Title | Date Published | Word Count |
|---|---|---|---|
| `/blog/msbte-winter-2025-result` | MSBTE Result Winter 2026 (Winter 2025 Exam) \| Date & Link Declared | Jan 2026 | ~722 words |
| `/blog/msbte-winter-2025-result-revaluation-guide` | MSBTE Winter 2025 Result OUT: Revaluation, Photocopy & Grace Marks | Jan 2026 | ~1,145 words |
| `/blog/msbte-result-update-jan-2025` | MSBTE Result 2025 LIVE \| Winter Result Declared Today | Jan 2025 | ~548 words |
| `/blog/Msbte-winter-2025-exam-form` | MSBTE Winter 2025 Exam Form Fill up Dates | Oct 2025 | ~610 words |

### Search Intent Analysis
- MSBTE's Winter session is officially designated "Winter 2025", but examinations and results roll into January/February 2026.
- `/blog/msbte-winter-2025-result` and `/blog/msbte-result-update-jan-2025` target the exact same headline: "Winter Result Declared Today".
- Users searching for revaluation / photocopy grace marks land on `/blog/msbte-winter-2025-result-revaluation-guide`.

### Recommendations & Owner Decision
- **Owner Directive (Q10.3):** Keep `/blog/msbte-winter-2025-result` as the main page.
- **Recommended Action:**
  1. **Update Jan 2025 Post:** `/blog/msbte-result-update-jan-2025` refers to the previous academic year (Winter 2024 exam declared Jan 2025). Add a prominent historic notice or 301 redirect it to `/blog/msbte-winter-2025-result`.
  2. **Internal Architecture:** Ensure `/blog/msbte-winter-2025-result` links directly to `/blog/msbte-winter-2025-result-revaluation-guide`.

---

## 4. Engineering College Directories & Rankings

### Competing URLs

| URL | Title | Scope | Word Count |
|---|---|---|---|
| `/blog/top-engineering-colleges-pune` | Top Engineering Colleges in Pune 2026 \| Cutoffs, Fees & Ranking | Pune city | ~1,450 words |
| `/blog/top-5-engineering-colleges-maharashtra` | Top 5 Engineering Colleges in Maharashtra (MHT CET / DSE) | State (Top 5) | ~1,100 words |
| `/blog/top-20-engineering-colleges-maharashtra` | Top 20 Engineering Colleges in Maharashtra: Complete Guide | State (Top 20) | ~3,200 words |
| `/blog/autonomous-engineering-colleges-maharashtra` | List of Autonomous Engineering Colleges in Maharashtra | Autonomous only | ~1,350 words |
| `/collegeinfo/pune` | Top Diploma Engineering Colleges in Pune District | Pune District Hub | ~450 words |
| `/collegeinfo/mumbai` | Top Diploma Engineering Colleges in Mumbai Region | Mumbai District Hub | ~420 words |

### Search Intent Analysis
- **Degree vs. Diploma Discrepancy:** The blog posts target *degree* engineering colleges (COEP, VJTI, PICT, SPIT) for DSE (Direct Second Year Engineering admission after diploma).
- The `/collegeinfo/*.html` pages target *polytechnic diploma* colleges in each district (Government Polytechnic Pune, etc.).
- There is minimal direct cannibalization because the scope differs (State Top 20 vs. Pune vs. Autonomous), but search engines may confuse degree vs. polytechnic intent without clear title delineation.

### Recommendations & Owner Decision
- **Owner Directive (Q10.4):** Keep all pages live because they target distinct queries.
- **Recommended Action:**
  1. **Title Differentiation:** In `/blog/top-engineering-colleges-pune`, clarify the title: *"Top Engineering Colleges in Pune for DSE & B.Tech 2026"*.
  2. In `/collegeinfo/pune.html`, maintain clear branding: *"Top Polytechnic & Diploma Colleges in Pune District"*.
  3. Cross-link the district hubs into the comprehensive state guide.
