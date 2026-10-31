#!/usr/bin/env python3
"""Builds the Kor website from content.py, data/privacy.json and assets/shots/manifest.json.

    python3 build.py        # needs only Python 3

Writes index.html (English), bn/index.html (Bangla), privacy/index.html, 404.html, sitemap.xml and
robots.txt. Commit the generated files: they are what gets published, and CI fails if they are stale.
Everything is plain HTML and CSS: no JavaScript, no inline styles, no requests to other sites.
"""
import html
import json
import pathlib

import content as c

ROOT = pathlib.Path(__file__).resolve().parent
SHOTS = json.loads((ROOT / "assets" / "shots" / "manifest.json").read_text(encoding="utf-8"))
PRIVACY = json.loads((ROOT / "data" / "privacy.json").read_text(encoding="utf-8"))


def e(text: str) -> str:
    return html.escape(text, quote=True)


def same_shape(a, b, path="content"):
    """Fails if English and Bangla differ in keys or list lengths, so the pages cannot drift apart."""
    if isinstance(a, dict):
        if not isinstance(b, dict) or a.keys() != b.keys():
            raise SystemExit(f"{path}: English and Bangla have different keys")
        for key in a:
            same_shape(a[key], b[key], f"{path}.{key}")
    elif isinstance(a, list):
        if not isinstance(b, list) or len(a) != len(b):
            raise SystemExit(f"{path}: English and Bangla have different numbers of items")
        for i, (x, y) in enumerate(zip(a, b)):
            same_shape(x, y, f"{path}[{i}]")


same_shape(c.EN, c.BN)
if len(PRIVACY["en"]["sections"]) != len(PRIVACY["bn"]["sections"]):
    raise SystemExit("data/privacy.json: English and Bangla sections differ")


def img(lang: str, name: str, alt: str, up: str, eager: bool = False) -> str:
    size = SHOTS[name]
    loading = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (
        f'<img src="{up}assets/shots/{lang}/{name}.webp" width="{size["width"]}" height="{size["height"]}" '
        f'alt="{e(alt)}" {loading} decoding="async">'
    )


def header(t, up: str, home: str, other: str, privacy: str, github: bool = True) -> str:
    n = t["nav"]
    links = (
        f'<a class="hide-small" href="{home}#features">{e(n["features"])}</a>'
        f'<a class="hide-small" href="{home}#screens">{e(n["screens"])}</a>'
        f'<a class="hide-small" href="{home}#privacy">{e(n["privacy"])}</a>'
        f'<a class="hide-small" href="{home}#status">{e(n["status"])}</a>'
        f'<a class="hide-small" href="{c.GITHUB}">{e(n["github"])}</a>'
    )
    return (
        f'<a class="skip" href="#main">{e(t["skip"])}</a>'
        f'<header class="bar"><div class="wrap">'
        f'<a class="brand" href="{home}"><img src="{up}assets/logo.svg" width="40" height="40" alt="">{e(t["name"])}</a>'
        f'<nav class="nav" aria-label="Main">{links}'
        f'<a class="lang" href="{other}" lang="{"bn" if t["lang"] == "en" else "en"}" hreflang="{"bn" if t["lang"] == "en" else "en"}" '
        f'aria-label="{e(t["switch_label"])}">{e(t["switch_to"])}</a></nav></div></header>'
    )


def footer(t, privacy: str) -> str:
    f = t["footer"]
    return (
        '<footer><div class="wrap foot">'
        f'<p>{e(f["disclaimer"])}</p>'
        f'<div class="links"><a href="{c.GITHUB}">{e(f["source"])}</a><a href="{privacy}">{e(f["privacy"])}</a>'
        f'<a href="mailto:{c.EMAIL}">{e(f["contact"])}: {c.EMAIL}</a>'
        f'<a href="{c.DEVELOPER}">{e(f["developer"])}</a></div>'
        f'<p>{e(f["made"])}. {e(f["licence"])}</p>'
        '</div></footer>'
    )


