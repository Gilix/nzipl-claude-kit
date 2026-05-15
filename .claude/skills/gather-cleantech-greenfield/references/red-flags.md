# Red flags

Signals that demote or drop a candidate. Review before writing each record.

## Cross-cutting flags (apply to all four techs)

### Existence

- **MOU-only** — "signed an MOU", "intends to invest", no site, no permit, no update in 6+ months. → Tier 3, status `Announced`. If 12+ months stale: mark `Cancelled`.
- **Stale announcement** — >18 months old, no construction / permit / hiring / equipment trail. → `Paused` or `Cancelled`; Tier 2 or 3.
- **PR-wire-only** — only sources are Business Wire / PR Newswire / GlobeNewswire. → Tier 3 max; require independent named-author coverage.
- **Politician announcement, no company confirmation** — governor / minister / president announces Company X investing, company silent. → Tier 3 at most; re-verify in 60 days.
- **Shell-company SPV, no parent disclosure** — operator is a local SPV, no parent named. → Drop unless parent confirmed; `origin` requires the parent.
- **Reverse announcement** — announcement says Company X will build in Country Y; company's own IR / 10-K / 20-F mentions nothing. → Treat as rumor. Tier 3 or drop.

### Scope

- **EV / battery / charging** — out of scope for this skill. Belongs in `gather-ev-greenfield`. → Drop.
- **Upstream extraction** — lithium brine, nickel / cobalt mining, polysilicon precursor chemistry, copper smelting, hydrogen feedstock from natural gas without CCUS. → Drop.
- **Brownfield mis-labeled as greenfield** — same site as existing plant, "Phase 2" / "expansion" / "capacity addition" language. → `countAsNew: false`, or update existing record's `investmentM_history`.

### Duplicate

- **Rebrand / rename not caught by dedup** — JinkoSolar = 晶科能源; Goldwind = 金风科技; Mitsubishi Heavy Industries vs Mitsubishi Electric (different companies); Carrier (post-Viessmann acquisition); Hanwha Q Cells = Q CELLS = Hanwha Solutions Qcells. → Check `aliases` of existing records; update rather than insert.
- **Phased expansion as new project** — "First Solar Series 7 Phase 2 in Alabama" when Phase 1 is already recorded. → Update `investmentM_history` + `targetProduction` on existing record.
- **JV branded multiple ways** — common in solar (LONGi-XYZ JV) and hydrogen (Air Products + ACWA Power on NEOM, ITM Power + Linde JVs). → Record once under JV brand; put partner names in `aliases`.

### Evidence quality

- **Three reproductions of one PR** — company PR + Reuters pickup + named-author trade pickup citing the PR = one source with three URLs. Fails Tier 1 "three independent sources" requirement.
- **"Industry sources" with company silence** — named-author trade piece citing "sources familiar" + company declined. → Tier 3 max; re-verify in 90 days.
- **Satellite imagery without timestamp** — can't distinguish 2023 from 2025 construction. → Optional strengthener only, never primary.
- **Local press conflicts with company filing** — local paper says operating; company's 10-K / annual report says "expected to start 2027". → Trust the filing; downgrade status.

### Process

- **Wrong status × tier** — validator catches. Fix tier or status.
- **Wrong tech for projectType** — `tech=solar`, `projectType=blade` — validator catches. Fix the tech assignment.
- **Wrong file for ID** — `SOL-DEU-0001` placed in `solar/USA.json`. Validator catches. Move record.
- **Unsourced numeric claim** — `targetProduction: 5.0` but `sources.targetProduction` missing. → Source it or remove the field.
- **Currency not USD** — `investmentM` in ambiguous units. → Convert at announcement-date FX; annotate in `investmentM_history.original`.
- **Imprecise date with no annotation** — `announced: "2024"` when source has month. → Use most precise form the source supports.

## Solar-specific

- **Polysilicon vaporware** — announced polysilicon capacity is one of the most-overstated metrics in clean tech. Many "100 kt/year" announcements never ramp past 30%. → Tier 3 until production data available; mark `status: Announced` even when company says "Operating" without third-party confirmation.
- **Module-only assembly mis-labeled as cell+module** — many "1 GW solar factory" announcements are module-assembly only, importing cells from China or Vietnam. → Distinguish via `projectType`: `module` (assembly only) vs `cell` (cell production). Read past the headline.
- **Nameplate vs effective capacity confusion** — module-line throughput depends heavily on cell technology (TOPCon vs HJT vs PERC). "5 GW nameplate" can mean 3.5 GW effective. → Record nameplate in `targetProduction`; note cell tech in `product`.
- **AD/CVD circumvention sites** — Southeast Asian module plants (Cambodia, Vietnam, Malaysia, Thailand) labeled as new investment when they're tariff-circumvention reroutes. → Verify operator is a real manufacturer, not a shell.
- **Inverter announcements that bundle BoS** — Sungrow / SolarEdge / Enphase announcements often combine inverter and battery BoS. Distinguish via `projectType`.

