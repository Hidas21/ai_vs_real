"""
Claude Vision segítségével elemzi az AI képeket és generál magyar magyarázatokat.
Futtatás: python scripts/generate_explanations.py
"""
import base64
import json
import os
import sys
import time
from pathlib import Path

try:
    import anthropic
except ImportError:
    print("pip install anthropic")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "images.json"
IMAGES_DIR = ROOT / "images"

SYSTEM = """Te egy AI-képfelismerő oktató asszisztens vagy.
Kapsz egy képet amelyről tudod hogy AI generálta.
Feladatod: írj PONTOSAN egy rövid magyar mondatot (max 120 karakter) amely megmagyarázza,
mi az a konkrét vizuális jel ami elárulja hogy ez AI generált kép.
Legyen specifikus: mutass rá egy konkrét részletre (pl. ujjak, árnyék, szöveg, szimmetria, textúra).
NE írj bevezetőt, NE írj több mondatot. Csak a magyarázat maga."""

PROMPT = "Mi árulja el hogy ez AI generált kép? Egy mondatban magyarul, konkrétan."


def encode_image(path: Path) -> str:
    return base64.standard_b64encode(path.read_bytes()).decode("utf-8")


def analyze_image(client: anthropic.Anthropic, image_path: Path) -> str:
    b64 = encode_image(image_path)
    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=150,
        system=SYSTEM,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": b64,
                    },
                },
                {"type": "text", "text": PROMPT},
            ],
        }],
    )
    return msg.content[0].text.strip()


def main() -> int:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("HIBA: ANTHROPIC_API_KEY környezeti változó nincs beállítva.")
        print("  Windows PowerShell: $env:ANTHROPIC_API_KEY = 'sk-ant-...'")
        return 1

    with MANIFEST.open(encoding="utf-8") as f:
        manifest = json.load(f)

    ai_entries = [e for e in manifest if e["label"] == "ai"]
    missing = [e for e in ai_entries if not e.get("explanation", "").strip()]
    print(f"Összes AI kép: {len(ai_entries)}, hiányzó magyarázat: {len(missing)}")

    if not missing:
        print("Nincs mit generálni — minden AI képhez van magyarázat.")
        return 0

    client = anthropic.Anthropic(api_key=api_key)
    errors = 0

    for i, entry in enumerate(missing):
        img_path = ROOT / entry["file"]
        print(f"[{i+1}/{len(missing)}] {img_path.name} ... ", end="", flush=True)
        try:
            explanation = analyze_image(client, img_path)
            entry["explanation"] = explanation
            print(explanation[:80])
        except anthropic.RateLimitError:
            print("rate limit, várok 60s...")
            time.sleep(60)
            try:
                explanation = analyze_image(client, img_path)
                entry["explanation"] = explanation
                print(explanation[:80])
            except Exception as e2:
                print(f"HIBA: {e2}")
                errors += 1
        except Exception as e:
            print(f"HIBA: {e}")
            errors += 1
            continue

        # Mentés minden 5. után
        if (i + 1) % 5 == 0:
            with MANIFEST.open("w", encoding="utf-8") as f:
                json.dump(manifest, f, ensure_ascii=False, indent=2)
            print(f"  -> Elmentve ({i+1}/{len(missing)})")

        time.sleep(0.3)

    with MANIFEST.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"\nKész. Hibák: {errors}. Fájl frissítve: {MANIFEST}")
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
