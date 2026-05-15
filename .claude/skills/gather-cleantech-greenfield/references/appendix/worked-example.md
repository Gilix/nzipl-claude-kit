# Worked examples

Four short walkthroughs — one per technology — showing the gap-fill workflow end to end.

Each example tracks: candidate identification → source gathering → tier assignment → record write → validator check.

---

## Example 1: Solar — First Solar Series 7 plant in Iowa, USA

**Candidate**: First Solar announced a Series 7 module plant in Iowa in May 2023.

**Step 1 — Search.**
```
site:investor.firstsolar.com Iowa
"First Solar" Iowa "Series 7"
site:pv-magazine.com First Solar Iowa
site:reuters.com First Solar Iowa
```

**Step 2 — Gather sources.**
- Company IR: `https://investor.firstsolar.com/news/news-details/2023/05/...` — announces $1.1B Iowa Series 7 module plant, 3.5 GW nameplate, ~700 jobs.
- pv-magazine: `https://www.pv-magazine.com/2023/05/.../first-solar-iowa-fourth-us-factory/` — independent confirmation, dated May 2023.
- Reuters: `https://www.reuters.com/business/sustainable-business/...` — independent named-author piece, May 2023.
- (Future: Iowa state econ-dev permit announcement — would make this a Tier 1 corroborator.)

**Step 3 — Tier assignment.** Three independent citation URLs from primary + two named-author trade — qualifies for Tier 1 if status is `Operating` or `Under Construction`. As of announcement (May 2023), status is `Announced`. Pick `Announced` + Tier 2 (announced + one independent corroborator).

**Step 4 — ID and file.** First record for solar in USA → `SOL-USA-0001`. File: `cleantech_greenfield/solar/USA.json`.

**Step 5 — Write.**
```json
{
  "id": "SOL-USA-0001",
  "name": "First Solar Iowa Series 7 Module Plant",
  "company": "First Solar",
  "origin": "USA",
  "country": "USA",
  "city": "Iowa City",
  "lat": 41.6611,
  "lng": -91.5302,
  "tech": "solar",
  "projectType": "module",
  "sector": "Modules",
  "product": "Series 7 CdTe modules, 540W",
  "status": "Announced",
  "announced": "2023-05-09",
  "investmentM": 1100,
  "targetProduction": 3.5,
  "productionUnits": "GW/year",
  "isFDI": false,
  "region": "North America",
  "postIRA": true,
  "verificationTier": 2,
  "verifiedBy": "<Lab member>",
  "verifiedDate": "2026-05-07",
  "sources": {
    "company":    "https://investor.firstsolar.com/news/news-details/2023/05/...",
    "investmentM": "https://www.pv-magazine.com/2023/05/.../first-solar-iowa-fourth-us-factory/",
    "announced":   "https://investor.firstsolar.com/news/news-details/2023/05/...",
    "targetProduction": "https://www.pv-magazine.com/2023/05/.../first-solar-iowa-fourth-us-factory/",
    "status":      "https://www.reuters.com/business/sustainable-business/..."
  }
}
```

**Step 6 — Validate.**
```bash
python3 data/validate_cleantech_record.py projects/nzipl/infra-mx/data/cleantech_greenfield/solar/USA.json
# OK: 1 record(s) clean
```

---

## Example 2: Wind — Vestas blade plant expansion in Pueblo, Colorado

**Candidate**: Vestas announced reopening / expansion of Pueblo CO blade plant in 2023.

**Red flag check**: Vestas operates multiple Colorado plants (Brighton — nacelle, Windsor — towers, Pueblo — blades). Disambiguate by city. This is the Pueblo blade plant.

**Brownfield check**: Vestas Pueblo was originally opened 2010, idled 2019, restarted 2023. Same site → `countAsNew: false`. The 2023 announcement is not a greenfield investment; it's a restart with capex. Update the existing record's `investmentM_history` if Pueblo is already in the dataset; otherwise either skip or record with `countAsNew: false` and note in `product`.

**Decision**: For dataset hygiene, Vestas Pueblo restart is recorded with `countAsNew: false` and treated as an existing-asset reactivation, not a new greenfield announcement.

**Lesson logged to `common-mistakes.md`**: brownfield restart announcements are the #1 wind false-positive in 2023–2024.

---

## Example 3: Hydrogen — Plug Power Genfuel Louisiana

**Candidate**: Plug Power and partners announced a Louisiana green-hydrogen hub site in 2022, part of the broader Genfuel network.

**Red flag check**: "Hub" announcement → consolidates multiple sub-projects. Plug's Louisiana site is one of several announced under the umbrella. Each sub-site requires its own record.

