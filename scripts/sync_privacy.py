#!/usr/bin/env python3
"""Copies the privacy policy from the Kor app's own string resources into data/privacy.json.

    python3 scripts/sync_privacy.py ../kor      # then: python3 build.py

The policy belongs to the app (Settings, then Privacy policy; PRIVACY.md carries the English text), so it is
written there and copied here, in English and Bangla. Never edit data/privacy.json or privacy/ by hand.
"""
import json
import pathlib
import re
import sys


def load(res: pathlib.Path, folder: str) -> dict:
    text = (res / folder / "strings.xml").read_text(encoding="utf-8")
    strings = {
        m.group(1): m.group(2).replace("\\'", "'").replace("&amp;", "&")
        for m in re.finditer(r'<string name="(privacy_[a-z0-9_]+)">(.*?)</string>', text, re.S)
    }
    return {
        "title": strings["privacy_policy_title"],
        "updated": strings["privacy_updated"],
        "intro": strings["privacy_intro"],
        "sections": [
            {"title": strings[f"privacy_s{i}_title"], "body": strings[f"privacy_s{i}_body"]} for i in range(1, 8)
        ],
    }


def main(app: pathlib.Path) -> None:
    res = app / "app" / "src" / "main" / "res"
    out = {"en": load(res, "values"), "bn": load(res, "values-bn")}
    target = pathlib.Path(__file__).resolve().parent.parent / "data" / "privacy.json"
    target.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {target}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    main(pathlib.Path(sys.argv[1]))
