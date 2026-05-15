# Working Patterns (Python stdlib only)

Copyable templates for the six most common DataMexico queries. Each is self-contained, uses only `urllib.request`, `urllib.parse`, `json`, and `pathlib`, and applies the gotcha workarounds documented in `gotchas.md`. Drop into a new pipeline and adjust the constants.

House style: stdlib-only (matches every existing DataMexico pipeline), `--skip-api` CLI flag, `*_cache.json` next to the script, defensive ID reads, browser User-Agent.

---

## Pattern 1 — Reusable fetcher with cache

This is the boilerplate every pipeline below builds on. Use it directly when you just need a one-shot fetcher.

```python
import json
import urllib.parse
import urllib.request
from pathlib import Path

USER_AGENT = "Mozilla/5.0 (NZIPL Pipeline)"

def fetch(url: str, cache_path: Path, timeout: int = 60) -> list[dict]:
    """Fetch a DataMexico URL, cache the response, return records."""
    if cache_path.exists():
        with open(cache_path, "r", encoding="utf-8") as f:
            payload = json.load(f)
        return payload.get("data", payload) if isinstance(payload, dict) else payload

    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    })
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        payload = json.loads(resp.read().decode("utf-8"))

    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False)

    return payload.get("data", payload)


def build_url(base: str, params: dict) -> str:
    return base + "?" + urllib.parse.urlencode(params)
```

---

## Pattern 2 — DENUE state employment (with manufacturing-drop workaround)

Source: distilled from `projects/nzipl/data/nzipl_denue_pipeline.py`.

```python
STATS_URL = "https://www.economia.gob.mx/datamexico/api/stats/rca"
MONTHS = "20250522,20241126,20240523"  # multi-month for full sector coverage

params = {
    "cube": "inegi_denue",
    "Month": MONTHS,
    "rca": "State,National Industry,Number of Employees Midpoint",
    "threshold": "National Industry:900,State:900",
    "locale": "es",
    "parents": "true",
}
url = build_url(STATS_URL, params)
records = fetch(url, Path("denue_state_industry_cache.json"), timeout=120)

# Defensive ID read (some cubes use "Id", most use "ID")
for r in records:
    ind_id = r.get("National Industry ID") or r.get("National Industry Id")
    state = r.get("State")
    emp = float(r.get("Number of Employees Midpoint", 0))
    sector_id = str(r.get("Sector ID", ""))  # "31-33" for manufacturing
    if not ind_id or not state or emp <= 0:
        continue
    # ... process ...

# Sanity check: confirm manufacturing showed up
assert any(str(r.get("Sector ID", "")) == "31-33" for r in records), \
    "Manufacturing missing — add another month or switch to /stats/rca"
```

---

## Pattern 3 — Municipality HS4 trade (with chapter-prefix extraction)

Source: distilled from `projects/nzipl/data/compute_municipality_rca.py`.

```python
DATA_URL = "https://www.economia.gob.mx/datamexico/api/data"

params = {
    "cube": "economy_foreign_trade_mun",
    "drilldowns": "Municipality,HS4",
    "measures": "Trade Value",
    "Flow": "2",                    # 2 = exports, 1 = imports
    "Date Year": "2023,2024",       # year range
    "parents": "true",
}
url = build_url(DATA_URL, params)
records = fetch(url, Path("mun_hs4_exports_cache.json"), timeout=300)


def extract_hs4(hs4_id) -> str:
    """DataMexico HS4 IDs include a chapter prefix (e.g., 20702 = chapter 2 + HS4 0702)."""
    s = str(hs4_id).strip()
    return s[-4:] if len(s) > 4 else s.zfill(4)


for r in records:
    mun_id = r.get("Municipality ID")
    hs4 = extract_hs4(r.get("HS4 ID"))
    val = float(r.get("Trade Value", 0))
    state = r.get("State")
    if not mun_id or val <= 0:
        continue
    # ... process ...
```

---

## Pattern 4 — Industrial parks (AMPIP registry)

Source: distilled from `projects/nzipl/data/nzipl_parks_pipeline.py`.

```python
PARKS_URL = (
    "https://www.economia.gob.mx/apidatamexico/tesseract/data.jsonrecords"
    "?cube=industrial_parks"
    "&drilldowns=State,Municipality,Industrial+Parks"
    "&measures=Parks"
)
records = fetch(PARKS_URL, Path("parks_api_cache.json"), timeout=30)

# Each record is one park
for park in records:
    park_id = park["Industrial Parks ID"]
    park_name = park["Industrial Parks"]
    municipality = park["Municipality"]
    municipality_id = park["Municipality ID"]
    state = park["State"]
    state_id = park["State ID"]
    # ... no lat/lng — geocode separately if needed (see nzipl_parks_pipeline.py) ...
```

For the Nominatim geocoding ladder + municipality-centroid fallback, copy `geocode_parks()` and `compute_municipality_centroids()` from `nzipl_parks_pipeline.py` directly. Don't reinvent.

---

## Pattern 5 — ECI / PCI lookup

