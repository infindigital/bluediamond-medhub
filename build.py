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


def fix_lazy_backgrounds(html):
    """Elementor lazy-loads section background images: an injected <style> sets
    `background-image:none !important` on parent containers until its JS adds the
    `e-lazyloaded` class on scroll. In a static snapshot that suppresses most
    section backgrounds. Remove the gating <style> and mark every container as
    loaded so all backgrounds render immediately."""
    # Drop the injected style block that suppresses lazy backgrounds.
    html = re.sub(
        r'<style>[^<]*background-image:\s*none\s*!important[^<]*</style>',
        '', html, flags=re.DOTALL)
    # Ensure every Elementor container (.e-con) also carries .e-lazyloaded.
    def add_class(m):
        cls = m.group(1)
        if 'e-con' in cls and 'e-lazyloaded' not in cls:
            cls = cls + ' e-lazyloaded'
        return f'class="{cls}"'
    html = re.sub(r'class="([^"]*\be-con\b[^"]*)"', add_class, html)
    # Elementor hides entrance-animated elements with `elementor-invisible`
    # (opacity:0) until its JS runs. In a static mirror that can leave images
    # and content blank, so strip the class to show everything immediately.
    html = re.sub(r'\s*\belementor-invisible\b', '', html)
    return html


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
        html = fix_lazy_backgrounds(html)
        html = rewrite_nav(html)
        open(os.path.join(OUT, name), "w", encoding="utf-8").write(html)
        count += 1
        print("built", name)
    print(f"\n{count} pages written to {OUT}/")


if __name__ == "__main__":
    main()
