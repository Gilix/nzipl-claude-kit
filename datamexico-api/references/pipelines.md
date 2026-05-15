# Production Pipelines (Canonical Reference Implementations)

When you want to read a fully worked DataMexico pipeline end-to-end, these are the canonical examples. They have been debugged against real data, ship `--skip-api` flags, and apply the gotcha workarounds from `gotchas.md`. Read them before writing a sibling pipeline for a new country, region, or cube.

All pipelines are stdlib-only Python 3 (`urllib.request`, `json`, `argparse`, `pathlib`, `collections`). No `requests`, no `pandas`, no `pip install` step.

## NZIPL play-card pipelines

| Goal | File | Cube | Endpoint | Output |
|------|------|------|----------|--------|
| State employment by play (LQ + SCIAN4 breakdown) | `projects/nzipl/data/nzipl_denue_pipeline.py` | `inegi_denue` | `/stats/rca` (multi-month) | `nzipl_denue_state_employment.json` |
| Municipality HS4 trade RCA per play | `projects/nzipl/data/compute_municipality_rca.py` | `economy_foreign_trade_mun` | `/data` | `nzipl_mun_trade_rca.json` |
| Municipality relatedness density (HS2 co-occurrence) | `projects/nzipl/data/compute_municipality_relatedness.py` | (uses cached HS4 data) | — | `nzipl_mun_relatedness_density.json` |
| AMPIP industrial parks scoring (geocoded + composite tier) | `projects/nzipl/data/nzipl_parks_pipeline.py` | `industrial_parks` | `/tesseract/data.jsonrecords` | `nzipl_industrial_parks.json` |

These four pipelines also produce the cache files used as DataMexico ground truth elsewhere in the repo:

- `projects/nzipl/data/denue_state_industry_cache.json` — raw DENUE multi-month payload
- `projects/nzipl/data/mun_hs4_exports_cache.json` — raw municipality × HS4 × 2023–2024 (5.3 MB)
- `projects/nzipl/data/parks_api_cache.json` — raw AMPIP registry (431 parks)
- `projects/nzipl/data/parks_geocode_cache.json` — Nominatim geocodes for the 431 parks

If you need any of these data without re-fetching, read the cache directly.

## Cross-project pipelines

| Goal | File | Cubes | Notes |
|------|------|-------|-------|
| State-level dashboard aggregation (general purpose) | `intelligence/data/datamexico_dashboard_pipeline.py` | multiple (ECI, FDI, trade) | Pulls a state-level snapshot for any state ID. Useful starting point for non-play work. |
| Acapulco metro-area economic complexity | `projects/acapulco/data/acapulco_pipeline.py` | `inegi_denue`, `complexity_eci` | Metro-area drilldown pattern — different from state-level. |
| Juárez-El Paso binational metro deck | `projects/juarez-elpaso/data/fetch_*.py` | `inegi_denue`, `complexity_eci`, `inegi_economic_census` | City-level + cross-border. Multiple small fetchers, one per cube. |

## When to read which

| Writing a new pipeline for | Read first |
|----------------------------|-----------|
| Industry employment in another country | (nothing — DataMexico is Mexico-only) |
| Industry employment in a different Mexican geography (metro, mun) | `nzipl_denue_pipeline.py` and adapt `rca=` triple |
| Municipality-level trade in another classification | `compute_municipality_rca.py` |
| Park / facility geocoding | `nzipl_parks_pipeline.py` (the geocoding ladder is reusable) |
| ECI/PCI lookup for a Mexican entity | `intelligence/data/datamexico_dashboard_pipeline.py` |
| Metro-level analysis | `projects/acapulco/data/acapulco_pipeline.py` |
| Multi-cube combination (joining ECI + FDI + trade) | `intelligence/data/datamexico_dashboard_pipeline.py` |

## Pipeline conventions to copy

Every production pipeline shares these conventions. New pipelines should match.

1. **Stdlib only**. No `requests`, `httpx`, `pandas`, `numpy`. The kit must be runnable on a fresh Python install with no `pip install` step.
2. **One file per pipeline**. Configuration constants at top, helpers in middle, `main()` at bottom, `if __name__ == "__main__": main()`. No multi-module split unless the pipeline grows past ~500 lines.
3. **`--skip-api` CLI flag**. Lets reruns skip the slow fetch when you're iterating on the processing logic. Implementation: `argparse` + `sys.exit(1)` if cache missing.
4. **Cache file next to script**. Path: `Path(__file__).parent / "<cube_or_purpose>_cache.json"`. Write with `json.dump(payload, f, ensure_ascii=False)`.
5. **Output file next to script**. Path: `Path(__file__).parent / "<output_name>.json"`. Same encoding rules.
6. **Output JSON includes a `meta` block**. Source attribution, fetch date, parameter snapshot. Example from `nzipl_parks_pipeline.py`:
   ```python
   "meta": {
       "source": "AMPIP via DataMexico (industrial_parks cube)",
       "date": str(date.today()),
       "total_parks": len(parks),
       ...
   }
   ```
7. **Print progress to stdout**. Use `print()` for each step ("Step 1: Fetching...", "Step 2: Processing..."), one summary line per step. No `logging` library — overkill for these scripts.
8. **Defensive ID reads**. `r.get("Foo ID") or r.get("Foo Id")` for any cube where you haven't verified the casing.
9. **Per-cube state name normalization**. Use the maps from `patterns.md` Pattern 8 if joining to local datasets.
10. **Browser User-Agent on every request**. `Mozilla/5.0 (NZIPL Pipeline)`.

## Discovery: what's already in production

If you're not sure whether a query has already been run, check the existing caches:

```bash
ls -la projects/nzipl/data/*_cache.json
ls -la intelligence/data/*_cache.json 2>/dev/null
ls -la projects/acapulco/data/*_cache.json 2>/dev/null
ls -la projects/juarez-elpaso/data/*_cache.json 2>/dev/null
```

A cache file is evidence that the upstream query worked — its size and modification date tell you how big and how fresh.

## See also

- `endpoints.md` — URL families and parameters
- `cubes.md` — which cube to pick
- `gotchas.md` — why these pipelines look the way they do
- `patterns.md` — copy-pasteable code distilled from these pipelines
