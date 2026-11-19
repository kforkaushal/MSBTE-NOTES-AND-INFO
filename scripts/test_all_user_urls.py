import urllib.request
import urllib.error

user_urls = [
    "https://msbtenotes-info.netlify.app/Blog/dpharm-exit-exam-cancelled-2026.html",
    "https://msbtenotes-info.netlify.app/Blog/msbte-winter-2025-exam-form.html",
    "https://msbtenotes-info.netlify.app/Branches/316338-computer-network-data-communication.html",
    "https://msbtenotes-info.netlify.app/pyq/315313-theory-of-structures/",
    "https://msbtenotes-info.netlify.app/Notes/",
    "https://msbtenotes-info.netlify.app/Branches/313323-highway-engineering.html",
    "https://msbtenotes-info.netlify.app/Branches/315313-theory-of-structures.html",
    "https://msbtenotes-info.netlify.app/pyq/316310-building-services/",
    "https://msbtenotes-info.netlify.app/Branches/315334-switchgear-and-protection.html",
    "https://msbtenotes-info.netlify.app/Branches/312315-elements-of-electrical-engineering.html",
    "https://msbtenotes-info.netlify.app/model-answer/315327-cloud-computing-for-data-science/",
    "https://msbtenotes-info.netlify.app/Branches/312314-basic-electronics.html",
    "https://msbtenotes-info.netlify.app/notes/?q={search_term_string}",
    "https://msbtenotes-info.netlify.app/courses/DSA-Basic",
    "https://msbtenotes-info.netlify.app/Blog/msbte-winter-2025-photocopy-reevaluation.html",
    "https://msbtenotes-info.netlify.app/Notes/dsa-handwritten-notes.html",
    "https://msbtenotes-info.netlify.app/Blog/msbte-institute-wise-summer-2026-timetable.html",
    "https://msbtenotes-info.netlify.app/Blog/how-to-study-smarter-using-ai-msbte.html",
    "https://msbtenotes-info.netlify.app/Blog/sppu-result-winter-2025.html",
    "https://msbtenotes-info.netlify.app/Notes/Manual/basic-mechanical-engineering-lab-manual.html",
    "https://msbtenotes-info.netlify.app/notes/Manual/basic-mechanical-engineering-lab-manual.html",
    "https://msbtenotes-info.netlify.app/Notes/315321-advance-computer-network.html",
    "https://msbtenotes-info.netlify.app/Blog/msbte-winter-2025-timetable.html",
    "https://msbtenotes-info.netlify.app/Branches/elective-316330-industrial-drives-and-control.html",
    "https://msbtenotes-info.netlify.app/Branches/314005-ui-ux-design.html",
    "https://msbtenotes-info.netlify.app/Branches/312310-fundamental-of-electrical-engineering.html",
    "https://msbtenotes-info.netlify.app/Notes/advanced-java-notes.html",
    "https://msbtenotes-info.netlify.app/Branches/312308-appliedscience.html",
    "https://msbtenotes-info.netlify.app/Branches/316013-3d-modelling-and-additive-manufacturing.html",
    "https://msbtenotes-info.netlify.app/Blog/ajit-pawar-death-news.html",
    "https://msbtenotes-info.netlify.app/Blog/msbte-winter-2025-study-strategies.html",
    "https://msbtenotes-info.netlify.app/Blog/fake-news-alert-msbte-exams.html",
    "https://msbtenotes-info.netlify.app/Branches/316328-maintenance-of-electrical-equipments.html",
    "https://msbtenotes-info.netlify.app/Branches/314315-geotechnical-engineering.html",
    "https://msbtenotes-info.netlify.app/Blog/what-to-do-after-10th.html",
    "https://msbtenotes-info.netlify.app/Blog/mahadbt-scholarship-error-solutions.html",
    "https://msbtenotes-info.netlify.app/Blog/aaple-sarkar-dbt-portal-guide.html",
    "https://msbtenotes-info.netlify.app/Blog/msbte-summer-2026-final-timetable-declared-diploma.html",
    "https://msbtenotes-info.netlify.app/Blog/msbte-summer-2026-hall-ticket.html",
    "https://msbtenotes-info.netlify.app/Notes/20-microproject-ideas-dbms.html",
    "https://msbtenotes-info.netlify.app/Blog/msbte-result-update-jan-2025.html",
    "https://msbtenotes-info.netlify.app/Blog/autonomous-engineering-colleges-maharashtra.html",
    "https://msbtenotes-info.netlify.app/Notes/Manual/engineering-mechanics-lab-manual.html",
    "https://msbtenotes-info.netlify.app/notes/Manual/engineering-mechanics-lab-manual.html",
    "https://msbtenotes-info.netlify.app/Notes/4th-sem-computer-microprojects.html",
    "https://msbtenotes-info.netlify.app/Blog/msbte-summer-2026-exam-result-date-and-link.html",
    "https://msbtenotes-info.netlify.app/Notes/msbte-computer-engg-question-bank.html",
    "https://msbtenotes-info.netlify.app/Blog/post-matric-scholarship-obc.html",
    "https://msbtenotes-info.netlify.app/Blog/50-capstone-project-ideas-computer-engineering.html",
    "https://msbtenotes-info.netlify.app/Blog/msbte-winter-2025-result.html",
    "https://msbtenotes-info.netlify.app/Blog/msbte-winter-2025-result-revaluation-guide.html",
    "https://msbtenotes-info.netlify.app/Blog/msbte-summer-2026-expected-result-date.html",
    "https://msbtenotes-info.netlify.app/Blog/msbte-winter-2025-hall-ticket.html",
    "https://msbtenotes-info.netlify.app/Notes/Manual/312303-pic-programming-in-c-manual-answers.html",
    "https://msbtenotes-info.netlify.app/Blog/msbte-academic-calendar-2025-26.html",
    "https://msbtenotes-info.netlify.app/Blog/programming-in-c-312303-v2.html",
    "https://msbtenotes-info.netlify.app/Branches/Mechanical-Engineering-Semester-3.html",
    "https://msbtenotes-info.netlify.app/CollegeInfo/amravati.html",
    "https://msbtenotes-info.netlify.app/Blog/msbte-summer-2026-exam-roadmap.html",
    "https://msbtenotes-info.netlify.app/Blog/cm-fellowship-maharashtra-2026.html",
    "https://msbtenotes-info.netlify.app/Branches/Computer.html",
    "https://msbtenotes-info.netlify.app/Branches/elective-315374-power-plant-engineering.html",
    "https://msbtenotes-info.netlify.app/Blog/top-5-engineering-colleges-maharashtra.html",
    "https://msbtenotes-info.netlify.app/Jobs/",
    "https://msbtenotes-info.netlify.app/Branches/Computer-I-Scheme.html",
    "https://msbtenotes-info.netlify.app/Branches/elective-316310-building-services.html",
    "https://msbtenotes-info.netlify.app/Blog/msbte-notes-summer-exam-2026.html",
    "https://msbtenotes-info.netlify.app/Notes/314318-data-communication-and-computer-network.html",
    "https://msbtenotes-info.netlify.app/CollegeInfo/raigad.html",
    "https://msbtenotes-info.netlify.app/Blog/professional-software-project-development.html",
    "https://msbtenotes-info.netlify.app/Blog/what-to-do-after-diploma.html",
    "https://msbtenotes-info.netlify.app/Branches/AI-ML-Semester-3.html",
    "https://msbtenotes-info.netlify.app/Branches/312312-engineering-mechanics.html",
    "https://msbtenotes-info.netlify.app/Notes/316314-software-testing.html",
    "https://msbtenotes-info.netlify.app/CollegeInfo/article-template.html"
]

results = []

for u in user_urls:
    try:
        # Quote curly braces if needed
        safe_url = u.replace('{', '%7B').replace('}', '%7D')
        req = urllib.request.Request(safe_url, headers={'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            results.append((u, resp.getcode(), resp.geturl()))
    except urllib.error.HTTPError as e:
        results.append((u, e.code, f"HTTPError {e.reason}"))
    except Exception as e:
        results.append((u, 0, f"Error {e}"))

print(f"Total tested: {len(results)}")
errors = [r for r in results if r[1] != 200]
print(f"Errors count: {len(errors)}")
for err in errors:
    print(err)
