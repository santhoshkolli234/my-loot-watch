import os, requests
from bs4 import BeautifulSoup

CHANNEL = os.environ["CHANNEL"]
TOPIC = os.environ["TOPIC"]

html = requests.get(f"https://t.me/s/{CHANNEL}", timeout=30).text
soup = BeautifulSoup(html, "html.parser")

posts = []
for m in soup.select("div.tgme_widget_message"):
    pid = int(m["data-post"].split("/")[1])
    t = m.select_one(".tgme_widget_message_text")
    text = t.get_text(" ", strip=True) if t else "New media post"
    posts.append((pid, text))

try:
    last = int(open("last_id.txt").read())
except Exception:
    last = None

if posts:
    newest = max(p[0] for p in posts)
    if last is None:
        last = newest
    for pid, text in sorted(posts):
        if pid > last:
            requests.post(
                f"https://ntfy.sh/{TOPIC}",
                data=text[:500].encode("utf-8"),
                headers={"Click": f"https://t.me/{CHANNEL}/{pid}"},
            )
    open("last_id.txt", "w").write(str(newest))
