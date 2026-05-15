# DataMexico Endpoints

The DataMexico API has three working URL families, all hosted on `economia.gob.mx`. They wrap the same Tesseract engine but differ in path style and feature set. Production code in this repo uses all three. Pick by query type.

## Active base URLs

| Family | Base | Use for |
|--------|------|---------|
| **Modern data** | `https://www.economia.gob.mx/datamexico/api/data` | Standard cube queries (trade, FDI, census, complexity, remittances, etc.) |
| **Modern stats** | `https://www.economia.gob.mx/datamexico/api/stats/rca` | RCA/specialization queries — and the **only** path that returns full sector coverage for DENUE |
| **Tesseract direct** | `https://www.economia.gob.mx/apidatamexico/tesseract/data.jsonrecords` | Equivalent to `/data` but in JSON-records format. Used in `nzipl_parks_pipeline.py`. Slightly older path; still works. |

Legacy: the kit's `nzipl-claude-kit/CLAUDE.md` and the memory file's header still cite `https://api.datamexico.org/tesseract/`. That host *may* still resolve but no production pipeline points there. Treat it as deprecated; use one of the three above.

## Endpoint selection

| You need | Endpoint | Why |
|----------|----------|-----|
| Records of (drilldowns × measures), single year or year range | `/datamexico/api/data` | Standard query path |
| Same shape but as records-of-objects (slightly different formatting) | `/apidatamexico/tesseract/data.jsonrecords` | Drop-in alternative; chosen when the response shape suits the calling code |
| Industry-by-geography matrix where DENUE thresholds drop manufacturing | `/datamexico/api/stats/rca` with multi-month | Only path that returns complete sector coverage for `inegi_denue` |
| Specialization scores (RCA) computed server-side | `/datamexico/api/stats/rca` | Returns the RCA matrix directly |
| Similarity / proximity measures | `/datamexico/api/stats/jaro` | Used in some intelligence pipelines for relatedness; less common |

If you are unsure: start with `/datamexico/api/data`. Only move to `/stats/rca` when working with DENUE or when you specifically want server-computed RCA.

## Query parameters

All endpoints share the Tesseract parameter shape:

| Param | Purpose | Example | Notes |
|-------|---------|---------|-------|
| `cube` | Cube name | `cube=inegi_denue` | Required |
| `drilldowns` | Dimensions to break out, comma-separated, **with spaces preserved** (URL-encoded) | `drilldowns=Municipality,HS4` | Required for `/data`. Use `+` or `%20` for spaces inside a single dim name |
| `measures` | Numeric measures to return, comma-separated | `measures=Trade Value` | Required for `/data` |
| `parents` | Include parent-dimension fields (e.g., State ID alongside Municipality) | `parents=true` | Almost always set this |
| `locale` | Language for label fields | `locale=es` | Default is English; production uses Spanish for DENUE consistency |
| `<Dim Name>` | Filter on a dimension by member ID(s) or name | `Flow=2`, `Date Year=2023,2024`, `Year=2024` | Comma-separated for multiple values |
| **`/stats/rca`-only** | | | |
| `rca` | The (geo, industry, measure) triple defining the RCA cell | `rca=State,National Industry,Number of Employees Midpoint` | Required for `/stats/rca` |
| `threshold` | Minimum cell value for inclusion | `threshold=National Industry:900,State:900` | Pair with `rca`; format is `<dim>:<min>` |
| `Month` | One or more snapshot dates (YYYYMMDD) | `Month=20250522,20241126,20240523` | Multi-month list aggregates snapshots — critical for DENUE |

### Parameter quirks

- **Spaces in dimension names** must be URL-encoded as `+` (form-encoding) or `%20`. Production uses `urllib.parse.urlencode(...)` which produces `+`. Both work.
- **Comma vs `+` in lists**: comma separates members within a single param; `+` is space-as-form-encoded. Don't conflate.
- **Filtering by ID vs name**: most dimensions accept either. DENUE's `Sector ID` accepts the canonical "31-33" string for manufacturing; `Sector` would accept the Spanish label. Pick one form per query.
- **Year filters are dimension-specific**: `Year`, `Date Year`, `Date Quarter`, and `Month` are different dimensions on different cubes. Match what the cube exposes (see `cubes.md`).

## Response shape

All three endpoints return JSON with this structure:

```json
{
  "data": [
    { "<Dim>": "...", "<Dim ID>": ..., "<Measure>": ..., ... },
    ...
  ],
  "annotations": { ... },
  "headers": [ ... ]
}
```

Records are inside `data`. **Always extract with `payload.get("data", payload)`** — same defensive pattern as OEC. Forgetting this returns the wrapper instead of the rows.

Field naming convention:
- Dimensions appear as both `<Dim>` (label) and `<Dim> ID` (machine ID). E.g., `"Municipality"` and `"Municipality ID"`.
- Some cubes use `Id` instead of `ID` inconsistently — defensively read both: `r.get("National Industry ID") or r.get("National Industry Id")`. Pattern from `nzipl_denue_pipeline.py`.
- Measures appear under their declared name verbatim, e.g., `"Trade Value"`, `"Number of Employees Midpoint"`, `"Investment"`.

## Auth

None. The API is public.

There is no API key, no token, no Authorization header. But:

- **Set a browser User-Agent**: `Mozilla/5.0 (NZIPL Pipeline)` (production value) or any non-default Python UA. Empty UA is occasionally throttled at the edge.
- **Set Accept**: `application/json`. Helps if the gateway negotiates content types.

```python
req = urllib.request.Request(url, headers={
    "User-Agent": "Mozilla/5.0 (NZIPL Pipeline)",
    "Accept": "application/json",
})
```

No Cloudflare bot challenge has been observed (unlike OEC).

## Timeouts

Production uses three different timeouts depending on payload weight:

| Pipeline | Timeout | Why |
|----------|---------|-----|
| `nzipl_parks_pipeline.py` (parks list) | 30s | Small payload (~431 rows) |
| `nzipl_denue_pipeline.py` (DENUE multi-month) | 120s | Larger matrix (state × industry × month) |
| `compute_municipality_rca.py` (mun × HS4 × 2 years) | 300s | Big payload (5+ MB) |

Default to 60s for new code; bump up if the cube is wide.

## Multi-month aggregation (DENUE-specific)

This is the workaround for the silent manufacturing-drop bug:

```python
# /data drops sectors 31-33, 43, 51, 54 from DENUE single-month responses.
# /stats/rca with three or more snapshot dates returns the full matrix.
MONTHS = "20250522,20241126,20240523"
params = {
    "cube": "inegi_denue",
    "Month": MONTHS,
    "rca": "State,National Industry,Number of Employees Midpoint",
    "threshold": "National Industry:900,State:900",
    "locale": "es",
    "parents": "true",
}
url = "https://www.economia.gob.mx/datamexico/api/stats/rca?" + urllib.parse.urlencode(params)
```

Pick three or more recent monthly DENUE snapshots that span at least one year. Verify by checking that response includes records with `Sector ID == "31-33"`. If manufacturing is missing, add another month and retry.

## See also

- `cubes.md` — concrete cube-by-cube request examples
- `gotchas.md` — full list of known traps
- `patterns.md` — copyable Python templates
