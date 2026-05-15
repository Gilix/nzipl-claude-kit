---
name: datamexico-api
description: "Expert reference for the DataMexico API (Mexican government's economic data platform via economia.gob.mx). Use whenever the user asks to query Mexican subnational economic data, mentions DataMexico, DENUE manufacturing employment, AMPIP industrial parks, INEGI economic census, municipality-level HS4 trade, ECI/PCI by Mexican state, FDI by state/sector, ENOE/ETOE labor, CONEVAL poverty/Gini, BANXICO remittances, INFONAVIT credits, or specific cube names like inegi_denue, economy_foreign_trade_mun, industrial_parks, complexity_eci, inegi_economic_census, fdi_year_state_industry, coneval_poverty. Also trigger when the user asks which DataMexico endpoint to use (/data vs /stats/rca), debugs missing manufacturing sectors, hits HS4 chapter-prefix issues, or needs to extend a Mexico pipeline. Do NOT trigger for OEC/BACI queries (different API — those have their own browser-CSV refresh path), nor for cached local data the user can read directly."
---

# DataMexico API Expert

The DataMexico API exposes Mexican government datasets (INEGI, CONEVAL, BANXICO, AMPIP, IMPI, etc.) through a Tesseract-based query layer hosted by Secretaría de Economía. It is public, no key required, and it is the canonical source for Mexican subnational data — state, municipality, and metro-area cuts that OEC's Mexico cube (`trade_s_mex_y_hs6`) does not cover at the same depth.

This skill is a fast reference: pick the right endpoint, pick the right cube, write a working request, avoid the known traps. The 96-cube master catalog lives separately at `~/.claude/projects/-Users-gilbertogarcia-Desktop-GripPoint/memory/reference_datamexico_api.md` — this skill curates only the cubes that show up in real GripPoint work.

## When to use

Use this skill any time you are:

- Writing a new pipeline that pulls Mexican subnational data
- Extending an existing pipeline (`projects/nzipl/data/*.py`, `intelligence/data/datamexico_dashboard_pipeline.py`, `projects/acapulco/data/*.py`, `projects/juarez-elpaso/data/*.py`)
- Picking between DataMexico vs OEC for a Mexico question
- Debugging a DataMexico response that "looks empty" or is missing rows that should exist
- Looking up the right cube name + drilldowns for a question like "FDI by state and industry, last 3 years"

Skip this skill when: the user is querying OEC (use the OEC API reference), or when the data is already cached locally (just `Read` the cache JSON).

## Decision tree

