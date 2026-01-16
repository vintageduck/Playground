from bs4 import BeautifulSoup
import json

with open('everyman_debug.html', 'r') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Print all script sources or content
scripts = soup.find_all('script')
for s in scripts:
    if s.string:
        if "JSON" in s.string or "props" in s.string:
            print("Found script with JSON/Props:")
            print(s.string[:200] + "...")
        elif "window.pageData" in s.string:
             print("Found pageData")

# Print all headings to see if titles are there
for h in soup.find_all(['h1', 'h2', 'h3', 'h4']):
    print(h.get_text().strip())

# Look for specific class
print("Film titles?")
titles = soup.select('div[class*="title"], h3[class*="title"], span[class*="title"]')
for t in titles:
    print(t.get_text().strip())
