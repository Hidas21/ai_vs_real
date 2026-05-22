"""
Letölt 50 AI + 50 real képet a Defactify_Image_Dataset-ből,
fájlneveket hash-eli (hogy a user ne tudjon cheatelni a fájlnévből),
és generál egy csontváz images.json-t.

Használat:
    pip install datasets pillow huggingface_hub
    cd ai-real-quiz
    python scripts/download_images.py
"""
import hashlib
import json
import random
import sys
from pathlib import Path

try:
    from datasets import load_dataset
except ImportError:
    print("Hiányzik a 'datasets' csomag. Telepítsd: pip install datasets pillow huggingface_hub")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = ROOT / "images"
MANIFEST_PATH = ROOT / "images.json"

TARGET_AI = 50
TARGET_REAL = 50
DATASET_NAME = "Rajarshi-Roy-research/Defactify_Image_Dataset"
SEED = 42


def hashed_name(seed_bytes: bytes) -> str:
    h = hashlib.sha1(seed_bytes).hexdigest()[:10]
    return f"img_{h}.jpg"


def normalize_label(row: dict) -> str | None:
    """A dataset több mezőnévvel jöhet. Visszaadja 'ai' | 'real' | None."""
    for key in ("label", "class", "category", "type"):
        v = row.get(key)
        if v is None:
            continue
        if isinstance(v, int):
            return "ai" if v == 1 else "real"
        s = str(v).lower()
        if s in ("ai", "fake", "synthetic", "generated", "1"):
            return "ai"
        if s in ("real", "natural", "0"):
            return "real"
    return None


def main() -> int:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Letöltés: {DATASET_NAME} (streaming, max {TARGET_AI + TARGET_REAL} kép)")

    try:
        ds = load_dataset(DATASET_NAME, split="train", streaming=True)
    except Exception as exc:
        print(f"Nem sikerült a dataset betöltése: {exc}")
        print("Tipp: ellenőrizd, hogy be vagy-e jelentkezve `huggingface-cli login`-nal.")
        return 1

    ai_rows: list[dict] = []
    real_rows: list[dict] = []
    scanned = 0
    for row in ds:
        scanned += 1
        if scanned % 100 == 0:
            print(f"  scanned={scanned}  ai={len(ai_rows)}  real={len(real_rows)}")
        label = normalize_label(row)
        if label == "ai" and len(ai_rows) < TARGET_AI:
            ai_rows.append(row)
        elif label == "real" and len(real_rows) < TARGET_REAL:
            real_rows.append(row)
        if len(ai_rows) >= TARGET_AI and len(real_rows) >= TARGET_REAL:
            break

    if len(ai_rows) < TARGET_AI or len(real_rows) < TARGET_REAL:
        print(f"FIGYELEM: csak {len(ai_rows)} AI és {len(real_rows)} real képet találtam.")

    manifest: list[dict] = []
    next_id = 0
    for row, true_label in [(r, "ai") for r in ai_rows] + [(r, "real") for r in real_rows]:
        img = row.get("image")
        if img is None:
            continue
        seed = f"{true_label}_{next_id}_{SEED}".encode("utf-8")
        fname = hashed_name(seed)
        fpath = IMAGES_DIR / fname
        try:
            img.convert("RGB").save(fpath, "JPEG", quality=85)
        except Exception as exc:
            print(f"  kép mentés hiba ({fname}): {exc}")
            continue

        generator = row.get("generator") or row.get("model") or ("photo" if true_label == "real" else "unknown")
        entry: dict = {
            "id": next_id,
            "file": f"images/{fname}",
            "label": true_label,
            "generator": str(generator),
        }
        if true_label == "ai":
            entry["explanation"] = ""
        manifest.append(entry)
        next_id += 1

    rng = random.Random(SEED)
    rng.shuffle(manifest)

    with MANIFEST_PATH.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    n_ai = sum(1 for e in manifest if e["label"] == "ai")
    n_real = sum(1 for e in manifest if e["label"] == "real")
    print(f"\nKész: {n_ai} AI + {n_real} real -> {MANIFEST_PATH.name}")
    print("Következő lépés: szerkeszd kézzel az images.json-t és tölts ki minden AI képhez egy 'explanation' mondatot.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
