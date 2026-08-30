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

IMG_EXT = "png|jpe?g|gif|svg|webp|avif|ico"
IMG_RE = re.compile(
    r'https://bluediamondmed\.com/([^"\'\s,)]+?\.(?:' + IMG_EXT + r'))(\?[^"\'\s,)]*)?')
# Collected local image paths (relative, query stripped) -> a live source URL.
IMAGES = {}


def localize_images(html):
    """Point every <img>/srcset/favicon image at a local relative path (query
    stripped) and record where it came from, so the folders can be created and
    the user can drop the real files in."""
    def repl(m):
        path = m.group(1)
        IMAGES[path] = "https://bluediamondmed.com/" + path
        return path
    return IMG_RE.sub(repl, html)


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
        html = localize_images(html)
        html = rewrite_nav(html)
        open(os.path.join(OUT, name), "w", encoding="utf-8").write(html)
        count += 1
        print("built", name)

    # Create the image folder tree (with .gitkeep so empty dirs are tracked)
    # and a manifest listing each expected file and its live source URL.
    dirs = sorted({os.path.dirname(p) for p in IMAGES})
    for d in dirs:
        full = os.path.join(OUT, d)
        os.makedirs(full, exist_ok=True)
        open(os.path.join(full, ".gitkeep"), "a").close()
    manifest = os.path.join(OUT, "IMAGES-NEEDED.txt")
    with open(manifest, "w") as fh:
        fh.write("# Images referenced by the clone. Save each file at the local\n"
                 "# path on the left; download it from the URL on the right.\n"
                 f"# {len(IMAGES)} files.\n\n")
        for p in sorted(IMAGES):
            fh.write(f"{p}\t{IMAGES[p]}\n")

    print(f"\n{count} pages written to {OUT}/")
    print(f"{len(IMAGES)} image paths across {len(dirs)} folders; manifest: {manifest}")


if __name__ == "__main__":
    main()
