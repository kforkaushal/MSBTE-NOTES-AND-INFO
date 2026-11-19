import urllib.request

test_urls = [
    "https://msbtenotes-info.netlify.app/Notes/java-k-scheme-notes.html",
    "https://msbtenotes-info.netlify.app/Notes/dcn-k-scheme-notes.html",
    "https://msbtenotes-info.netlify.app/Notes/osy-k-scheme-notes.html",
    "https://msbtenotes-info.netlify.app/Blog/dse-admission-2026-27-maharashtra.html"
]

class RedirectTracker(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        print(f"   [{code} Redirect] -> {newurl}")
        return super().redirect_request(req, fp, code, msg, headers, newurl)

opener = urllib.request.build_opener(RedirectTracker)

for u in test_urls:
    print(f"\nTesting: {u}")
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'})
        resp = opener.open(req)
        print(f"-> SUCCESS: Final URL = {resp.geturl()} | Status = {resp.getcode()}")
    except Exception as e:
        print(f"-> FAILED: {e}")
