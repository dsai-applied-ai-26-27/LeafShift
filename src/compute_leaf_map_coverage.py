"""Compute how many PlantVillage images resolve to an official leaf identifier.

The upstream PlantVillage repository publishes `leaf_grouping/leaf-map.json`,
which maps a normalized source file name to one or more official leaf records.
This script reproduces `data/processed/plantvillage_leaf_map_coverage.csv`.

Download the map first (it is kept outside version control):

    curl -L -o data/raw/leaf_grouping/leaf-map.json \
      https://huggingface.co/datasets/mohanty/PlantVillage/resolve/main/leaf_grouping/leaf-map.json

Then run:

    .venv\\Scripts\\python.exe src\\compute_leaf_map_coverage.py

Matching rule, in order:
  1. lowercase the file-name suffix after `___` and drop the extension;
  2. look the result up directly;
  3. if that fails, remove the word `leaf` and look up again;
  4. repeat 2 and 3 with `.` and `_` swapped, because the map mixes both.

The script is read-only with respect to the dataset and writes one CSV row per
image, so the coverage figure can be recomputed rather than trusted.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
MAP_URL = (
    "https://huggingface.co/datasets/mohanty/PlantVillage/resolve/main/"
    "leaf_grouping/leaf-map.json"
)
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png"}


def candidate_keys(suffix: str) -> list[str]:
    """Return the lookup keys to try, in order, for one file-name suffix."""
    without_extension = re.sub(r"\.(jpg|jpeg|png)$", "", suffix, flags=re.IGNORECASE)
    base = re.sub(r"\s+", " ", without_extension.lower().strip())
    without_leaf = base.replace(" leaf", "")
    variants = [
        base,
        without_leaf,
        base.replace("_", "."),
        base.replace(".", "_"),
        without_leaf.replace("_", "."),
        without_leaf.replace(".", "_"),
    ]
    seen: list[str] = []
    for variant in variants:
        if variant not in seen:
            seen.append(variant)
    return seen


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--map", type=Path, default=PROJECT / "data" / "raw" / "leaf_grouping" / "leaf-map.json")
    parser.add_argument("--root", type=Path, default=PROJECT / "data" / "raw" / "plantvillage" / "PlantVillage")
    parser.add_argument("--out", type=Path, default=PROJECT / "data" / "processed" / "plantvillage_leaf_map_coverage.csv")
    args = parser.parse_args()

    if not args.map.exists():
        print(f"Leaf map not found: {args.map}")
        print(f"Download it from: {MAP_URL}")
        return 1

    leaf_map = json.loads(args.map.read_text(encoding="utf-8"))
    keys = set(leaf_map)
    print(f"leaf map entries: {len(keys):,}")

    rows = []
    for path in sorted(args.root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in IMAGE_SUFFIXES:
            continue
        relative = path.relative_to(args.root).as_posix()
        suffix = path.name.split("___", 1)[1] if "___" in path.name else path.name
        leaf_key = ""
        records: list[str] = []
        for candidate in candidate_keys(suffix):
            if candidate in keys:
                leaf_key = candidate
                records = leaf_map[candidate]
                break
        rows.append(
            {
                "relative_path": relative,
                "filename_suffix": suffix,
                "leaf_key": leaf_key,
                "leaf_records": " | ".join(records),
                "record_count": len(records),
                "matched": "yes" if leaf_key else "no",
            }
        )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["relative_path", "filename_suffix", "leaf_key", "leaf_records", "record_count", "matched"],
        )
        writer.writeheader()
        writer.writerows(rows)

    matched = sum(1 for row in rows if row["matched"] == "yes")
    multi = sum(1 for row in rows if row["record_count"] > 1)
    print(f"images: {len(rows):,}")
    print(f"matched: {matched:,} ({matched / len(rows):.2%})")
    print(f"keys with more than one leaf record: {multi:,}")
    print(f"written: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
