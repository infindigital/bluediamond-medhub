#!/usr/bin/env python3
"""Build the static Blue Diamond mirror from raw fetched HTML.

Phase 1: copy rendered HTML into the clone folder, rewrite internal page
navigation to local .html files, keep all asset (css/js/img/font) URLs
pointing at the live CDN so the pages render identically.
"""
import re, glob, os

SRC = "site-raw"
OUT = "bluediamondmed-clone"
BASE = "https://bluediamondmed.com"

# slug (no slashes) -> local file
PAGES = {
    "": "index.html",
    "about-us": "about-us.html",
    "services": "services.html",
    "healthcare-staffing-services-page": "healthcare-staffing-services-page.html",
    "school-staffing": "school-staffing.html",
    "healthcare-professionals": "healthcare-professionals.html",
    "teachers-substitute-educators": "teachers-substitute-educators.html",
    "cpr-emergency-training-certification": "cpr-emergency-training-certification.html",
    "teach-in-the-u-s-a-with-blue-diamond-school-staffing": "teach-in-the-u-s-a-with-blue-diamond-school-staffing.html",
    "healthcare-staffing": "healthcare-staffing.html",
    "teaching-jobs": "teaching-jobs.html",
    "contact-us": "contact-us.html",
}

os.makedirs(OUT, exist_ok=True)


def rewrite_nav(html):
    # href="https://bluediamondmed.com/slug/" or without trailing slash -> local file
    def repl(m):
        quote = m.group(1)
        slug = m.group(2).strip("/")
        if slug in PAGES:
            return f'href={quote}{PAGES[slug]}{quote}'
        return m.group(0)  # leave other internal links absolute

    # match href="https://bluediamondmed.com/....." (page-like, no file extension, no query)
    pattern = r'href=(["\'])' + re.escape(BASE) + r'/([a-z0-9\-/]*)/?\1'
    html = re.sub(pattern, repl, html)
    return html


def main():
    count = 0
    for f in sorted(glob.glob(f"{SRC}/*.html")):
        name = os.path.basename(f)
        html = open(f, encoding="utf-8", errors="replace").read()
        html = rewrite_nav(html)
        open(os.path.join(OUT, name), "w", encoding="utf-8").write(html)
        count += 1
        print("built", name)
    print(f"\n{count} pages written to {OUT}/")


if __name__ == "__main__":
    main()
