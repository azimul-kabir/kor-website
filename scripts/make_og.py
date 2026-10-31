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
    # Logo: the round badge cropped from a home screenshot (top right of the bar). Without it the text moves up.
    dy = 0
    if logo:
        home = Image.open(raw / "en" / "01-home.png").convert("RGB")
        badge = home.crop((920, 103, 1020, 203)).resize((96, 96), Image.LANCZOS)
        # The mask sits a little inside the badge so the light pixels at its edge are left out, and a thin light
        # ring, like the one on the app's About screen, shows the circle against the same green.
        mask = Image.new("L", badge.size, 0)
        ImageDraw.Draw(mask).ellipse((3, 3, 93, 93), fill=255)
        canvas.paste(badge, (72, 70), mask)
        ring = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        ImageDraw.Draw(ring).ellipse((72, 70, 72 + 96, 70 + 96), outline=(255, 255, 255, 140), width=3)
        canvas.alpha_composite(ring)
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
