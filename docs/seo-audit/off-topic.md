# Off-Topic Content Analysis & Strategic Guidance: MSBTE Notes & Info

**Date:** 8 October 2026  
**Auditor:** Antigravity AI Engineering  
**Branch:** `seo-fixes`  
**Site:** `https://msbtenotes-info.netlify.app/`

---

## Executive Summary

Search engines evaluate website topical authority under the Google Quality Rater E-E-A-T (Experience, Expertise, Authoritativeness, and Trustworthiness) framework. When a site primarily recognized for MSBTE diploma engineering study resources publishes content about celebrity obituaries or unrelated political news, search engines may experience mixed topical signals.

However, many high-traffic informational sites in Maharashtra successfully operate blended editorial coverage to reach broader youth and student demographics.

Per the site owner's policy in `docs/seo-audit/needs-owner-decision.md`:
- **Q11.1:** Keep off-topic and celebrity news posts as is.
- **Q11.2:** The owner intends to continue publishing general news and cultural tributes.

---

## Inventory of Non-Core Editorial Content

| URL | Headline / Topic | Primary Classification | Word Count |
|---|---|---|---|
| `/blog/asha-bhosle-death-news` | Asha Bhosle Passes Away at 92: Tribute & Musical Legacy | Cultural / Celebrity Tribute | ~1,245 words |
| `/blog/ajit-pawar-death-news` | Maharashtra Political Leader Tragic News / Tribute | Current Affairs / News | ~725 words |
| `/blog/nana-patekar-tribute` | Nana Patekar Passes Away at 75: Heartfelt Tribute | Cinema / Cultural Tribute | ~1,295 words |
| `/blog/ugc-new-rules-2026` | UGC Reforms 2026: New Rules for PhD, Faculty & Foreign Campuses | National Higher Education Policy | ~700 words |
| `/blog/all-india-ncat-2026` | All India NCAT 2026: Naukri Campus Aptitude Test | Commercial Campus Contest | ~620 words |
| `/blog/naukri-young-turks-2025` | Naukri Campus Young Turks 2025 (SAT) | Commercial Campus Contest | ~640 words |
| `/blog/niti-aayog-internship-2026` | NITI Aayog Internship 2026 Apply Online | National Government Internship | ~680 words |

---

## Search Engine & AdSense Considerations

### 1. Topical Authority & The "Helpful Content" System
- **Risk:** If Google's classifier determines that a substantial portion of the domain's content does not align with its declared primary topic (diploma engineering curriculum), sitewide quality scores can be affected.
- **Observation:** Currently, out of 69 blog posts and 469 total site URLs, non-engineering articles represent less than 5% of total indexed pages. This low percentage poses minimal sitewide risk provided engineering content remains the core focus.

### 2. Google AdSense & News Policy Compliance
- **Sensationalism Policy:** Google AdSense strictly monitors claims regarding sensitive events or deaths. Content must be factually accurate, respectful, and appropriately categorized as news or cultural tributes.
- **Article Schema:** All tribute posts must maintain correct `NewsArticle` or `Article` schema with attributed publisher information (completed in Phase 4).

---

## Architecture Recommendations (Balancing Strategy & Growth)

Given the owner's decision to maintain and expand general news coverage, we recommend the following structural enhancements:

1. **Category Taxonomy in Blog:**
   - Clearly delineate article sections in the blog index:
     - **Curriculum & Exam Updates:** MSBTE timetables, results, hall tickets, K-scheme notes.
     - **Career & Scholarships:** MahaDBT, national internships, NCAT tests.
     - **News & Culture / Tributes:** Tributes, state news, higher education policy.
2. **Schema Separation:**
   - Use `NewsArticle` schema for current events and cultural tributes, while using `TechArticle` or `Article` for academic guides.
3. **Internal Linking Integrity:**
   - Do not display celebrity tribute articles in "Related Resources" sidebars on syllabus and note download pages (e.g. keep them separated from OSY or PIC notes). Keep related links strictly topic-relevant.