| User wants | Cube | Endpoint | Reference to read |
|------------|------|----------|-------------------|
| "Manufacturing employment by state" | `inegi_denue` | `/stats/rca` (multi-month) | `references/cubes.md`, `references/gotchas.md` (gotcha #1) |
| "Municipality exports / RCA" | `economy_foreign_trade_mun` | `/data` | `references/cubes.md`, `references/gotchas.md` (gotcha #2) |
| "AMPIP industrial parks list" | `industrial_parks` | `/tesseract/data.jsonrecords` | `references/cubes.md`, `references/patterns.md` |
| "ECI / PCI of a state or metro" | `complexity_eci` / `complexity_pci` | `/data` | `references/cubes.md` |
| "Deep industry structure (production, wages, capex)" | `inegi_economic_census` | `/data` | `references/cubes.md` |
| "FDI by state, industry, country of origin" | `fdi_year_state_industry`, `economy_fdi`, related | `/data` | `references/cubes.md` |
| "Poverty / inequality" | `coneval_poverty`, `coneval_gini_mun` | `/data` | `references/cubes.md` |
| "State-level trade (HS6 detail)" | `economy_foreign_trade_ent` | `/data` | `references/cubes.md` |
| "Remittances by municipality" | `banxico_mun_income_remittances` | `/data` | `references/cubes.md` |
| "Anything else from the 96-cube catalog" | (look up) | (usually `/data`) | `~/.claude/projects/.../memory/reference_datamexico_api.md` |
| "Why is sector 31-33 missing from my response" | — | — | `references/gotchas.md` (gotcha #1) |
| "Why is HS4 0702 returning chapter 2 garbage" | — | — | `references/gotchas.md` (gotcha #2) |
| "Why does my state name not match" | — | — | `references/gotchas.md` (gotcha #3) |
| "Show me a working code template" | — | — | `references/patterns.md` |
| "Where is the production version of this pipeline" | — | — | `references/pipelines.md` |

## Hard rules (top of mind)

These are rules that get violated repeatedly and silently corrupt results. Internalize them.

1. **Use `/stats/rca` for industry employment.** The `/data` endpoint silently drops manufacturing (SCIAN 31-33), wholesale (43), info (51), and professional services (54) from DENUE. Always pair `/stats/rca` with multi-month: `Month=20250522,20241126,20240523`. Discovered in `nzipl_denue_pipeline.py`.

2. **Extract the last 4 digits when reading `HS4 ID`.** DataMexico HS4 IDs include a chapter prefix (e.g., `20702` is chapter 2 + HS4 0702, not HS4 20702). Use `str(hs4_id)[-4:]`. Discovered in `compute_municipality_rca.py`.

3. **Normalize state names per consuming dataset.** DataMexico returns Spanish names with accents ("Nuevo León", "Querétaro", "Estado de México"). Energy-infrastructure JSON uses accent-stripped short forms ("Nuevo Leon", "Queretaro", "Mexico"). RCA/DENUE JSONs are inconsistent. The production pattern is three normalization maps (`STATE_TO_PROFILE`, `STATE_TO_DATA`, `STATE_TO_RCA`) — copy them from `nzipl_parks_pipeline.py` rather than inventing new ones.

4. **Stay stdlib-only.** Every existing DataMexico pipeline uses `urllib.request` + `json` only. No `requests`, `httpx`, or `pandas`. This keeps the kit reproducible without a venv. House style.

5. **Always cache.** Production pipelines write `*_cache.json` next to the script and ship a `--skip-api` flag. New pipelines should do the same — one fetch can take 5+ minutes, and DataMexico has no rate-limit guarantees.

6. **Set a browser User-Agent.** `User-Agent: Mozilla/5.0 (NZIPL Pipeline)` and `Accept: application/json` is what production sends. Empty/default Python User-Agent is occasionally throttled.

7. **Records live under `data` key.** Always: `payload.get("data", payload)`. Same wrapper as OEC.

## Picking DataMexico vs OEC

For Mexico data, both DataMexico and OEC have something to offer. Quick rules:

- **Bilateral trade with origin/destination country**: OEC `trade_s_mex_y_hs6` is richer; DataMexico's `economy_foreign_trade_*` aggregates mostly state/mun without country detail.
- **Subnational HS6**: OEC `trade_s_mex_y_hs6` (state level). DataMexico `economy_foreign_trade_mun` (municipality level, but HS4 only).
- **Industry employment, business registry**: DataMexico `inegi_denue` is the only practical source — OEC has no DENUE.
- **ECI/PCI by Mexican state or metro**: DataMexico `complexity_eci` / `complexity_pci` come ready; OEC has cross-country ECI but not subnational Mexico.
- **Poverty, inequality, remittances, education**: DataMexico only.
- **Industrial parks**: DataMexico `industrial_parks` (AMPIP registry, no other source).

When both work, prefer whichever the existing pipeline in scope already uses — drop-in compatibility beats optimization.

## File structure

```
datamexico-api/
├── SKILL.md              ← You are here (decision tree + hard rules)
└── references/
    ├── endpoints.md      ← URL paths, params, response shape, auth, multi-month workaround
    ├── cubes.md          ← Top 12–15 cubes used in production, with full request examples
    ├── gotchas.md        ← Known issues with traceable incidents and workarounds
    ├── patterns.md       ← Python stdlib templates for the 6 most common queries
    └── pipelines.md      ← Pointers to canonical production pipelines + their caches
```

When picking a reference: **always read `endpoints.md` first** if you are writing a new request. Then read the cube-specific entry in `cubes.md` and the relevant gotcha in `gotchas.md`. Use `patterns.md` to copy a starting point. Use `pipelines.md` when you want to read a fully worked production example end-to-end.
