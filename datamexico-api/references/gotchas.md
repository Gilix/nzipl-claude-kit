# DataMexico Gotchas

Each entry is something that has silently corrupted results in production. Headline → symptom → root cause → workaround → traceable incident. When you hit something weird, scan this page first.

---

## 1. `/data` silently drops manufacturing from DENUE

**Symptom**: You query `inegi_denue` against `/data` for state × industry employment. Manufacturing (SCIAN 31-33), wholesale (43), info (51), and professional services (54) are missing — but no error is raised. Sectors 11 (agriculture), 21 (mining), 22 (utilities), and the rest are there.

**Root cause**: DataMexico's `/data` endpoint applies undocumented thresholds that suppress dimension members where the cell value is below the cutoff. For DENUE, this drops the four manufacturing-adjacent sectors entirely. Single-month queries also fail to clear thresholds even on the surviving sectors.

**Workaround**: Use `/stats/rca` instead, with three or more monthly snapshots:

```python
STATS_URL = "https://www.economia.gob.mx/datamexico/api/stats/rca"
params = {
    "cube": "inegi_denue",
    "Month": "20250522,20241126,20240523",
    "rca": "State,National Industry,Number of Employees Midpoint",
    "threshold": "National Industry:900,State:900",
    "locale": "es",
    "parents": "true",
}
```

**Verification**: After fetching, check `any(r.get("Sector ID") == "31-33" for r in data)`. If False, add another month and retry.

**Discovered in**: `projects/nzipl/data/nzipl_denue_pipeline.py` lines 27–34. The pipeline has a multi-paragraph comment block explaining this — read it if you're writing a sibling pipeline for another country.

---

## 2. HS4 IDs include a chapter prefix

**Symptom**: You query `economy_foreign_trade_mun` with `drilldowns=Municipality,HS4`. The response has `HS4 ID` values like `20702`, `40703`, `170100` — five and six digit numbers, not the 4-digit codes you expected. If you blindly use these as HS4 keys, joins to your taxonomy fail.

**Root cause**: DataMexico encodes HS4 IDs as `<chapter><HS4>`, where `<chapter>` is the 1-2 digit HS chapter that scoped the original product. So `20702` is chapter 2 + HS4 0702, and `170100` is chapter 17 + HS4 0100 (wait — that one is suspicious; in practice 6-digit IDs come from cubes that mix HS levels, double-check).

**Workaround**: Always extract the trailing 4 digits:

```python
def extract_hs4(hs4_id) -> str:
    s = str(hs4_id).strip()
    return s[-4:] if len(s) > 4 else s.zfill(4)
```

**Verification**: For 2024 data, HS4 `0702` should be tomatoes — confirm by checking the corresponding `HS4` (label) field shows "Tomatoes, fresh or chilled" or similar.

**Discovered in**: `projects/nzipl/data/compute_municipality_rca.py` line 101. The `extract_hs4()` helper is the canonical implementation; reuse it.

---

## 3. State names need three normalization maps

**Symptom**: You join DataMexico responses to `energy-infrastructure.json` profiles, `nzipl_mex_state_rca.json`, or another local dataset, and 4–6 states mysteriously have no data on either side of the join.

**Root cause**: Mexican state names appear in at least three forms across the data ecosystem:

| DataMexico (Spanish, accents) | Energy infra (accent-stripped short) | RCA/DENUE (mostly DataMexico, but with edge cases) |
|------------------------------|--------------------------------------|----------------------------------------------------|
| Coahuila de Zaragoza | Coahuila | Coahuila de Zaragoza |
| Michoacán de Ocampo | Michoacan | Michoacán de Ocampo |
| Querétaro | Queretaro | Querétaro de Arteaga |
| Veracruz de Ignacio de la Llave | Veracruz | Veracruz de Ignacio de la Llave |
| México (= Estado de México) | Estado de Mexico | México (RCA) / Estado de México (DENUE) |
| Nuevo León | Nuevo Leon | Nuevo León |
| San Luis Potosí | San Luis Potosi | San Luis Potosí |
| Yucatán | Yucatan | Yucatán |

**Workaround**: Production uses three normalization maps in `nzipl_parks_pipeline.py`:

- `STATE_TO_PROFILE` — DataMexico → energy-infrastructure profile keys (accent-stripped short forms)
- `STATE_TO_DATA` — DataMexico → RCA/DENUE keys (mostly identity, plus `Querétaro → Querétaro de Arteaga`)
- `STATE_TO_RCA` — special case: `Estado de México → México` (RCA only; DENUE keeps "Estado de México")

Plus a `strip_accents()` helper for fuzzy fallback matching. Copy these maps verbatim from the parks pipeline rather than re-deriving them — they were debugged against real data.

**Discovered in**: `projects/nzipl/data/nzipl_parks_pipeline.py` lines 64–90. Documented in CLAUDE.md "Known Gotchas" section.

---

## 4. `Id` vs `ID` field-name inconsistency

**Symptom**: A pipeline that worked yesterday returns `None` for one of its dimension IDs. You check the response and `National Industry ID` is missing — but `National Industry Id` is there.

**Root cause**: Different cubes capitalize the suffix differently. Most use `ID`. A few use `Id`. There may be no rhyme or reason — possibly historical artifacts of how cubes were registered.

**Workaround**: Read defensively:

```python
ind_id = r.get("National Industry ID") or r.get("National Industry Id")
```

