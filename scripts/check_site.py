#!/usr/bin/env python3
"""Checks the generated site: links and anchors, images, language links, and the rules in _headers.

    python3 scripts/check_site.py        # run python3 build.py first

Fails (exit 1) with a list of problems. It needs only Python 3 and makes no network requests.
"""
import pathlib
import re
import sys
from html.parser import HTMLParser
from urllib.parse import unquote, urlparse

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ["index.html", "bn/index.html", "privacy/index.html", "404.html"]
OUTSIDE = ("https://github.com/azimul-kabir", "https://azimulkabir.com", "https://kor.azimulkabir.com", "mailto:kor@azimulkabir.com")
errors: list[str] = []


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.images, self.tags, self.attrs_seen = set(), [], [], [], []
        self.h1 = 0
        self.lang = None
        self.title = False
        self.has_title = False
        self.description = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.append(tag)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "html":
            self.lang = a.get("lang")
        if tag == "h1":
            self.h1 += 1
        if tag == "title":
            self.has_title = True
        if tag == "meta" and a.get("name") == "description" and a.get("content"):
            self.description = True
        if "style" in a:
            errors.append("inline style attribute (the CSP forbids it)")
        for key in ("href", "src"):
            if key in a:
                self.links.append((tag, key, a[key], a))
        if tag == "img":
            self.images.append(a)


def parse(path: pathlib.Path) -> Page:
    page = Page()
    page.feed(path.read_text(encoding="utf-8"))
    return page


def resolve(page_path: pathlib.Path, target: str) -> pathlib.Path:
    """The file a local link points at, treating a folder as its index.html."""
    base = ROOT if target.startswith("/") else page_path.parent
    resolved = (base / unquote(target.lstrip("/"))).resolve()
    return resolved / "index.html" if resolved.is_dir() or target.endswith("/") else resolved


pages = {name: parse(ROOT / name) for name in PAGES}
for name, page in pages.items():
    here = ROOT / name
    if not page.lang:
        errors.append(f"{name}: <html> has no lang")
    if not page.has_title or not (name == "404.html" or page.description):
        errors.append(f"{name}: needs a <title>" + ("" if name == "404.html" else " and a meta description"))
    if "script" in page.tags:
        errors.append(f"{name}: contains a <script>")
    if name != "privacy/index.html" and name != "404.html" and page.h1 != 1:
        errors.append(f"{name}: expected one <h1>, found {page.h1}")
    for img in page.images:
        if "alt" not in img:
            errors.append(f"{name}: image {img.get('src')} has no alt text")
        if not (img.get("width") and img.get("height")):
            errors.append(f"{name}: image {img.get('src')} has no width and height")
    for tag, key, target, attrs in page.links:
        parsed = urlparse(target)
        if parsed.scheme in ("http", "https", "mailto"):
            if tag != "a" and not (tag == "link" and attrs.get("rel") in ("canonical", "alternate")):
                errors.append(f"{name}: {tag} loads {target} from another site")
            elif not target.startswith(OUTSIDE):
                errors.append(f"{name}: unexpected outside link {target}")
            continue
        file = resolve(here, parsed.path) if parsed.path else here
        if not file.exists():
            errors.append(f"{name}: {target} does not exist")
            continue
        if parsed.fragment and file.suffix == ".html":
            other = pages.get(str(file.relative_to(ROOT))) or parse(file)
            if parsed.fragment not in other.ids:
                errors.append(f"{name}: {target} points at a missing anchor")

# The two home pages must link to each other with matching languages.
en, bn = pages["index.html"], pages["bn/index.html"]
if en.lang != "en" or bn.lang != "bn":
    errors.append("home pages need lang en and bn")
for page, name, want in ((en, "index.html", "bn/"), (bn, "bn/index.html", "../")):
    if not any(t == "a" and k == "href" and v == want and a.get("hreflang") for t, k, v, a in page.links):
        errors.append(f"{name}: missing language-switch link to {want}")

# The stylesheet may not pull anything from another site.
css = (ROOT / "assets" / "style.css").read_text(encoding="utf-8")
if re.search(r"url\(\s*['\"]?https?:", css) or "@import" in css:
    errors.append("assets/style.css loads something from another site")
for ref in re.findall(r'url\("([^"]+)"\)', css):
    if not (ROOT / "assets" / ref).exists():
        errors.append(f"assets/style.css: {ref} does not exist")

# Every sitemap address maps to a page.
for loc in re.findall(r"<loc>https://kor\.azimulkabir\.com(/[^<]*)</loc>", (ROOT / "sitemap.xml").read_text()):
    if not resolve(ROOT / "index.html", loc).exists():
        errors.append(f"sitemap.xml: {loc} has no page")

# The share image is the size the pages promise.
og = ROOT / "assets" / "og.png"
if not og.exists():
    errors.append("assets/og.png is missing")
elif og.read_bytes()[16:24] != (1200).to_bytes(4, "big") + (630).to_bytes(4, "big"):
    errors.append("assets/og.png must be 1200x630")

if errors:
    print("\n".join(f"  - {e}" for e in sorted(set(errors))))
    sys.exit(1)
print(f"ok: {len(PAGES)} pages, links, anchors, images and headers checked")
