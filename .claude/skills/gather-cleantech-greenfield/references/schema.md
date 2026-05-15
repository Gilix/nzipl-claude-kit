# Schema reference

Output files: `projects/nzipl/infra-mx/data/cleantech_greenfield/<tech>/<ISO3>.json` (one array per tech-country pair).
Validator: `data/validate_cleantech_record.py`.

## Required typed fields (15)

| Field | Type | Notes |
|-------|------|-------|
| `id` | string | `<TECH>-<ISO3>-<NNNN>`. Prefix maps to `tech`: `SOL`/`WND`/`HYD`/`HPU`. Zero-padded, sequential per tech-country file. |
| `name` | string | Canonical facility name as the operator uses it. |
| `company` | string | Current majority operator. |
| `origin` | ISO-3 | Parent HQ country. |
| `country` | ISO-3 | Destination country. Must match the file's ISO-3. |
| `city` | string | Primary municipality. |
| `lat` | float | WGS84, within 5 km of `city`. |
| `lng` | float | WGS84. |
| `tech` | enum | `solar` \| `wind` \| `hydrogen` \| `heatpumps`. Must match the ID prefix. |
| `projectType` | enum | Tech-specific — see matrix below. |
| `status` | enum | `Operating` \| `Under Construction` \| `Planned` \| `Announced` \| `Paused` \| `Cancelled` \| `Closed` \| `Rumored`. |
| `announced` | string | `YYYY`, `YYYY-MM`, or `YYYY-MM-DD`. |
| `investmentM` | number | Total capex, USD millions, FX at announcement date. |
| `verificationTier` | int | `1` \| `2` \| `3`. See `verification-protocol.md`. |
| `sources` | object | Field-keyed URL map (see below). |

Plus `verifiedBy` (string, Lab member name) and `verifiedDate` (`YYYY-MM-DD`).

## projectType per tech (validator enforces)

| tech | allowed projectType values |
|------|----------------------------|
| `solar` | `polysilicon`, `ingot`, `wafer`, `cell`, `module`, `tracker`, `inverter`, `glass`, `eva_film`, `junction_box` |
| `wind` | `turbine_assembly`, `blade`, `tower`, `nacelle`, `gearbox`, `generator`, `offshore_foundation`, `cable` |
| `hydrogen` | `electrolyzer_alkaline`, `electrolyzer_pem`, `electrolyzer_soec`, `fuel_cell`, `h2_production`, `ammonia_synth`, `methanol_synth`, `saf_synth` |
| `heatpumps` | `heat_pump_residential`, `heat_pump_commercial`, `compressor`, `refrigerant`, `control_unit` |

## Auto-derived (validator fills or verifies)

| Field | Derivation |
|-------|-----------|
| `isFDI` | `origin != country`. Cross-border = `true`. |
| `region` | From `country` ISO-3 via continent lookup. |
| `postIRA` | `announced >= '2022-08-16'`. |
| `license` | Default `CC-BY-4.0` if omitted. |

The validator errors when any of these is present but inconsistent with the derivation.

## Optional fields (fill when confirmable)

| Field | Type | Notes |
|-------|------|-------|
| `aliases` | string[] | Rename history + shorthand. Dedup uses these. |
| `sector` | string | Optional tech-specific tag, e.g. solar `Modules` / `BoS` / `Polysilicon`; wind `Onshore` / `Offshore`; hydrogen `Green` / `Blue` / `Turquoise` / `Pink`. Free-form, not validated. |
| `product` | string | Free-text specifics (chemistry, model, capacity rating). |
| `prodStarted` | string | ISO-8601. |
| `targetProduction` | number | Annual throughput. **Requires `productionUnits`.** |
| `productionUnits` | enum | Tech-specific — see matrix below. Per year, never cumulative. |
| `targetJobs` | int | Announced hiring target. |
| `investmentM_history` | array | `[{"date": "YYYY-MM-DD", "valueM": N, "source": "URL", "original": "€XB"}]`. Most recent value lives in `investmentM`. |
| `countAsNew` | bool | Default `true`. `false` for phased expansion that shouldn't double-count. |

## productionUnits per projectType

