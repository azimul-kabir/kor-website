#!/usr/bin/env python3
"""Turns raw emulator screenshots into the small WebP files the site serves.

    python3 scripts/optimize_shots.py /path/to/raw      # raw/en/*.png and raw/bn/*.png, 1080x2340

Writes assets/shots/{en,bn}/<name>.webp at 540 px wide and assets/shots/manifest.json with each size, which
build.py puts on every <img> so pages never jump while loading. Needs Pillow (pip install pillow).
"""
import json
import pathlib
import sys

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "shots"
WIDTH = 540
# The screens the site uses; the rest of a capture run is left out.
KEEP = ["01-home", "02-home-tiles", "04-tax-detail", "06-wealth-assets", "07-ereturn", "09-calculator"]


def main(raw: pathlib.Path) -> None:
    manifest = {}
    for lang in ("en", "bn"):
        (OUT / lang).mkdir(parents=True, exist_ok=True)
        for name in KEEP:
            source = raw / lang / f"{name}.png"
            if not source.exists():
                raise SystemExit(f"missing {source}")
            image = Image.open(source).convert("RGB")
            height = round(image.height * WIDTH / image.width)
            image = image.resize((WIDTH, height), Image.LANCZOS)
            target = OUT / lang / f"{name}.webp"
            image.save(target, "WEBP", quality=82, method=6)
            manifest.setdefault(name, {"width": WIDTH, "height": height})
            if manifest[name]["height"] != height:
                raise SystemExit(f"{name}: English and Bangla captures differ in size")
            print(f"{lang}/{name}.webp  {target.stat().st_size // 1024} KB")
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    main(pathlib.Path(sys.argv[1]))