```python
DATA_URL = "https://www.economia.gob.mx/datamexico/api/data"

# Latest ECI for all Mexican states
params = {
    "cube": "complexity_eci",
    "drilldowns": "Geography State",
    "measures": "ECI,ECI Ranking",
    "Latest": "true",
    "parents": "true",
}
records = fetch(build_url(DATA_URL, params), Path("eci_states_cache.json"))

eci_by_state = {}
for r in records:
    state = r.get("Geography State")
    eci = r.get("ECI")
    rank = r.get("ECI Ranking")
    if state is not None and eci is not None:
        eci_by_state[state] = {"eci": eci, "rank": rank}

# Time series instead: drop "Latest", add Date Day to drilldowns
```

PCI is symmetric — swap `complexity_eci` → `complexity_pci`, `Geography State` → `National Industry`.

---

## Pattern 6 — FDI by state and industry

```python
DATA_URL = "https://www.economia.gob.mx/datamexico/api/data"

# All FDI movements to Nuevo León (state ID 19) by industry, 2020–2024
params = {
    "cube": "fdi_year_state_industry",
    "drilldowns": "Year,FDI Industry",
    "measures": "Investment,Count",
    "Geography": "19",                       # Nuevo León INEGI code
    "Year": "2020,2021,2022,2023,2024",
    "parents": "true",
}
records = fetch(build_url(DATA_URL, params), Path("fdi_nl_cache.json"))

for r in records:
    year = r.get("Year")
    industry = r.get("FDI Industry")
    investment_usd = float(r.get("Investment", 0) or 0)
    count = int(r.get("Count", 0) or 0)
```

For all states at once, drop the `Geography` filter and add `Geography` to `drilldowns`.

---

## Pattern 7 — Economic census deep industry data

```python
DATA_URL = "https://www.economia.gob.mx/datamexico/api/data"

# Transportation equipment manufacturing (SCIAN 3361) by municipality, 2019 census
params = {
    "cube": "inegi_economic_census",
    "drilldowns": "Geography,Industry 6 Digit",
    "measures": "Total Personnel,Wages and Salaries,Total Production,Gross Capital Formation",
    "Industry 4 Digit": "3361",       # filter at parent level
    "Year": "2019",
    "parents": "true",
}
records = fetch(build_url(DATA_URL, params), Path("ec2019_3361_cache.json"))
```

The census exposes 90+ measures; pick the ones you need. To discover the full list query `/tesseract/cubes/inegi_economic_census`.

---

## Pattern 8 — State name normalization (3-map strategy)

When joining DataMexico responses to local datasets, copy these maps. Patterns from `nzipl_parks_pipeline.py`.

```python
# DataMexico → energy-infrastructure profile keys (accent-stripped short forms)
STATE_TO_PROFILE = {
    "Coahuila de Zaragoza": "Coahuila",
    "Michoacán de Ocampo": "Michoacan",
    "Querétaro": "Queretaro",
    "Veracruz de Ignacio de la Llave": "Veracruz",
    "México": "Estado de Mexico",
    "Nuevo León": "Nuevo Leon",
    "San Luis Potosí": "San Luis Potosi",
    "Yucatán": "Yucatan",
}

# DataMexico → RCA/DENUE keys (mostly identity)
STATE_TO_DATA = {
    "Querétaro": "Querétaro de Arteaga",
}

# Special case: RCA uses "México", DENUE uses "Estado de México"
STATE_TO_RCA = {"Estado de México": "México"}


def strip_accents(s: str) -> str:
    for k, v in {"á":"a","é":"e","í":"i","ó":"o","ú":"u","ñ":"n","ü":"u"}.items():
        s = s.replace(k, v).replace(k.upper(), v.upper())
    return s


def to_profile_key(name: str) -> str:
    return STATE_TO_PROFILE.get(name, strip_accents(name))


def to_data_key(name: str) -> str:
    return STATE_TO_DATA.get(name, name)
```

If you hit a 33rd edge case, extend the maps — don't try to derive normalization from accent rules alone.

---

## Skeleton: full pipeline structure

When writing a new DataMexico pipeline, follow this structure. It matches every pipeline in `projects/nzipl/data/`.

```python
#!/usr/bin/env python3
"""<one-line purpose>

Output: <output_file>.json

Usage:
    python3 my_pipeline.py
    python3 my_pipeline.py --skip-api   # use cached data only
"""

from __future__ import annotations
import argparse
import json
import sys
import urllib.request
import urllib.parse
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent
CACHE_FILE = OUTPUT_DIR / "<name>_cache.json"
OUTPUT_FILE = OUTPUT_DIR / "<name>.json"
USER_AGENT = "Mozilla/5.0 (NZIPL Pipeline)"


def fetch_data(...) -> list[dict]:
    if CACHE_FILE.exists():
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            payload = json.load(f)
        return payload.get("data", payload)
    # ... build url, fetch, cache, return ...


def process(records: list[dict]) -> dict:
    # ... transform ...
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-api", action="store_true")
    args = parser.parse_args()
    if args.skip_api and not CACHE_FILE.exists():
        print(f"ERROR: --skip-api but cache not found"); sys.exit(1)
    records = fetch_data(...)
    result = process(records)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
```

---

## See also

- `endpoints.md` — full URL surface and parameter reference
- `cubes.md` — what each cube returns and how to filter it
- `gotchas.md` — why each pattern looks the way it does
- `pipelines.md` — pointers to fully worked production examples
