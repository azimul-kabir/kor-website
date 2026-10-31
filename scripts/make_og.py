#!/usr/bin/env python3
"""Draws assets/og.png (1200x630), the picture shown when a page is shared on WhatsApp, Facebook and the like.

    python3 scripts/make_og.py /path/to/raw /path/to/Inter.ttf

raw is the same folder of full-size screenshots that optimize_shots.py reads (raw/en/*.png); the font is any
Inter .ttf (the app bundles one in app/src/main/res/font). Needs Pillow. Latin text only: Pillow cannot shape Bangla.
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


def main(raw: pathlib.Path, font_path: str) -> None:
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
    # Logo: the round badge cropped from a home screenshot (top right of the bar).
    home = Image.open(raw / "en" / "01-home.png").convert("RGB")
    logo = home.crop((920, 103, 1020, 203)).resize((96, 96), Image.LANCZOS)
    mask = Image.new("L", logo.size, 0)
    ImageDraw.Draw(mask).ellipse((0, 0, 96, 96), fill=255)
    canvas.paste(logo, (72, 70), mask)
    draw.text((184, 92), "Kor", font=font(44, 800), fill="white")

    draw.text((72, 210), "Know your", font=font(76, 800), fill="white")
    draw.text((72, 290), "income tax", font=font(76, 800), fill="white")
    draw.text((72, 370), "as you go.", font=font(76, 800), fill=AMBER)
    draw.text((72, 488), "Bangladesh personal income tax.", font=font(28, 500), fill=MINT)
    draw.text((72, 528), "Offline. English and Bangla.", font=font(28, 500), fill=MINT)

    shots = [(raw / "en" / "09-calculator.png", 610, 70, 16), (raw / "en" / "02-home-tiles.png", 740, 34, 0)]
    for path, x, y, tilt in shots:
        body = phone(Image.open(path).convert("RGB"), 520)
        canvas.alpha_composite(body, (x, y + 0))
    # Bottom of the phones runs off the card, as in the hero.
    canvas.convert("RGB").save(ROOT / "assets" / "og.png", optimize=True)
    print("wrote assets/og.png")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    main(pathlib.Path(sys.argv[1]), sys.argv[2])
