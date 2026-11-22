"""Scan grade/week folders and write lessons.json for the site's index page.

Folder layout:  <grade number>/week<N>/<lesson>.html
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WEEK_RE = re.compile(r"^week[ _-]?(\d+)$", re.I)
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)


def lesson_title(path, fallback):
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            head = f.read(16384)
        m = TITLE_RE.search(head)
        if m and m.group(1).strip():
            return html.unescape(" ".join(m.group(1).split()))
    except OSError:
        pass
    return fallback


def main():
    grades = []
    for g in sorted(os.listdir(ROOT), key=lambda s: (not s.isdigit(), int(s) if s.isdigit() else 0, s)):
        gdir = os.path.join(ROOT, g)
        if not (os.path.isdir(gdir) and g.isdigit()):
            continue
        weeks = []
        for w in os.listdir(gdir):
            m = WEEK_RE.match(w)
            wdir = os.path.join(gdir, w)
            if not (m and os.path.isdir(wdir)):
                continue
            lessons = []
            for f in sorted(os.listdir(wdir)):
                if f.lower().endswith((".html", ".htm")):
                    name = os.path.splitext(f)[0].replace("-", " ").replace("_", " ").title()
                    lessons.append({"title": lesson_title(os.path.join(wdir, f), name), "file": f"{g}/{w}/{f}"})
            weeks.append({"week": int(m.group(1)), "lessons": lessons})
        weeks.sort(key=lambda x: x["week"])
        grades.append({"grade": int(g), "weeks": weeks})
    out = os.path.join(ROOT, "lessons.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"grades": grades}, f, ensure_ascii=False, indent=2)
    print(f"Wrote {out}: {sum(len(w['lessons']) for g in grades for w in g['weeks'])} lessons")


if __name__ == "__main__":
    main()