## Wind-specific

- **Offshore "permits acquired" ≠ "FID taken"** — offshore wind has a multi-year gap between permit award and final investment decision. → Permit award alone = Tier 3; FID = Tier 1 candidate.
- **Local-content rules inflate counts** — Brazil's BNDES local-content rule and India's PLI scheme drive "factory announcement" theater that doesn't always materialize. → Require company FID + ground-breaking; otherwise Tier 3.
- **"Up to" capacity** — "up to 100 MW per year" usually means 60. → Record the lower bound or flag in `product`.
- **Blade vs nacelle vs turbine-assembly conflation** — Vestas / Siemens Gamesa / GE Vernova run separate blade and nacelle plants. A "Vestas factory in <city>" needs the projectType disambiguated. → Always check what's actually being made before assigning `projectType`.
- **Offshore foundation jackets** — increasingly important supply chain bottleneck. Often announced by EPC firms (Vinci, Boskalis) rather than turbine OEMs. Worth tracking under `projectType: offshore_foundation`.

## Hydrogen-specific

- **MOU-only is the dominant failure mode** — hydrogen has the highest ratio of announced projects to FID-stage projects of any cleantech. → Default to Tier 3 unless company FID is confirmed in IR / regulatory filing. Re-verify every 90 days.
- **Color-confusion** — green / blue / turquoise / pink hydrogen are different production routes with very different capex profiles. Record the color in `sector` (`Green` / `Blue` / `Turquoise` / `Pink`).
- **Ammonia plants without electrolyzer pairing** — "green ammonia plant" sometimes means fossil ammonia plant with future electrolyzer optionality. → If the electrolyzer is not yet contracted, it's blue / fossil ammonia; flag and downgrade.
- **"Hub" announcements that consolidate multiple unconfirmed sites** — US DOE H2Hub program, EU IPCEI Hydrogen, German H2-Großvorhaben all announce regional "hubs" that bundle 5–10 sub-projects, of which 1–2 are confirmed. → Each sub-site requires its own record; do not write a single "hub" record.
- **GW-electrolyzer/year vs kt-H2/year confusion** — same plant can be reported as "1 GW electrolyzer" (input) or "100 kt H2/year" (output). Record one consistently; use `product` to note conversion.
- **Saudi NEOM and similar mega-announcements** — single project announcements at $5–10B scale require extra scrutiny; keep at Tier 3 until EPC contracts publicly disclosed.

## Heat-pump-specific

- **Brand vs OEM** — many "Daikin US plant" announcements are licensed contract manufacturing by Goodman (Daikin's US sub) or third-party OEMs. → Record the actual operator in `company`; put brand in `aliases`.
- **Refrigerant transition retrofit mis-labeled as new capacity** — many "new heat pump factory" announcements in Europe 2024–2025 are existing factories retooling for R290 / CO2 refrigerants. → `countAsNew: false` if same site, same operator; update existing record.
- **Residential vs commercial conflation** — same factory often makes both, but they're recorded as separate `projectType` values (`heat_pump_residential` vs `heat_pump_commercial`). → Pick the dominant line by units/year; note split in `product`.
- **EU heat-pump subsidy announcements ≠ factory announcements** — many "€500M heat pump support" headlines are subsidy programs, not capex on a factory. → Read past the headline.
- **Compressor as upstream input** — compressor plants (Copeland, Sanhua) are scope-valid (`projectType: compressor`) but easy to miss because they're branded as HVAC industrial, not "heat pump". → Watch for compressor announcements when tracking the supply chain.

## Cross-cutting Chinese announcements

- Chinese-domestic media sometimes inflates or pre-announces. Require Tier A on the company's own site (catl.com, longi.com, goldwind.com, sungrowpower.com) in Chinese or English.
- Chinese-province government announcements sometimes precede official company commitment. → Tier 3 until company confirms.
- Weibo / WeChat posts without corroboration: aspirational only, Tier 3 max. (Validator forbids these directly.)

## When a red flag fires

1. Demote tier, reclassify status, or drop.
2. Log the flag in batch notes if using a training-mode task file.
3. If a recurring new pattern, append to `appendix/common-mistakes.md`.
