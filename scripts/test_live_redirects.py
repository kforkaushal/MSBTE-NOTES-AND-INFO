import urllib.request

test_urls = [
    "https://msbtenotes-info.netlify.app/Blog/dpharm-exit-exam-cancelled-2026.html",
    "https://msbtenotes-info.netlify.app/pyq/315313-theory-of-structures/",
    "https://msbtenotes-info.netlify.app/Notes/",
    "https://msbtenotes-info.netlify.app/notes/?q={search_term_string}",
    "https://msbtenotes-info.netlify.app/Notes/Manual/basic-mechanical-engineering-lab-manual.html"
]

class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        print(f"  -> Redirect [{code}] to: {newurl}")
        return super().redirect_request(req, fp, code, msg, headers, newurl)

opener = urllib.request.build_opener(NoRedirectHandler)

for u in test_urls:
    print(f"\nTesting: {u}")
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'})
        resp = opener.open(req)
        print(f"Final URL: {resp.geturl()} | Status: {resp.getcode()}")
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        if 'location' in e.headers:
            print(f"Location header: {e.headers['location']}")
    except Exception as e:
        print(f"Error: {e}")