Production pattern is in `nzipl_denue_pipeline.py` line 200.

---

## 5. Records are nested under `data` key

**Symptom**: Your code iterates over the response and gets metadata fields (`annotations`, `headers`) instead of records.

**Root cause**: All Tesseract responses wrap records in `{"data": [...], "annotations": {...}, "headers": [...]}`.

**Workaround**: Always: `payload.get("data", payload)`. The fallback (`payload`) handles the rare case where the API returns a bare list.

```python
with urllib.request.urlopen(req) as resp:
    payload = json.loads(resp.read().decode("utf-8"))
records = payload.get("data", payload)
```

Same pattern as OEC. Standard everywhere in this codebase.

---

## 6. URL encoding spaces in dimension names

**Symptom**: A query with `drilldowns=Number of Employees Midpoint` returns 400 or empty data when typed manually.

**Root cause**: Dimension names with spaces need to be URL-encoded. Manual URL construction is fragile.

**Workaround**: Always build the URL with `urllib.parse.urlencode(params)`. It produces `+` for spaces (form-encoding), which Tesseract accepts. `%20` also works.

```python
url = "https://www.economia.gob.mx/datamexico/api/data?" + urllib.parse.urlencode(params)
```

Don't hand-construct the query string.

---

## 7. Industrial parks have no coordinates

**Symptom**: You pull `industrial_parks` and want to plot points on a map. The records have `Industrial Parks ID`, `Industrial Parks` (name), `Municipality`, `State` — but no lat/lng.

**Root cause**: AMPIP's registry is a directory of park names; coordinates were never digitized into the cube.

**Workaround**: Geocode separately with a 3-tier Nominatim ladder:

1. Park name + municipality + state + country
2. Generic "parque industrial, <muni>, <state>, Mexico"
3. Municipality centroid from `mx_municipalities.json` (computed from polygon coordinates)

Cache results to `parks_geocode_cache.json`. Respect Nominatim's 1 req/sec rate limit (`time.sleep(1.1)` between requests). Set a real `User-Agent` with a contact email — Nominatim blocks anonymous bots.

**Reference**: `nzipl_parks_pipeline.py` lines 211–305 has the full implementation.

---

## 8. DENUE drilldown depth: state × national-industry × employees-midpoint

**Symptom**: You change `rca=State,National Industry,Number of Employees Midpoint` to a different triple and the response is empty or wrong.

**Root cause**: DENUE's `/stats/rca` endpoint expects a specific dimension triple matching the underlying RCA computation. Other combinations are not pre-computed.

**Workaround**: For state-level employment by industry, use exactly the production triple. For municipality-level, swap `State` for `Municipality` (untested in this kit but should work; verify before relying). For non-employment measures (`Companies`, `Employees LCI`/`UCI`), test by swapping the third dimension.

---

## 9. Always set `parents=true`

**Symptom**: Response records have `Municipality` and `Municipality ID` but you also need `State` for downstream joins, and it's missing.

**Root cause**: Default Tesseract responses include only the requested drilldowns. Parent levels of the geography hierarchy (state for municipality, region for state) are dropped.

**Workaround**: Add `parents=true` to every query. It's nearly free in payload size and saves a round trip. Production pipelines use it universally.

---

## 10. Cache aggressively with `--skip-api`

**Symptom**: A pipeline works, you make a small downstream change, and re-running takes 5 minutes because it re-fetches the API.

**Root cause**: DataMexico is fast for narrow queries but slow for wide ones (5+ MB payloads can take 60–300s). Re-fetching unchanged data is wasted time.

**Workaround**: Production pattern: write the raw API response to `<cube>_cache.json` next to the pipeline, expose a `--skip-api` CLI flag, and read from cache when set. Reference: every `*.py` in `projects/nzipl/data/` follows this pattern.

```python
parser.add_argument("--skip-api", action="store_true", help="Use cached data only")
# ...
if CACHE_FILE.exists():
    return json.load(open(CACHE_FILE))
# else: fetch and write
```

---

## 11. Legacy `api.datamexico.org` host

**Symptom**: Old documentation (including `nzipl-claude-kit/CLAUDE.md` and the master catalog header) cites `https://api.datamexico.org/tesseract/`. New code in this repo doesn't.

**Status**: That host may still respond, but no production pipeline uses it. The canonical hosts are on `economia.gob.mx`. Treat the old URL as deprecated; if you find it in code, update to one of:

- `https://www.economia.gob.mx/datamexico/api/data`
- `https://www.economia.gob.mx/datamexico/api/stats/rca`
- `https://www.economia.gob.mx/apidatamexico/tesseract/data.jsonrecords`

---

## 12. JSON encoding for non-ASCII characters

**Symptom**: You write the cache to disk, open it, and Spanish accents are mangled (`Mu00e9xico` instead of `México`).

**Root cause**: Python's `json.dump` defaults to `ensure_ascii=True`, which escapes non-ASCII.

**Workaround**: Pass `ensure_ascii=False` when caching. Production:

```python
json.dump(payload, f, ensure_ascii=False)
```

Same pattern as the rest of GripPoint's pipelines.

---

## See also

- `endpoints.md` — full API surface
- `cubes.md` — cube-by-cube examples
- `patterns.md` — copyable code that already accounts for these traps
- `pipelines.md` — production examples to read end-to-end