def head(t, url: str, alternates: dict, up: str, og_locale: str) -> str:
    alts = "".join(f'<link rel="alternate" hreflang="{k}" href="{v}">' for k, v in alternates.items())
    return (
        '<meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<title>{e(t["title"])}</title>'
        f'<meta name="description" content="{e(t["description"])}">'
        '<meta name="color-scheme" content="light dark">'
        '<meta name="theme-color" content="#006a4e">'
        f'<link rel="canonical" href="{url}">{alts}'
        f'<link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">'
        '<meta property="og:type" content="website">'
        f'<meta property="og:title" content="{e(t["title"])}">'
        f'<meta property="og:description" content="{e(t["description"])}">'
        f'<meta property="og:url" content="{url}">'
        f'<meta property="og:image" content="{c.SITE}/assets/og.png">'
        '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
        f'<meta property="og:locale" content="{og_locale}">'
        '<meta name="twitter:card" content="summary_large_image">'
        f'<link rel="stylesheet" href="{up}assets/style.css">'
    )


def home(t, lang: str) -> str:
    up = "" if lang == "en" else "../"
    home_href = "./" if lang == "en" else "./"
    other = "bn/" if lang == "en" else "../"
    privacy = f"{up}privacy/" + ("" if lang == "en" else "#bn")
    url = c.SITE + ("/" if lang == "en" else "/bn/")
    h, g, f, s, p, st = t["hero"], t["glance"], t["features"], t["screens"], t["privacy"], t["status"]

    stage = "".join(
        f'<div class="phone p-{pos}">{img(lang, name, alt, up, eager=True)}</div>'
        for pos, name, alt in zip(("left", "mid", "right"), c.HERO_SHOTS, s["hero_alts"])
    )
    chips = "".join(f"<li>{e(x)}</li>" for x in h["chips"])
    glance_points = "".join(f"<li>{e(x)}</li>" for x in g["points"])
    cards = "".join(f'<article class="card"><h3>{e(i["title"])}</h3><p>{e(i["body"])}</p></article>' for i in f["items"])
    figures = "".join(
        f'<figure class="shot"><div class="phone">{img(lang, name, item["alt"], up)}</div>'
        f'<figcaption>{e(item["title"])}</figcaption></figure>'
        for name, item in zip(c.GALLERY, s["items"])
    )
    priv_points = "".join(f"<li>{e(x)}</li>" for x in p["points"])
    works = "".join(f"<li>{e(x)}</li>" for x in st["works"])
    later = "".join(f"<li>{e(x)}</li>" for x in st["later"])

    return (
        f'<!doctype html><html lang="{lang}"><head>'
        + head(t, url, {"en": c.SITE + "/", "bn": c.SITE + "/bn/", "x-default": c.SITE + "/"}, up, "en_BD" if lang == "en" else "bn_BD")
        + "</head><body>"
        + header(t, up, home_href, other, privacy)
        + '<main id="main">'
        '<section class="hero" aria-labelledby="top"><div class="wrap">'
        f'<div class="hero-text"><p class="eyebrow">{e(h["eyebrow"])}</p><h1 id="top">{e(h["title"])}</h1>'
        f'<p class="lead">{e(h["lead"])}</p>'
        f'<div class="cta"><a class="btn btn-primary" href="{c.GITHUB}">{e(h["cta"])}</a>'
        f'<a class="btn btn-ghost" href="#features">{e(h["cta2"])}</a></div>'
        f'<p class="status-note">{e(h["status"])}</p><ul class="chips">{chips}</ul></div>'
        f'<div class="stage">{stage}</div></div></section>'
        '<section class="alt" aria-labelledby="glance"><div class="wrap split">'
        f'<div><h2 id="glance">{e(g["title"])}</h2><p class="sub">{e(g["body"])}</p><ul class="ticks">{glance_points}</ul></div>'
        f'<div class="phone">{img(lang, "01-home", s["items"][0]["alt"], up)}</div></div></section>'
        f'<section id="features" aria-labelledby="features-h"><div class="wrap"><h2 id="features-h">{e(f["title"])}</h2>'
        f'<div class="grid">{cards}</div></div></section>'
        f'<section id="screens" class="alt" aria-labelledby="screens-h"><div class="wrap"><h2 id="screens-h">{e(s["title"])}</h2>'
        f'<div class="shots">{figures}</div><p class="fine">{e(s["note"])}</p></div></section>'
        f'<section id="privacy" class="band" aria-labelledby="privacy-h"><div class="wrap band-grid">'
        f'<div><h2 id="privacy-h">{e(p["title"])}</h2><p class="sub">{e(p["body"])}</p>'
        f'<p><a href="{privacy}">{e(p["link"])}</a></p></div><ul class="ticks">{priv_points}</ul></div></section>'
        f'<section id="status" aria-labelledby="status-h"><div class="wrap"><h2 id="status-h">{e(st["title"])}</h2>'
        f'<p class="sub">{e(st["intro"])}</p><div class="two">'
        f'<div class="card"><h3>{e(st["works_title"])}</h3><ul>{works}</ul></div>'
        f'<div class="card later"><h3>{e(st["later_title"])}</h3><ul>{later}</ul>'
        f'<p><a href="{c.GITHUB}/issues">{e(st["link"])}</a></p></div></div></div></section>'
        "</main>" + footer(t, privacy) + "</body></html>"
    )