**MOU check**: Multiple sources reported "intends to develop" without confirmed FID through 2024. → Tier 3 max. Status remains `Announced`.

**FID check (as of 2026-05)**: Plug Power's quarterly filings show capex deployment delayed; H2 hub program subject to DOE re-evaluation 2025. → Status `Paused`, Tier 2.

**Color check**: Pink (nuclear-coupled). Some sources say green; verify against Plug Power's own filings, which specify the upstream electricity source.

**Capacity unit check**: Plug Power tends to announce in MW-electrolyzer (input) and tonnes-H2-per-day (output). Convert to canonical: `kt-H2/year` for `productionUnits`, with conversion noted in `product`.

**Decision**: Record at Tier 3, status `Paused`, color in `sector` (`Green` or `Pink` once confirmed). Re-verify in 60 days for FID disclosure.

```json
{
  "id": "HYD-USA-0001",
  "name": "Plug Power Louisiana Green Hydrogen Site",
  "aliases": ["Genfuel Louisiana"],
  "company": "Plug Power",
  "origin": "USA",
  "country": "USA",
  "city": "St. Gabriel",
  "lat": 30.2538,
  "lng": -91.0995,
  "tech": "hydrogen",
  "projectType": "h2_production",
  "sector": "Green",
  "product": "PEM electrolyzer + on-site H2; 15 tonnes/day announced",
  "status": "Paused",
  "announced": "2022-04-01",
  "investmentM": 500,
  "targetProduction": 5.5,
  "productionUnits": "kt-H2/year",
  "isFDI": false,
  "region": "North America",
  "postIRA": false,
  "verificationTier": 3,
  "verifiedBy": "<Lab member>",
  "verifiedDate": "2026-05-07",
  "sources": {
    "company":   "https://www.plugpower.com/press-releases/...",
    "investmentM": "https://www.hydrogeninsight.com/production/..."
  }
}
```

---

## Example 4: Heat pumps — Mitsubishi Electric Trane HVAC factory expansion, Tennessee

**Candidate**: Mitsubishi Electric Trane HVAC US (METUS) announced a $146M Tennessee factory expansion in 2024 for residential heat pumps.

**Brand vs OEM check**: METUS is a JV (Mitsubishi Electric + Trane Technologies). The Tennessee Loudoun plant is operated by METUS, not Mitsubishi Electric directly. Record under `company: "Mitsubishi Electric Trane HVAC US"`, `aliases: ["METUS", "Mitsubishi Electric"]`.

**Brownfield check**: This is an expansion of an existing facility, not a new greenfield. → `countAsNew: false`. If the existing METUS Loudoun record is already in the dataset, update its `investmentM_history`.

**Decision (assuming greenfield record doesn't exist)**: Create record with `countAsNew: false`. Will be excluded from "new capacity" aggregations but kept for full picture.

**Origin tagging**: METUS is a JV; primary controlling entity is Mitsubishi Electric (Japan). `origin: JPN`, `country: USA`. `isFDI: true`.

**Sources**:
- Company: METUS press release
- Trade: ACHR News (independent)
- State: Tennessee TNECD announcement
- Three distinct URLs → Tier 1 candidate. Status `Under Construction` (groundbreaking confirmed) → Tier 1 required, met.

```json
{
  "id": "HPU-USA-0001",
  "name": "METUS Loudoun Tennessee Heat Pump Plant Expansion",
  "aliases": ["METUS", "Mitsubishi Electric"],
  "company": "Mitsubishi Electric Trane HVAC US",
  "origin": "JPN",
  "country": "USA",
  "city": "Loudon",
  "lat": 35.7331,
  "lng": -84.3344,
  "tech": "heatpumps",
  "projectType": "heat_pump_residential",
  "sector": "Residential",
  "product": "Hyper-heat ducted residential heat pumps",
  "status": "Under Construction",
  "announced": "2024-03-15",
  "investmentM": 146,
  "isFDI": true,
  "region": "North America",
  "postIRA": true,
  "countAsNew": false,
  "verificationTier": 1,
  "verifiedBy": "<Lab member>",
  "verifiedDate": "2026-05-07",
  "sources": {
    "company":   "https://www.mitsubishicomfort.com/news/...",
    "investmentM": "https://www.achrnews.com/articles/...",
    "announced":   "https://www.tnecd.com/news/...",
    "status":      "https://www.achrnews.com/articles/..."
  }
}
```

---

## Common pattern across the four

In every example: the dominant work is not finding the announcement but **disambiguating** it — distinguishing module from cell production, distinguishing greenfield from restart, distinguishing operator from brand, distinguishing sub-site from hub. The skill's value is enforcing that discipline mechanically rather than relying on the researcher's memory.
