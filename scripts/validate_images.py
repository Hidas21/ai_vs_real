"""
Ellenőrzi az images.json-t:
 - minden AI képhez van-e explanation
 - minden hivatkozott fájl létezik-e a images/ mappában
 - nincsenek-e árva fájlok (a images/ mappában, de nincsenek a manifestben)

Használat:
    cd ai-real-quiz
    python scripts/validate_images.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "images.json"
IMAGES_DIR = ROOT / "images"


def main() -> int:
    if not MANIFEST_PATH.exists():
        print(f"HIBA: nincs {MANIFEST_PATH.name}. Futtasd elobb a download_images.py-t.")
        return 1

    with MANIFEST_PATH.open(encoding="utf-8") as f:
        manifest = json.load(f)

    problems = 0
    missing_files: list[str] = []
    missing_explanations: list[str] = []

    referenced = set()
    for entry in manifest:
        fpath = ROOT / entry["file"]
        referenced.add(fpath.name)
        if not fpath.exists():
            missing_files.append(entry["file"])
            problems += 1
        if entry["label"] == "ai":
            if not entry.get("explanation", "").strip():
                missing_explanations.append(entry["file"])
                problems += 1

    orphans = []
    if IMAGES_DIR.exists():
        for f in IMAGES_DIR.iterdir():
            if f.is_file() and f.name not in referenced:
                orphans.append(f.name)

    print(f"Manifest: {len(manifest)} bejegyzes")
    n_ai = sum(1 for e in manifest if e["label"] == "ai")
    n_real = sum(1 for e in manifest if e["label"] == "real")
    print(f"  AI: {n_ai}   Real: {n_real}")

    if missing_files:
        print(f"\nHIANYZO FAJLOK ({len(missing_files)}):")
        for f in missing_files[:10]:
            print(f"  - {f}")
        if len(missing_files) > 10:
            print(f"  ... es meg {len(missing_files) - 10}")

    if missing_explanations:
        print(f"\nHIANYZO MAGYARAZATOK ({len(missing_explanations)}) AI kepeknel:")
        for f in missing_explanations[:20]:
            print(f"  - {f}")
        if len(missing_explanations) > 20:
            print(f"  ... es meg {len(missing_explanations) - 20}")

    if orphans:
        print(f"\nARVA FAJLOK az images/ mappaban ({len(orphans)}, nincsenek a manifestben):")
        for f in orphans[:10]:
            print(f"  - {f}")

    if problems == 0:
        print("\nOK: minden rendben.")
        return 0
    print(f"\n{problems} problema talalva.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
