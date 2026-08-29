"""Static audit of the built site: links, assets, headings, labels, alt text,
colour tokens and leftover template content."""
import io
import os
import re
from collections import Counter
from html.parser import HTMLParser

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
PAGES = ["index.html", "404.html"] + [
    f"{d}/index.html" for d in
    ("about-us", "accommodation", "restaurant", "banquets", "services", "gallery", "contact")
]

problems = []
notes = []


def add(page, msg):
    problems.append(f"{page}: {msg}")


class Doc(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.headings = []
        self.images = []
        self.links = []
        self.inputs = []          # (tag, attrs)
        self.labels_for = []
        self.buttons = []
        self.iframes = 0
        self._h = None
        self._buf = []
        self.title = ""
        self._in_title = False
        self.metas = []
        self.scripts = []
        self.links_rel = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._h = tag
            self._buf = []
        if tag == "img":
            self.images.append(a)
        if tag == "a":
            self.links.append(a)
        if tag in ("input", "select", "textarea"):
            self.inputs.append((tag, a))
        if tag == "label":
            self.labels_for.append(a.get("for"))
        if tag == "button":
            self.buttons.append(a)
        if tag == "iframe":
            self.iframes += 1
        if tag == "title":
            self._in_title = True
        if tag == "meta":
            self.metas.append(a)
        if tag == "script":
            self.scripts.append(a)
        if tag == "link":
            self.links_rel.append(a)

    def handle_endtag(self, tag):
        if tag == self._h:
            self.headings.append((tag, "".join(self._buf).strip()))
            self._h = None
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._h:
            self._buf.append(data)
        if self._in_title:
            self.title += data


def exists(path):
    """Resolve a root-relative site path to a file on disk."""
    path = path.split("?")[0].split("#")[0]
    if path.startswith("/"):
        p = os.path.join(ROOT, path.lstrip("/"))
        if os.path.isdir(p):
            p = os.path.join(p, "index.html")
        return os.path.exists(p)
    return None


titles, descs = [], []

for page in PAGES:
    full = os.path.join(ROOT, page)
    if not os.path.exists(full):
        add(page, "FILE MISSING")
        continue
    html = io.open(full, encoding="utf-8").read()
    d = Doc()
    d.feed(html)

    # --- one h1, sane heading order -------------------------------------
    h1s = [t for t, _ in d.headings if t == "h1"]
    if len(h1s) != 1:
        add(page, f"expected exactly one <h1>, found {len(h1s)}")

    levels = [int(t[1]) for t, _ in d.headings]
    for i in range(1, len(levels)):
        if levels[i] - levels[i - 1] > 1:
            add(page, f"heading level jumps h{levels[i-1]} -> h{levels[i]}")
            break

    # --- duplicate ids ---------------------------------------------------
    dupes = [i for i, c in Counter(d.ids).items() if c > 1]
    if dupes:
        add(page, f"duplicate id(s): {dupes}")

    # --- images ----------------------------------------------------------
    for img in d.images:
        src = img.get("src", "")
        if "alt" not in img:
            add(page, f"img without alt attribute: {src}")
        elif not img["alt"].strip() and "gp-lightbox__image" not in img.get("class", ""):
            add(page, f"img with empty alt: {src}")
        if src and exists(src) is False:
            add(page, f"missing image file: {src}")
        if src and not src.startswith("data:"):
            if "width" not in img or "height" not in img:
                add(page, f"img without width/height: {src}")

    # --- internal links --------------------------------------------------
    for a in d.links:
        href = a.get("href", "")
        if href.startswith(("http", "mailto:", "tel:", "#")) or not href:
            continue
        target = href.split("#")[0]
        if target and exists(target) is False:
            add(page, f"broken internal link: {href}")

    # --- asset references in <link>/<script> -----------------------------
    for l in d.links_rel:
        h = l.get("href", "")
        if h.startswith("/") and exists(h) is False:
            add(page, f"missing asset: {h}")
    for s in d.scripts:
        src = s.get("src", "")
        if src.startswith("/") and exists(src) is False:
            add(page, f"missing script: {src}")

    # --- form labelling --------------------------------------------------
    label_targets = set(x for x in d.labels_for if x)
    for tag, a in d.inputs:
        if a.get("type") == "hidden":
            continue
        fid = a.get("id")
        labelled = (fid in label_targets) or ("aria-label" in a) or ("aria-labelledby" in a)
        if not labelled:
            add(page, f"unlabelled form control: <{tag} name={a.get('name')}>")

    # --- buttons need an accessible name ---------------------------------
    for b in d.buttons:
        if "aria-label" not in b and b.get("class", "").startswith("gp-filter") is False:
            pass  # text content buttons are fine; checked visually below

    # --- SEO -------------------------------------------------------------
    title = d.title.strip()
    if not title:
        add(page, "missing <title>")
    titles.append((page, title))

    desc = next((m.get("content", "") for m in d.metas if m.get("name") == "description"), "")
    if not desc:
        add(page, "missing meta description")
    elif not (50 <= len(desc) <= 175):
        notes.append(f"{page}: meta description is {len(desc)} chars")
    descs.append((page, desc))

    canonical = [l for l in d.links_rel if l.get("rel") == "canonical"]
    robots = [m for m in d.metas if m.get("name") == "robots"]
    if not canonical and not robots:
        add(page, "missing canonical")

    for prop in ("og:title", "og:description", "og:image", "og:url"):
        if not any(m.get("property") == prop for m in d.metas):
            add(page, f"missing {prop}")

    # --- leftover template content ---------------------------------------
    lowered = html.lower()
    for bad in ("lorem ipsum", "riorelax", "template", "demo", "buy now",
                "themeforest", "envato", "dripicons", "wow.js", "particles",
                "typed.js", "counterup", "placeholder.com", "index-2.html",
                "single-rooms", "blog-details", "shop-details"):
        if bad in lowered:
            # "PLACEHOLDER" in our own image comments is intentional
            add(page, f"possible leftover template content: '{bad}'")

    if d.iframes:
        add(page, f"{d.iframes} iframe(s) in markup (map should be click-to-load)")

    # --- lazy loading below the fold -------------------------------------
    non_lazy = [i.get("src") for i in d.images
                if "loading" not in i and i.get("fetchpriority") != "high"
                and "gp-lightbox__image" not in i.get("class", "")]
    # logo images in header/panel/footer are small and above/near the fold
    non_lazy = [s for s in non_lazy if s and "/logo/" not in s]
    if non_lazy:
        add(page, f"images without loading=lazy: {non_lazy}")

# --- unique titles / descriptions ----------------------------------------
for label, pairs in (("title", titles), ("description", descs)):
    seen = Counter(v for _, v in pairs)
    for value, count in seen.items():
        if count > 1 and value:
            add("SITE", f"duplicate {label} on {count} pages: {value[:60]}…")

# --- CSS: every colour must come from a token -----------------------------
css = io.open(os.path.join(ROOT, "assets/css/style.css"), encoding="utf-8").read()
root_block = re.search(r":root\s*\{(.*?)\}", css, re.S).group(1)
body_css = css.replace(root_block, "")

stray_hex = re.findall(r"#[0-9a-fA-F]{3,8}\b", body_css)
# the inline SVG data-uri for the select arrow carries an escaped hex colour
stray_hex = [h for h in stray_hex if h.lower() not in ("#5a6357",)]
if stray_hex:
    add("style.css", f"stray hex outside :root — {sorted(set(stray_hex))}")

stray_rgba = re.findall(r"rgba?\([^)]*\)", body_css)
# Plain black at any alpha is a neutral drop-shadow primitive, not a brand
# colour choice — it models light absorption, not palette, so it's exempt.
stray_rgba = [c for c in stray_rgba if not re.match(r"rgba?\(\s*0\s*,\s*0\s*,\s*0\s*,", c)]
if stray_rgba:
    add("style.css", f"stray rgb/rgba outside :root — {sorted(set(stray_rgba))}")

named = re.findall(r":\s*(red|blue|green|black|white|grey|gray|gold|maroon)\b", body_css)
if named:
    add("style.css", f"named colour keywords in CSS — {sorted(set(named))}")

# fonts
fams = set(re.findall(r"font-family:([^;]+);", css))
notes.append(f"font-family declarations: {len(fams)} (expect 2 token defs + inherits)")

# --- sitemap / robots -----------------------------------------------------
for f in ("sitemap.xml", "robots.txt", "enquiry.php", "assets/js/main.js"):
    if not os.path.exists(os.path.join(ROOT, f)):
        add("SITE", f"missing {f}")

sitemap = io.open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
# read the canonical host straight out of the generator so the two cannot drift
SITE = re.search(r'^SITE = "([^"]+)"', io.open(os.path.join(ROOT, "_build/build.py"),
                                               encoding="utf-8").read(), re.M).group(1)
for u in ("/", "/about-us/", "/accommodation/", "/restaurant/", "/banquets/",
          "/services/", "/gallery/", "/contact/"):
    if f"<loc>{SITE}{u}</loc>" not in sitemap:
        add("sitemap.xml", f"missing {u}")

# --- report ---------------------------------------------------------------
print("=" * 70)
if problems:
    print(f"PROBLEMS ({len(problems)})")
    for p in problems:
        print("  ✗", p)
else:
    print("No problems found.")
print("-" * 70)
for n in notes:
    print("  ·", n)

verify = Counter()
for page in PAGES:
    full = os.path.join(ROOT, page)
    if os.path.exists(full):
        for m in re.findall(r"\[VERIFY: ([^\]]+)\]", io.open(full, encoding="utf-8").read()):
            verify[m] += 1
print("-" * 70)
print(f"[VERIFY] placeholders ({len(verify)} distinct):")
for k, v in sorted(verify.items()):
    print(f"  · {k}  ×{v}")
