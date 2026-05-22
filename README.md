# AI vagy valódi? — Képfelismerő kvíz

Statikus webapp, ami megtanítja a usert AI által generált képeket felismerni a hétköznapokban.
A user 100 képet kap; mindegyiknél eldönti, hogy AI vagy valódi. Ha rosszul tippel egy AI képnél,
megjelenik egy magyarázat, mire kellett volna figyelni.

## Indítás (a kész app)

A `python -m http.server` CORS miatt kell — `file://`-ből nem fog menni a `fetch('images.json')`.

```powershell
cd ai-real-quiz
python -m http.server 8000
# bongeszo: http://localhost:8000
```

## Telepítés nulláról

### 1. Python függőségek (csak az első futtatáshoz, a képek letöltéséhez)

```powershell
pip install datasets pillow huggingface_hub
```

### 2. Képek letöltése (100 db: 50 AI + 50 valódi)

```powershell
cd ai-real-quiz
python scripts/download_images.py
```

Ez letölt 100 képet a [Defactify_Image_Dataset](https://huggingface.co/datasets/Rajarshi-Roy-research/Defactify_Image_Dataset)
HuggingFace dataset-ből az `images/` mappába, hash-elt fájlnevekkel (`img_*.jpg`), hogy a user
ne tudja a fájlnévből kitalálni a választ. Egyúttal létrehoz egy `images.json` manifest fájlt.

### 3. Magyarázatok írása az AI képekhez (kb. 20-30 perc)

Nyisd meg az `images.json`-t egy szövegszerkesztőben (pl. VS Code), és nyisd meg az `images/` mappát
egy galéria nézetben (Windows Explorer → nagy ikonok). Minden AI képhez (`"label": "ai"`) írj egy
1 mondatos magyarázatot magyarul az `"explanation": ""` mezőbe.

**Tipp**: keress jellemző AI-artifaktokat — torz ujjak/fogak, túl szimmetrikus arc, értelmetlen
szöveg/feliratok, lebegő tárgyak, fizikailag lehetetlen árnyékok, túl sima bőr, hibás háttér-elemek.

Példa:

```json
{
  "id": 7,
  "file": "images/img_a3f8c2.jpg",
  "label": "ai",
  "generator": "sdxl",
  "explanation": "A bal kézen hat ujj látható, és a háttérben lévő szöveg betűi értelmetlenek."
}
```

### 4. Ellenőrzés

```powershell
python scripts/validate_images.py
```

Megmutatja, melyik AI képhez maradt ki magyarázat, vagy melyik manifest-bejegyzéshez hiányzik a fájl.

### 5. Indítás

```powershell
python -m http.server 8000
# bongeszo: http://localhost:8000
```

## Fájlszerkezet

```
ai-real-quiz/
├── index.html              # 4 képernyő (start / quiz / feedback / end)
├── style.css               # Reszponzív, sötét téma
├── app.js                  # State machine, localStorage
├── images.json             # 100 kép manifest (file + label + generator + explanation)
├── images/                 # 100 jpg
└── scripts/
    ├── download_images.py  # HuggingFace letöltő
    └── validate_images.py  # Manifest ellenőrző
```

## Csalás-védelem

- A fájlnevek hash-eltek (`img_a3f8c2.jpg`), nem árulják el a választ.
- A `label` és `explanation` mezők **nem kerülnek a DOM-ba** a tipp előtt — `app.js` egy modul-szintű
  `Map`-ben tartja őket, és csak a választás után jeleníti meg a feedbacknél.
- Aki nagyon akar, a Network tabon megnézheti az `images.json`-t — ez ellen statikus app-ban
  nincs védelem (külön backend nélkül).

## Adatvédelem

- Nincs backend, nincs analytics, nincs külső hívás.
- A user pontszáma és haladása csak a böngésző `localStorage`-jában van (`aiquiz.state.v1` kulcs).
- "Új játék" gomb törli ezt.