| projectType | allowed productionUnits |
|-------------|-------------------------|
| `polysilicon` | `tonnes/year` |
| `ingot` | `tonnes/year`, `GW/year` |
| `wafer` | `GW/year`, `units/year` |
| `cell` (solar) | `GW/year` |
| `module` | `GW/year` |
| `tracker` | `MW-tracker/year`, `units/year` |
| `inverter` | `GW/year`, `units/year` |
| `glass` | `tonnes/year` |
| `eva_film` | `tonnes/year` |
| `junction_box` | `units/year` |
| `turbine_assembly` | `MW/year`, `units/year` |
| `blade` | `blades/year`, `MW/year` |
| `tower` | `towers/year`, `units/year` |
| `nacelle` | `nacelles/year`, `MW/year`, `units/year` |
| `gearbox` | `units/year` |
| `generator` | `units/year`, `MW/year` |
| `offshore_foundation` | `units/year` |
| `cable` | `km/year`, `tonnes/year` |
| `electrolyzer_alkaline` | `GW-electrolyzer/year`, `units/year` |
| `electrolyzer_pem` | `GW-electrolyzer/year`, `units/year` |
| `electrolyzer_soec` | `GW-electrolyzer/year`, `units/year` |
| `fuel_cell` | `GW/year`, `units/year` |
| `h2_production` | `kt-H2/year` |
| `ammonia_synth` | `kt-NH3/year` |
| `methanol_synth` | `kt-MeOH/year` |
| `saf_synth` | `kt-SAF/year` |
| `heat_pump_residential` | `units/year`, `MW-thermal/year` |
| `heat_pump_commercial` | `units/year`, `MW-thermal/year` |
| `compressor` | `units/year` |
| `refrigerant` | `tonnes/year` |
| `control_unit` | `units/year` |

## The `sources` object

```json
"sources": {
  "company":          "https://www.firstsolar.com/news/...",
  "investmentM":      "https://www.pv-magazine.com/2024/...",
  "announced":        "https://www.firstsolar.com/news/...",
  "prodStarted":      "https://www.pv-magazine.com/2025/...",
  "lat_lng":          "https://www.firstsolar.com/factories/alabama",
  "status":           "https://www.reuters.com/business/energy/..."
}
```

**Rules (enforced):**
- One public URL per sourced field. Non-receipt keys must start with `http(s)://`.
- Forbidden domains: `wikipedia.org`, `grokipedia.com`, `linkedin.com`, `reddit.com`, `twitter.com`, `x.com`, `facebook.com`, `instagram.com`, `medium.com`.
- Composite geocoding uses `lat_lng` (one key, not separate `lat`/`lng` URL keys).
- Receipt keys (currently none) are excluded from the citation count.
- If a field isn't sourced, omit the key. Don't fabricate URLs.

**Tier minimums (distinct citation URLs, excluding receipts):**
- Tier 1 → ≥3
- Tier 2 → ≥2
- Tier 3 → ≥1

## ID-to-file consistency (enforced)

The validator parses the ID and checks the record's file location:

| ID | Must live in |
|----|--------------|
| `SOL-DEU-0001` | `cleantech_greenfield/solar/DEU.json` |
| `WND-CHN-0001` | `cleantech_greenfield/wind/CHN.json` |
| `HYD-USA-0001` | `cleantech_greenfield/hydrogen/USA.json` |
| `HPU-FRA-0001` | `cleantech_greenfield/heatpumps/FRA.json` |

Sequence numbers are independent per file. `SOL-DEU-0001` and `SOL-USA-0001` are both valid first records.

## Example

```json
{
  "id": "SOL-USA-0001",
  "name": "First Solar Series 7 Module Plant",
  "aliases": ["First Solar Lawrence County", "First Solar Alabama Plant"],
  "company": "First Solar",
  "origin": "USA",
  "country": "USA",
  "city": "Trinity",
  "lat": 34.5980,
  "lng": -87.0900,
  "tech": "solar",
  "projectType": "module",
  "sector": "Modules",
  "product": "Series 7 CdTe modules, 540W",
  "status": "Operating",
  "announced": "2022-08-30",
  "prodStarted": "2025-01-15",
  "investmentM": 1100,
  "targetProduction": 3.5,
  "productionUnits": "GW/year",
  "isFDI": false,
  "region": "North America",
  "postIRA": true,
  "license": "CC-BY-4.0",
  "verificationTier": 1,
  "verifiedBy": "Gilberto García-Vazquez",
  "verifiedDate": "2026-05-07",
  "sources": {
    "company":          "https://investor.firstsolar.com/news/news-details/2022/...",
    "investmentM":      "https://www.pv-magazine.com/2022/08/30/first-solar-to-invest-1-1-billion-in-new-us-thin-film-module-factory/",
    "announced":        "https://investor.firstsolar.com/news/news-details/2022/...",
    "prodStarted":      "https://www.reuters.com/business/energy/...",
    "targetProduction": "https://www.pv-magazine.com/2022/08/30/first-solar-to-invest-1-1-billion-in-new-us-thin-film-module-factory/"
  }
}
```

## Run the validator

```bash
# Whole tree:
python3 data/validate_cleantech_record.py projects/nzipl/infra-mx/data/cleantech_greenfield/

# One file:
python3 data/validate_cleantech_record.py projects/nzipl/infra-mx/data/cleantech_greenfield/solar/USA.json
```

Exit 0 = clean. Non-zero = fix and re-run. The validator replaces manual checklist walks.