def privacy_page() -> str:
    t = c.EN
    sections = ""
    for lang, wrap_id in (("en", "en"), ("bn", "bn")):
        d = PRIVACY[lang]
        body = "".join(f"<h2>{e(s['title'])}</h2><p>{e(s['body'])}</p>" for s in d["sections"])
        sections += (
            f'<article class="doc" id="{wrap_id}" lang="{lang}"><h1>{e(d["title"])}</h1>'
            f'<p class="updated">{e(d["updated"])}</p><p>{e(d["intro"])}</p>{body}'
            f'<p><a href="mailto:{c.EMAIL}">{c.EMAIL}</a></p></article>'
            + ("<hr>" if lang == "en" else "")
        )
    return (
        '<!doctype html><html lang="en"><head>'
        + head(
            {"title": c.EN["privacy_page"]["title"], "description": PRIVACY["en"]["intro"]},
            c.SITE + "/privacy/",
            {},
            "../",
            "en_BD",
        )
        + '</head><body><div class="page-head">'
        + header(t, "../", "../", "../bn/", "./")
        + '</div><main id="main" class="page"><div class="wrap">'
        + f'<p><a href="../">{e(c.EN["privacy_page"]["back"])}</a> · <a href="#bn" lang="bn">বাংলায় পড়ুন</a></p>'
        + sections
        + "</div></main>"
        + footer(t, "./")
        + "</body></html>"
    )


def not_found() -> str:
    t, n = c.EN, c.EN["notfound"]
    # A 404 can be served for any path, so every link here is absolute.
    return (
        '<!doctype html><html lang="en"><head>'
        '<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<title>{e(n["title"])} · Kor</title><meta name="robots" content="noindex">'
        '<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/style.css">'
        '</head><body><div class="page-head">'
        + header(t, "/", "/", "/bn/", "/privacy/")
        + f'</div><main id="main" class="page"><div class="wrap doc"><h1>{e(n["title"])}</h1><p>{e(n["body"])}</p>'
        f'<p><a class="btn btn-primary" href="/">{e(n["link"])}</a></p></div></main>'
        + footer(t, "/privacy/")
        + "</body></html>"
    )


def write(path: str, text: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")


write("index.html", home(c.EN, "en"))
write("bn/index.html", home(c.BN, "bn"))
write("privacy/index.html", privacy_page())
write("404.html", not_found())
write(
    "sitemap.xml",
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
    'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    + "".join(
        f"  <url><loc>{c.SITE}{path}</loc>"
        + (
            f'<xhtml:link rel="alternate" hreflang="en" href="{c.SITE}/"/>'
            f'<xhtml:link rel="alternate" hreflang="bn" href="{c.SITE}/bn/"/>'
            if path in ("/", "/bn/")
            else ""
        )
        + "</url>\n"
        for path in ("/", "/bn/", "/privacy/")
    )
    + "</urlset>\n",
)
write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {c.SITE}/sitemap.xml\n")
print("built index.html, bn/index.html, privacy/index.html, 404.html, sitemap.xml, robots.txt")
