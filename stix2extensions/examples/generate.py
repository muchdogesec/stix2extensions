#!/usr/bin/env python3
"""Write example STIX objects to JSON files.

Loads modules under `stix2extensions.examples` and writes each object's
serialized JSON to `automodel_generated/examples/{category}/{object.id}.json`.
"""
from pathlib import Path
import importlib
import json
import sys
import traceback


FIRST_KEYS = ["type", "spec_version", "id", "created_by_ref", "created", "modified", "name"]
LAST_KEYS = ["object_marking_refs", "extensions", "external_references"]


def sort_key(key):
    if key in FIRST_KEYS:
        return (0, FIRST_KEYS.index(key))
    elif key in LAST_KEYS:
        return (2, LAST_KEYS.index(key))
    else:
        return (1, key)


def generate_examples(repo_root: Path):
    sys.path.insert(0, str(repo_root))

    examples_root = repo_root / "stix2extensions" / "examples"
    out_root = repo_root / "automodel_generated" / "examples"

    if not examples_root.exists():
        raise FileNotFoundError(f"examples folder not found: {examples_root}")

    categories = sorted(p.name for p in examples_root.iterdir() if p.is_dir())

    total = 0

    for category in categories:
        category_dir = examples_root / category
        py_files = sorted(
            p for p in category_dir.glob("*.py") if p.is_file() and p.name != "__init__.py"
        )
        dest_dir = out_root / category
        dest_dir.mkdir(parents=True, exist_ok=True)

        for py_file in py_files:
            module_name = f"stix2extensions.examples.{category}.{py_file.stem}"
            module = importlib.import_module(module_name)

            examples = getattr(module, "examples", None)
            if not examples:
                continue

            for obj in examples:
                obj_id = obj['id']

                filename = dest_dir / f"{obj_id}.json"
                obj_dict = json.loads(obj.serialize())
                sorted_dict = {k: v for k, v in sorted(obj_dict.items(), key=lambda x: sort_key(x[0]))}
                data = json.dumps(sorted_dict, indent=4, ensure_ascii=False)
                filename.write_text(data + "\n", encoding="utf-8")

                total += 1
                print(f"Wrote {filename}")

    print(f"Wrote {total} example files to {out_root}")

def main():
    repo_root = Path(__file__).resolve().parents[2]
    generate_examples(repo_root)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
