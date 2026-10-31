#!/usr/bin/env python3
"""Draws assets/og.png (1200x630), the picture shown when a page is shared on WhatsApp, Facebook and the like.

    python3 scripts/make_og.py /path/to/raw /path/to/Inter.ttf [--no-logo] [--out path.png]

raw is the same folder of full-size screenshots that optimize_shots.py reads (raw/en/*.png); the font is any
Inter .ttf (the app bundles one in app/src/main/res/font). Needs Pillow. Latin text only: Pillow cannot shape Bangla.

The logo already says "kor.", so no "Kor" text is drawn beside it. --no-logo leaves the logo out too, for a README that
shows the logo above the banner; --out writes somewhere other than assets/og.png.
"""
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
W, H = 1200, 630
GREEN, DEEP, MINT, AMBER = (0, 106, 78), (0, 56, 42), (200, 240, 221), (251, 191, 119)


def rounded(image: Image.Image, radius: int) -> Image.Image:
    mask = Image.new("L", image.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, *image.size), radius, fill=255)
    image = image.convert("RGBA")
    image.putalpha(mask)
    return image


def render_logo(size: int, ring: bool = False) -> Image.Image:
    """The Kor logo drawn from its shapes (assets/logo.svg), at 8x and scaled down, so it is sharp at any size.

    Pillow cannot read SVG, so the shapes are drawn here with the same numbers as the file: a green disc, the
    white "kor" strokes and the amber dot, scaled 1.32 about the centre.
    """
    ss = 8
    big = size * ss
    f = big / 108
    k = 1.32  # the logo's own scale inside the 108-unit disc

    def pt(x, y):
        return ((k * (x - 54) + 54 - 1.32) * f, (k * (y - 54) + 54 + 3.96) * f)

    img = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    inset = 3 * ss if ring else 0  # leave room for the ring around the disc
    d.ellipse((inset, inset, big - 1 - inset, big - 1 - inset), fill=(0, 106, 78, 255))
    if ring:
        # A thin light ring, like the one on the app's About screen, shows the circle against the same green.
        d.ellipse((0, 0, big - 1, big - 1), outline=(255, 255, 255, 150), width=3 * ss)
    width = 6 * k * f
    r = width / 2

    def dot(x, y, radius, fill):
        d.ellipse((x - radius, y - radius, x + radius, y + radius), fill=fill)

    def stroke(points):
        for a, b in zip(points, points[1:]):
            d.line((*pt(*a), *pt(*b)), fill="white", width=round(width))
        for p in (points[0], points[-1]):
            dot(*pt(*p), r, "white")

    stroke([(26, 36), (26, 66)])  # k: stem
    stroke([(41, 46), (26, 59)])  # k: upper arm
    stroke([(32, 54), (42, 66)])  # k: leg
    cx, cy = pt(56, 56)  # o
    d.ellipse((cx - 10 * k * f - r, cy - 10 * k * f - r, cx + 10 * k * f + r, cy + 10 * k * f + r), fill="white")
    d.ellipse((cx - 10 * k * f + r, cy - 10 * k * f + r, cx + 10 * k * f - r, cy + 10 * k * f - r), fill=(0, 106, 78, 255))
    stroke([(74, 66), (74, 46)])  # r: stem
    # r: the curved arm, a quadratic curve from (74,56) through (75,46) to (82,46)
    curve = [((1 - t) ** 2 * 74 + 2 * (1 - t) * t * 75 + t * t * 82, (1 - t) ** 2 * 56 + 2 * (1 - t) * t * 46 + t * t * 46) for t in [i / 40 for i in range(41)]]
    for x, y in curve:  # a dot at every sample: short thick line segments leave gaps
        dot(*pt(x, y), r, "white")
    dot(*pt(84, 63), 3.5 * k * f, (251, 191, 119, 255))  # the dot
    return img.resize((size, size), Image.LANCZOS)


def phone(shot: Image.Image, height: int) -> Image.Image:
    width = round(shot.width * height / shot.height)
    screen = rounded(shot.resize((width, height), Image.LANCZOS), 30)
    pad = 9
    body = Image.new("RGBA", (width + 2 * pad, height + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(body).rounded_rectangle((0, 0, *body.size), 38, fill=(12, 18, 15, 255))
    body.alpha_composite(screen, (pad, pad))
    return body


def main(raw: pathlib.Path, font_path: str, logo: bool = True, out: pathlib.Path = ROOT / "assets" / "og.png") -> None:
    # Vertical gradient, light green at the top right to deep green at the bottom left.
    canvas = Image.new("RGB", (W, H), GREEN)
    px = canvas.load()
    for y in range(H):
        for x in range(W):
            t = min(1.0, max(0.0, (y / H) * 0.65 + ((W - x) / W) * -0.25 + 0.2))
            px[x, y] = tuple(round(GREEN[i] + (DEEP[i] - GREEN[i]) * t) for i in range(3))
    canvas = canvas.convert("RGBA")

    def font(size: int, weight: int) -> ImageFont.FreeTypeFont:
        f = ImageFont.truetype(font_path, size)
        try:
            f.set_variation_by_axes([weight])
        except Exception:
            pass
        return f

    draw = ImageDraw.Draw(canvas)
    # Logo: drawn from its vector shapes, so it is sharp. Without it the text moves up.
    dy = 0
    if logo:
        canvas.alpha_composite(render_logo(112, ring=True), (66, 56))
        draw = ImageDraw.Draw(canvas)
    else:
        dy = -50

    draw.text((72, 210 + dy), "Know your", font=font(76, 800), fill="white")
    draw.text((72, 290 + dy), "income tax", font=font(76, 800), fill="white")
    draw.text((72, 370 + dy), "as you go.", font=font(76, 800), fill=AMBER)
    draw.text((72, 488 + dy), "Bangladesh personal income tax.", font=font(28, 500), fill=MINT)
    draw.text((72, 528 + dy), "Offline. English and Bangla.", font=font(28, 500), fill=MINT)

    shots = [(raw / "en" / "09-calculator.png", 610, 70, 16), (raw / "en" / "02-home-tiles.png", 740, 34, 0)]
    for path, x, y, tilt in shots:
        body = phone(Image.open(path).convert("RGB"), 520)
        canvas.alpha_composite(body, (x, y + 0))
    # Bottom of the phones runs off the card, as in the hero.
    canvas.convert("RGB").save(out, optimize=True)
    print(f"wrote {out}")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    out = ROOT / "assets" / "og.png"
    if "--out" in sys.argv:
        out = pathlib.Path(sys.argv[sys.argv.index("--out") + 1])
        args = [a for a in args if a != str(out)]
    if len(args) != 2:
        raise SystemExit(__doc__)
    main(pathlib.Path(args[0]), args[1], logo="--no-logo" not in sys.argv, out=out)
