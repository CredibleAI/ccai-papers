#!/usr/bin/env python3
"""Validate all entries and build site/data.json.

Usage:
  python scripts/build.py            # validate + write site/data.json
  python scripts/build.py --check    # validate only (used in PRs)
"""
import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parent.parent
ENTRIES = ROOT / "entries"
SCHEMA = json.loads((ROOT / "schema" / "entry.schema.json").read_text())
OUT = ROOT / "site" / "data.json"
FOLDER_TYPE = {"articles": "article", "projects": "project"}
SLUG = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def main() -> int:
    check_only = "--check" in sys.argv
    validator = Draft202012Validator(SCHEMA, format_checker=FormatChecker())
    errors, items, seen_titles = [], [], {}

    files = sorted(ENTRIES.glob("*/*.y*ml"))
    for path in files:
        rel = path.relative_to(ROOT)
        slug = path.stem
        folder = path.parent.name
        if path.suffix not in (".yml", ".yaml"):
            continue
        if not SLUG.match(slug):
            errors.append(f"{rel}: file name must be lowercase-with-dashes")
        if folder not in FOLDER_TYPE:
            errors.append(f"{rel}: unknown folder '{folder}' (use articles/ or projects/)")
            continue
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as e:
            errors.append(f"{rel}: invalid YAML: {e}")
            continue
        if not isinstance(data, dict):
            errors.append(f"{rel}: entry must be a YAML mapping")
            continue
        for err in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
            where = "/".join(map(str, err.path)) or "(root)"
            errors.append(f"{rel}: {where}: {err.message}")
        if data.get("type") and data["type"] != FOLDER_TYPE[folder]:
            errors.append(f"{rel}: type '{data['type']}' does not match folder '{folder}/'")
        key = re.sub(r"\W+", " ", str(data.get("title", "")).lower()).strip()
        if key in seen_titles:
            errors.append(f"{rel}: duplicate title (also in {seen_titles[key]})")
        seen_titles[key] = rel
        items.append({"id": f"{folder}/{slug}", **data})

    if errors:
        print(f"❌ {len(errors)} problem(s) found:\n")
        for e in errors:
            print("  -", e)
        return 1

    print(f"✅ {len(items)} entries valid")
    if not check_only:
        items.sort(key=lambda x: (-x["year"], x["title"].lower()))
        OUT.write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"→ wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
