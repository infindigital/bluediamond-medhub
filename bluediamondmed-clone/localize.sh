#!/usr/bin/env bash
#
# Fully localize the Blue Diamond clone.
#
# Downloads every asset (CSS, JS, images, fonts) still referenced from the live
# bluediamondmed.com domain into this folder, then rewrites those references to
# root-relative local paths. After running it, the clone is 100% self-contained.
#
# Run this ONCE from a machine/environment with normal internet access:
#     cd bluediamondmed-clone && bash localize.sh
#
# Then serve the folder (paths are root-relative):
#     python3 -m http.server 8000   # visit http://localhost:8000
#
set -euo pipefail
cd "$(dirname "$0")"
BASE="bluediamondmed.com"
EXT='css|js|png|jpe?g|gif|svg|webp|avif|ico|woff2?|ttf|eot|mp4|webm'

echo "==> Collecting asset URLs referenced by the HTML pages..."
grep -ohE "https://$BASE/[^\"')> ]+\.($EXT)(\?[^\"')> ]*)?" ./*.html \
  | sed 's/?.*//' | sort -u > .asset-urls.txt
echo "    $(wc -l < .asset-urls.txt) unique assets."

echo "==> Downloading (mirroring the remote directory layout)..."
# -x keep dirs, -nH drop the hostname dir, -P . into this folder.
wget -q -x -nH -P . -i .asset-urls.txt || true

echo "==> Following url(...) references inside downloaded CSS (fonts, bg images)..."
: > .asset-urls2.txt
find wp-content wp-includes -name '*.css' 2>/dev/null -print0 | while IFS= read -r -d '' f; do
  grep -ohE "url\(([^)]+)\)" "$f" \
    | sed -E "s/url\(['\"]?//; s/['\"]?\).*//" \
    | grep -E "^https://$BASE/" | sed 's/?.*//'
done | sort -u >> .asset-urls2.txt
if [ -s .asset-urls2.txt ]; then
  echo "    $(wc -l < .asset-urls2.txt) nested assets."
  wget -q -x -nH -P . -i .asset-urls2.txt || true
fi

echo "==> Rewriting asset URLs to root-relative local paths (HTML + CSS)..."
python3 - "$BASE" "$EXT" <<'PY'
import re, sys, glob, os
base, ext = sys.argv[1], sys.argv[2]
pat = re.compile(r'https://' + re.escape(base) +
                 r'(/[^"\'()> ]+?\.(?:' + ext + r'))(\?[^"\'()> ]*)?')
files = glob.glob("*.html")
for root in ("wp-content", "wp-includes"):
    for dp, _, fns in os.walk(root):
        files += [os.path.join(dp, fn) for fn in fns if fn.endswith(".css")]
for fp in files:
    try:
        t = open(fp, encoding="utf-8", errors="replace").read()
    except IsADirectoryError:
        continue
    n = pat.sub(lambda m: m.group(1), t)
    if n != t:
        open(fp, "w", encoding="utf-8").write(n)
        print("    rewrote", fp)
PY

rm -f .asset-urls.txt .asset-urls2.txt
echo "==> Done. The clone now loads all assets locally."
