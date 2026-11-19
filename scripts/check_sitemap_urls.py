import xml.etree.ElementTree as ET

tree = ET.parse('sitemap.xml')
root = tree.getroot()

urls = [loc.text for loc in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]

html_urls = [u for u in urls if u.endswith('.html')]
upper_urls = [u for u in urls if any(cap in u for cap in ['/Blog/', '/Notes/', '/Branches/', '/CollegeInfo/', '/Jobs/', '/Courses/', '/News/', '/PYQ/', '/Model-Answer/'])]

print(f"Total URLs in sitemap.xml: {len(urls)}")
print(f"URLs in sitemap.xml ending with .html: {len(html_urls)}")
for u in html_urls[:10]:
    print(" ", u)
print(f"URLs in sitemap.xml with uppercase path: {len(upper_urls)}")
for u in upper_urls[:10]:
    print(" ", u)
