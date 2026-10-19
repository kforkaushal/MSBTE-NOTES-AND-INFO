# Stale & Outdated Content Audit: MSBTE Notes & Info

**Date:** 8 October 2026  
**Auditor:** Antigravity AI Engineering  
**Branch:** `seo-fixes`  
**Site:** `https://msbtenotes-info.netlify.app/`

---

## Executive Summary

Search engines penalize time-sensitive academic and exam-oriented sites when past dates, superseded schedules, or expired deadlines remain presented as active or upcoming news. On MSBTE Notes & Info, several posts published during 2024–mid 2026 contain outdated schedules or past deadlines.

Per the site owner's policy in `docs/seo-audit/needs-owner-decision.md`:
- **Q12.1:** Update stale posts with verified official MSBTE facts.
- **Q12.2:** Display a visible "Last updated" date to build reader and search engine trust.

---

## Outdated & Time-Sensitive Post Inventory

| Post URL | Original Publication Date | Current Stale Information | Recommended Action |
|---|---|---|---|
| `/blog/msbte-summer-2026-expected-result-date` | 29 May 2026 | Predicts results for "3rd week of June 2026". Summer 2026 results have already been declared. | **Refresh & Cross-link**: Add clear banner linking to `/blog/msbte-summer-2026-result-declared`. Update `dateModified`. |
| `/blog/msbte-summer-2026-phase6-rescheduled` | June 2026 | Rescheduling advisory for June 2026 online exam Phase 6. Exam window has concluded. | **Archive / Informational**: Add note that exam concluded; retain for historic timetable reference. |
| `/blog/Msbte-winter-2025-exam-form` | October 2025 | Deadlines for Winter 2025 exam form submission (without late fee and with late fee). | **Refresh Annually**: Update for Winter 2026 cycle once official circular is issued. |
| `/blog/msbte-winter-2025-timetable` | November 2025 | Final theory timetable for Winter 2025 exams. | **Archive / Retain**: Retain as historic reference; update title to clarify past session. |
| `/blog/msbte-result-update-jan-2025` | 2 January 2025 | "Winter Result Declared Today 2nd Jan at 2 PM" — refers to Jan 2025 (Winter 2024 exam session). | **301 Redirect or Historic Tag**: Redirect to current result hub `/blog/msbte-winter-2025-result` or tag with "[Archive 2025]". |
| `/blog/all-india-ncat-2026` | 2026 (Expired round) | NCAT aptitude test registration deadline and exam dates. | **Refresh or Expired Banner**: Update with current contest round or display "Registration for this round has closed". |
| `/blog/naukri-young-turks-2025` | 2025 (Past cycle) | Young Turks 2025 Skill Assessment Test (SAT) competition dates. | **Refresh for 2026 Cycle**: Update dates and eligibility for 2026 edition. |

---

## Strategic Action Framework

### 1. The "Last Updated" Standard (Owner Approved)
- For all high-traffic informational posts, maintain an accurate, visible metadata badge:
  ```html
  <p class="text-sm text-gray-500">Published: [Date] • Last Updated: [Current Date]</p>
  ```
- Ensure the schema `dateModified` strictly reflects content updates.

### 2. Time-Sensitive Exam Notices Lifecycle
1. **Upcoming Phase (T-30 to T-1):** Publish expected dates, preparation checklists, timetable alerts.
2. **Declaration Phase (Day 0 to Day 7):** Immediately publish official declared link, direct portal steps, revaluation window.
3. **Post-Result Phase (Day 8+):** Update expected date posts with a top-of-page alert banner directing all organic traffic to the live result & revaluation guides.

### 3. Contest & Scholarship Expiry Protocol
- When contests or scholarships pass their deadline:
  - Keep the page indexed (do not delete or 404).
  - Add an alert box at the top:
    > **Note:** The registration window for this specific round has concluded. Check back for upcoming scholarship and contest notifications.
