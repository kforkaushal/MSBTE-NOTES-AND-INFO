# MSBTE Notes & Info

[![Netlify Status](https://api.netlify.com/api/v1/badges/your-badge/deploy-status)](https://msbtenotes-info.netlify.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Website](https://img.shields.io/badge/Website-Live-brightgreen)](https://msbtenotes-info.netlify.app/)

> **MSBTE Notes & Info** is an independent educational resource platform dedicated to Maharashtra State Board of Technical Education (MSBTE) diploma engineering students. The platform provides structured study resources, semester-wise notes, previous-year question banks, model answers, syllabus details, and career guidance.

---

## 🌟 Key Features

- **Branch & Semester-Wise Resources**: Complete subject coverage for Computer, Information Technology, Civil, Mechanical, Electrical, E&TC, and AI & Machine Learning.
- **Curriculum Alignment**: Detailed coverage for both **K-Scheme** and **I-Scheme** courses.
- **Syllabus Finder**: Fast, interactive search tool to locate official curriculum PDFs by branch, scheme, and semester.
- **Question Banks & Model Answers**: Previous year question papers, unit test papers, and model answers.
- **Lab Manuals & Practical Solutions**: Solved laboratory manuals and experiment guides.
- **Free Video Courses**: Practical programming and technical courses with certificates.
- **Jobs & Internships Board**: Curated job and internship directory for diploma holders.
- **AI-Search Ready & SEO Optimized**: Structured JSON-LD schemas (`EducationalOrganization`, `BreadcrumbList`, `BlogPosting`, `FAQPage`), standards-compliant `robots.txt`, XML sitemaps, and `llms.txt`.

---

## 📂 Project Structure

```text
MSBTE-NOTES-AND-INFO/
├── index.html              # Main landing page
├── about.html              # About platform & team
├── contact.html            # Contact & contribution feedback
├── privacy-policy.html     # Privacy policy & data standards
├── internships.html        # Internship opportunities
├── services.html           # Platform resources & services
├── videos.html             # Video courses directory
├── sitemap.xml             # XML sitemap (canonical URLs)
├── robots.txt              # Search engine & AI crawler policies
├── llms.txt                # AI assistant / LLM context
│
├── Branches/               # Department hubs & subject syllabus pages
│   ├── Computer.html
│   ├── Information-Technology.html
│   ├── Civil.html
│   ├── Electrical-Engineering.html
│   ├── ETC-Engineering.html
│   ├── Mechanical-Engineering.html
│   ├── AI-ML.html
│   └── [code]-[subject].html   # 150+ subject-specific pages
│
├── Notes/                  # Subject notes, question banks & lab manuals
│   ├── index.html          # Notes central hub
│   ├── msbte-k-scheme-question-banks.html
│   ├── Manual/             # Solved lab manuals
│   └── [code]-[subject].html
│
├── scheme/                 # Syllabus finder & curriculum breakdowns
│   ├── index.html          # Interactive Syllabus Finder
│   ├── k-scheme.html       # K-Scheme course structures
│   └── i-scheme.html       # I-Scheme course structures
│
├── Blog/                   # Educational articles, exam tips & news
└── Jobs/                   # Job listings and details
```

---

## 💻 Tech Stack

- **Core**: Semantic HTML5, Vanilla JavaScript (ES6+)
- **Styling**: Tailwind CSS & Vanilla CSS
- **Structured Data**: Schema.org JSON-LD (`BreadcrumbList`, `EducationalOrganization`, `BlogPosting`, `FAQPage`)
- **Hosting & CI/CD**: Netlify / GitHub Pages (Static hosting)

---

## 🚀 Getting Started Locally

You can serve this project with any standard local HTTP server (Live Server, Python HTTP server, or `npx serve`).

### Option 1: Python HTTP Server
```bash
# Clone the repository
git clone https://github.com/kforkaushal/MSBTE-NOTES-AND-INFO.git

# Navigate to project directory
cd MSBTE-NOTES-AND-INFO

# Run local web server
python -m http.server 8000
```
Open `http://localhost:8000` in your browser.

### Option 2: Node.js / npx serve
```bash
npx serve .
```

---

## 🤖 AI Search & Web Standards Compliance

The platform is optimized for both traditional search engines (Google, Bing) and AI search assistants (ChatGPT Search, Perplexity, Claude, Gemini):
- [`robots.txt`](file:///c:/Users/bitbu/OneDrive/Documents/GitHub/MSBTE-NOTES-AND-INFO/robots.txt): Configured to allow crawlers including `Googlebot`, `Bingbot`, `OAI-SearchBot`, `ChatGPT-User`, `Claude-SearchBot`, `PerplexityBot`, and training bots.
- [`llms.txt`](file:///c:/Users/bitbu/OneDrive/Documents/GitHub/MSBTE-NOTES-AND-INFO/llms.txt): Machine-readable summary for AI agents describing courses, branches, and resources.
- [`sitemap.xml`](file:///c:/Users/bitbu/OneDrive/Documents/GitHub/MSBTE-NOTES-AND-INFO/sitemap.xml): Regularly updated canonical sitemap with priority ratings and update timestamps.

---

## ⚖️ Disclaimer

**MSBTE Notes & Info** is an independent educational platform created to support diploma students. This website is **not affiliated with, endorsed by, or officially associated with** the Maharashtra State Board of Technical Education (MSBTE). Official MSBTE notifications, curriculum documents, and results should always be verified on the official MSBTE website (`msbte.org.in`).

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
