# Gather EV Greenfield Investments — Training Guide

> Consolidated single-file version of the NZIPL `gather-ev-greenfield` skill.
> Built for Lab members running the training exercise.
> Source of truth: `nzipl-claude-kit/.claude/skills/gather-ev-greenfield/` (Claude Code skill).
> License: CC-BY-4.0. Attribution: Net Zero Industrial Policy Lab, Johns Hopkins University.

## About this guide

You are about to gather verified, publicly-citable records of EV greenfield manufacturing investments worldwide. This document is both the methodology (how to decide what's real, what's duplicated, what's in scope) and the training exercise (how to practice the methodology until you're consistent with other Lab members).

The exercise doubles as the onboarding path for new Lab researchers. A first cycle is 20 records on a single country; production cycles are 100+ records. First 5 records get pair-reviewed before you continue.

## How to read this guide

Sections 1–3 are concepts and structure. Read them linearly.
Section 4 (verification) and 5 (dedup) are the two hardest judgment calls — read twice.
Section 6 (checklist) is what you run on every record before writing.
Section 7 (red flags) is what you scan before finalizing a tier.
Section 8 is a full worked example — read it end-to-end once before your first record.
Sections 9–10 are appendices: country-by-country search patterns and a Lab-wide mistake log.

Total read time: 45–60 minutes on first pass. Later runs: skim red flags and common mistakes before each batch.

## Table of contents

1. [Skill overview and workflow](#gather-ev-greenfield-investments-skill)
2. [Schema reference](#schema-reference)
3. [Source catalog](#source-catalog)
4. [Verification protocol](#verification-protocol)
5. [De-duplication protocol](#de-duplication-protocol)
6. [Per-record QA checklist](#per-record-qa-checklist)
7. [Red flags](#red-flags)
8. [Worked example — LG Energy Solution Wrocław](#worked-example--lg-energy-solution-wrocław)
9. [Search playbook](#search-playbook)
10. [Common mistakes](#common-mistakes)

---


# Gather EV Greenfield Investments Skill

Compile verified, publicly-citable EV greenfield manufacturing records into the Lab's global dataset. The skill combines (a) a source protocol that prioritizes free, primary, and named-author sources, (b) a three-tier verification gate, and (c) a de-duplication pass against the existing BNEF and fDi Markets datasets. It is also the onboarding exercise for new Lab researchers.

## When to use this skill

| User says | You do |
|-----------|--------|
| "find EV investments in <country>" | Run the full gathering workflow (seed → dedup → verify → write) |
| "verify this gigafactory announcement" | Run the single-record verification loop: check sources, assign tier, write record |
| "audit existing Tier-1 records" | Sample existing records and re-check evidence; demote if stale |
| "add the <Company> plant in <City>" | Start from a known candidate; dedup, verify, write |
| "what's our protocol for EV investment data?" | Read `references/verification-protocol.md` + `references/sources.md` to the user |

**Do not use this skill** for upstream mining or refining investments (lithium brines, nickel mines, cobalt refining, precursor chemistry). Those live outside the defined scope. If a user asks for those, flag it and ask whether they want to extend the scope.

## How to use this skill

### Step 1 — Read the methodology

Before touching data, read these files in order. Budget 45–60 minutes on first run; later runs only need a refresher.

1. `references/schema.md` — the output shape. What fields exist, what values are valid.
2. `references/sources.md` — where to search first, second, and last.
3. `references/verification-protocol.md` — how to decide Tier 1 vs 2 vs 3.
4. `references/dedup-protocol.md` — how to avoid double-counting against BNEF and the fDi Markets workbook.
5. `references/red-flags.md` — what signals a "project" is vaporware.
6. `references/checklist.md` — the per-record QA you run before writing.
7. `references/worked-example.md` — end-to-end walkthrough on a real record (LG Energy Solution Wrocław).

On a production run, re-read `red-flags.md` and `common-mistakes.md` every time — those are the files that evolve.

### Step 2 — Confirm or create a task

The skill runs against a task file. If one doesn't exist, copy the template:

```bash
cp tasks/ev-greenfield-TEMPLATE.md tasks/ev-greenfield-<country>.md
cp tasks/ev-greenfield-TEMPLATE-progress.json tasks/ev-greenfield-<country>-progress.json
```

Fill in assignee, country, target record count, priority. If the user hasn't given you a scope, ask for: (a) country or region, (b) target count (20 for training, 100+ for production), (c) priority order (largest first, newest first, or sequential).

### Step 3 — Seed candidate list

Use `references/sources.md` to build a candidate list. Free, primary sources first:
- **US projects** → Atlas EV Hub (free, public, 300+ facilities)
- **Korean/Japanese/Chinese firms** → local-language announcements from KOTRA, METI, MIIT press pages
- **European projects** → national investment agency releases (BMWK, Invest in France, CDP Italia, Invest India, etc.)
- **Global press** → named-author trade coverage: Electrive, Battery-News, InsideEVs, PV Magazine, Reuters, FT

Do not start from fDi Markets or BNEF — those are dedup targets, not candidate sources.

### Step 4 — De-dup against BNEF and FDI_Combined

Before verifying any candidate, run the dedup protocol (`references/dedup-protocol.md`). Match on normalized company + country + state/city + sector. Tag each candidate `new`, `update-bnef`, or `update-fdi`.

### Step 5 — Per-record verification loop

For each candidate:

1. Apply `references/verification-protocol.md` to determine tier.
2. Fill the record per `references/schema.md`.
3. Populate `sources.*` with one public URL per sourced field (same pattern as `/enrich-fdi`).
4. Run `references/checklist.md` — every item must pass or the record is downgraded or dropped.
5. Run `references/red-flags.md` — demote or drop on any flag.

### Step 6 — Write to global JSON

Append or update-in-place in `projects/nzipl/data/nzipl_ev_greenfield_global.json`. Never blind-insert: match first.

### Step 7 — Update progress

Update `tasks/ev-greenfield-<country>-progress.json` after each batch:
- Counters: `candidates_found`, `tier1`, `tier2`, `tier3`, `dropped`, `next_candidate`.
- Append a batch entry: date, count, operator, notes.

Mirror the `enrich-fdi-progress.json` shape exactly.

### Step 8 — Log novel findings

- A new source, local-language trick, or government portal → append to `discoveries.md` per `CONTRIBUTING.md`.
- A recurring mistake → append to `references/common-mistakes.md`.
- A systematic data/API issue → promote via PR to `gotchas.md`.

### Step 9 — Pair-review first five records

The first five records on any new task get pair-reviewed by a second Lab member before proceeding. Catches tier inflation, disambiguation errors, and scope drift.

## Defaults this skill applies

| Decision | Default |
|----------|---------|
| Currency | USD millions, FX at announcement date |
| License | `CC-BY-4.0` per record |
| Paywalled sources | Allowed only when a free mirror exists |
| Target count — training | 20 records |
| Target count — production | 100+ records |
| Status × tier | `Operating` and `Under Construction` require Tier 1 |

## File structure

```
gather-ev-greenfield/
├── SKILL.md                     ← You are here
└── references/
    ├── schema.md                ← JSON schema + field sourcing rules + example record
    ├── sources.md               ← Tiered source catalog (free-first)
    ├── verification-protocol.md ← Tier 1/2/3 evidence gates
    ├── dedup-protocol.md        ← Match against BNEF + FDI_Combined
    ├── search-playbook.md       ← Country/language query templates
    ├── worked-example.md        ← LG Energy Solution Wrocław walkthrough
    ├── checklist.md             ← Per-record QA (printable)
    ├── red-flags.md             ← Vaporware + duplicate signals
    └── common-mistakes.md       ← Appendable Lab-wide pattern log
```

## Related skills and commands

- `/enrich-fdi` — companion command for the existing 698-row fDi Markets workbook. Different dataset, same per-field URL-sourcing philosophy.
- `nzipl-design` — apply when rendering this data into a visualization, map layer, or play-card input.

## What "done" looks like

A task is complete when:
- The target record count is hit.
- 100% of records have `verificationTier` assigned and `verifiedBy` + `verifiedDate` set.
- 100% of records have at least one populated `sources.*` URL.
- Operating / Under-Construction records are all Tier 1.
- Pair review of the first five records is logged in the task file.
- `tasks/ev-greenfield-<country>-progress.json` counters reconcile with the global JSON.

---

# Schema reference

Output file: `projects/nzipl/data/nzipl_ev_greenfield_global.json`

The file is a JSON array of record objects. Empty file = `[]`. Records extend the BNEF schema (`nzipl_bnef_projects.json`) with five additions: `country`, `region`, `projectType`, `aliases`, and the `verification*` / `sources` / `license` metadata block.

## Full field list

| Field | Type | Required | Notes |
|-------|------|:-:|-------|
| `id` | string | yes | Format: `EV-<ISO3>-<NNNN>`. ISO-3 is the destination country. Zero-padded sequential per country. First German record: `EV-DEU-0001`. |
| `name` | string | yes | Canonical facility name. Prefer the name the operator uses (e.g., "Tesla Gigafactory Berlin-Brandenburg"). |
| `aliases` | array of strings | no | Rename history + shorthand ("Giga Berlin", "Gruenheide Plant"). Used by the dedup protocol. |
| `company` | string | yes | Current operator or majority owner. For JVs, the lead party. |
| `origin` | ISO-3 | yes | Parent company HQ country. Tesla → `USA`; BYD → `CHN`; LGES → `KOR`. |
| `country` | ISO-3 | yes | Destination country. |
| `region` | string | yes | Subcontinent grouping. Use: `North America`, `Central America`, `South America`, `Europe`, `MENA`, `Sub-Saharan Africa`, `East Asia`, `SE Asia`, `South Asia`, `Oceania`. |
| `state` | string | yes where applicable | State / province / län / region / autonomous community / prefecture. Omit for country-level records. |
| `city` | string | yes where applicable | Primary municipality. If suburb/industrial park, note in `name`, use the municipality here. |
| `lat` | float | yes | Decimal degrees, WGS84. Within 5 km of named city. |
| `lng` | float | yes | Decimal degrees, WGS84. |
| `sector` | enum | yes | `Batteries` \| `EVs` \| `Charging`. Broadest bucket. |
| `projectType` | enum | yes | `cell` \| `pack` \| `cathode` \| `anode` \| `separator` \| `electrolyte` \| `recycling` \| `vehicle_assembly` \| `motor` \| `inverter` \| `charger`. Most specific category. |
| `product` | string | yes | Free-text specifics. Examples: "Model Y + 4680 cells", "NMC 811 cathode", "160 kW DC fast chargers". |
| `status` | enum | yes | `Operating` \| `Under Construction` \| `Planned` \| `Announced` \| `Paused` \| `Cancelled` \| `Closed` \| `Rumored`. Matches BNEF statuses plus `Announced`. |
| `countAsNew` | bool | yes | BNEF convention. `true` if this is new greenfield capacity that should count toward aggregate totals; `false` for phased-expansion announcements that should not double-count. Default `true`. |
| `announced` | string | yes | ISO-8601. Prefer `YYYY-MM-DD`. `YYYY-MM` or `YYYY` accepted when source is less precise; note ambiguity in `sources.announced` with `(year only)` or `(month only)` annotation. |
| `prodStarted` | string | no | ISO-8601 when known. `null` if not yet started or unknown. Distinct from `announced` — many records have one and not the other. |
| `targetYear` | int | no | Planned first-production year. For projects already in production, equals `prodStarted` year. |
| `investmentM` | float | yes | Current-best estimate of total capital investment in USD millions. FX-converted at announcement date using BIS or OECD reference rate. |
| `investmentM_history` | array | no | For projects with revised figures, append entries: `{"date": "2024-08-01", "valueM": 4500, "source": "URL"}`. Most recent figure lives in `investmentM`. |
| `targetProduction` | mixed | no | Annual throughput at full ramp. Integer preferred. Value depends on `productionUnits`. |
| `realizedProduction` | mixed | no | Actual annual throughput at most recent reporting. |
| `productionUnits` | string | no | Required if `targetProduction` or `realizedProduction` is set. Use: `vehicles/year`, `GWh/year`, `packs/year`, `tonnes/year`, `chargers/year`. Always per year. Never cumulative. |
| `targetJobs` | int | no | Announced hiring target at full ramp. |
| `currentJobs` | int | no | Current headcount at most recent reporting. |
| `postIRA` | bool | yes | `true` if `announced` is on or after 2022-08-16 (US IRA signing date). BNEF convention. Kept for cross-dataset compatibility even when the project is outside the US. |
| `verificationTier` | 1 \| 2 \| 3 | yes | See `verification-protocol.md`. |
| `verifiedBy` | string | yes | Lab member name. Full name preferred (e.g., "A. Rojas", "Gilberto Garcia-Vazquez"). |
| `verifiedDate` | string | yes | ISO-8601 date of most recent verification. Re-verification updates this. |
| `license` | string | yes | Default `CC-BY-4.0`. Per-record override only if a specific source imposes a different license. |
| `sources` | object | yes | Field-keyed URL map. See below. |

## The `sources` object

Mirrors the `/enrich-fdi` column-P-through-W pattern: one public URL per sourced field. Field keys match the record keys above.

```json
"sources": {
  "company":           "https://www.example-company.com/press/2024-01-giga-berlin",
  "investmentM":       "https://www.reuters.com/article/...",
  "announced":         "https://www.example-company.com/press/...",
  "prodStarted":       "https://www.tagesschau.de/...",
  "targetProduction":  "https://mwae.brandenburg.de/permit-doc.pdf",
  "lat_lng":           "https://www.example-city.de/geodata",
  "targetJobs":        "https://brandenburg.de/wirtschaft/...",
  "status":            "https://electrive.com/...",
  "bnef_origin":       "nzipl_bnef_projects.json:id=304",
  "fdi_origin":        "FDI_Combined.xlsx:row=147"
}
```

Rules:

- **One URL per key.** If multiple sources confirm a field, pick the strongest (primary > independent news > trade press > blog).
- **Public URLs only.** Paywalled URLs are acceptable *only when a free syndication mirror exists* — cite the free mirror.
- **Do not fabricate.** If a field isn't sourced, leave the key out of the `sources` object. Don't invent a URL.
- **Dedup receipts** (`bnef_origin`, `fdi_origin`) are internal path strings, not URLs. These document that the record originated from or matches an internal dataset.
- **Composite geocoding.** Use `lat_lng` (one key) rather than separate `lat` and `lng` — a single source typically confirms both.

## Example record

```json
{
  "id": "EV-POL-0001",
  "name": "LG Energy Solution Wrocław",
  "aliases": ["LGES Wroclaw", "LG Chem Wroclaw"],
  "company": "LG Energy Solution",
  "origin": "KOR",
  "country": "POL",
  "region": "Europe",
  "state": "Lower Silesian Voivodeship",
  "city": "Wrocław",
  "lat": 51.0843,
  "lng": 16.9253,
  "sector": "Batteries",
  "projectType": "cell",
  "product": "Lithium-ion pouch cells for European OEMs",
  "status": "Operating",
  "countAsNew": true,
  "announced": "2017-10",
  "prodStarted": "2018-Q1",
  "targetYear": 2025,
  "investmentM": 5000,
  "investmentM_history": [
    {"date": "2017-10-01", "valueM": 1630, "source": "https://www.lgensol.com/..."},
    {"date": "2020-06-01", "valueM": 3400, "source": "https://www.reuters.com/..."},
    {"date": "2023-01-01", "valueM": 5000, "source": "https://electrive.com/..."}
  ],
  "targetProduction": 90,
  "realizedProduction": 70,
  "productionUnits": "GWh/year",
  "targetJobs": 10000,
  "currentJobs": 8000,
  "postIRA": false,
  "verificationTier": 1,
  "verifiedBy": "A. Rojas",
  "verifiedDate": "2026-04-24",
  "license": "CC-BY-4.0",
  "sources": {
    "company":          "https://www.lgensol.com/en/company-history",
    "investmentM":      "https://electrive.com/2023/01/.../lg-energy-wroclaw-5bn",
    "announced":        "https://www.lgensol.com/en/press/release-2017-10",
    "prodStarted":      "https://www.reuters.com/article/lg-chem-wroclaw-2018",
    "targetProduction": "https://electrive.com/2023/.../90-gwh-target",
    "lat_lng":          "https://www.wroclaw.pl/biznes/lg-energy-solution",
    "targetJobs":       "https://www.invest-in-wroclaw.pl/lg-jobs-report",
    "status":           "https://electrive.com/2024/.../operating-capacity",
    "bnef_origin":      "nzipl_bnef_projects.json:id=NOMATCH",
    "fdi_origin":       "FDI_Combined.xlsx:row=NOMATCH"
  }
}
```

## Validation checklist

A record is schema-valid when all of these hold:

- [ ] `id` matches `EV-<3 uppercase letters>-<4 digits>`.
- [ ] `country` and `origin` are ISO-3 (three uppercase letters).
- [ ] `region` is one of the 10 enumerated regions.
- [ ] `sector` is one of `Batteries` \| `EVs` \| `Charging`.
- [ ] `projectType` is one of the 11 enumerated project types.
- [ ] `status` is one of the 8 enumerated statuses.
- [ ] `verificationTier` is `1`, `2`, or `3`.
- [ ] If `verificationTier` is 2 or 3, `status` is NOT `Operating` or `Under Construction`.
- [ ] `announced` parses as a date (YYYY, YYYY-MM, or YYYY-MM-DD).
- [ ] `investmentM` is a number (not a string).
- [ ] If `targetProduction` or `realizedProduction` is set, `productionUnits` is set.
- [ ] `postIRA == (announced >= '2022-08-16')`.
- [ ] `sources` has at least one URL (and matches the tier requirement).
- [ ] `license` is set (default `CC-BY-4.0`).
- [ ] `verifiedBy` and `verifiedDate` are set.

Run this checklist as `references/checklist.md` when a Lab member writes a record.

---

# Source catalog

Tiered inventory of where to look for EV greenfield announcements. Use top-to-bottom: primary sources first, aggregators last. The global dataset is public-citable, so free sources are strongly preferred; paywalled sources are allowed only when a free mirror exists.

## Tier A — Primary (use first)

These are the source-of-truth for any claim. A record can't reach verification Tier 1 without at least one Tier A source.

### Company channels

- **Investor relations + newsroom pages.** Every OEM and battery maker has a press archive: `lgensol.com/press`, `tesla.com/blog`, `byd.com/en/news`, `catl.com/en/news`, `stellantis.com/en/news`, `volkswagen-group.com/en/press`, `volvocars.com/us/news`, `fordmedia.com`, `samsungsdi.com/en/about/news`, etc. Start here.
- **Annual reports and 10-Ks / 20-Fs.** Facility lists and capex breakdowns often sit in the MD&A section. Search `<company> annual report <year> site:sec.gov` for US filers.
- **Investor day slides.** Capacity roadmaps are usually in the Q&A deck. Check the company's IR page.

### Government channels

- **US Department of Energy** — [energy.gov/loan-programs](https://www.energy.gov/lpo/loan-programs-office). Loan Programs Office announcements are the most granular public record for US battery/EV plants. Also: [energy.gov/articles](https://www.energy.gov/articles) for 48C tax-credit awardees.
- **SelectUSA** — [selectusa.gov](https://www.selectusa.gov/) for US inbound investment summaries.
- **Germany BMWK / iXPOS** — [bmwk.de](https://www.bmwk.de/Navigation/EN/Home/home.html) and [gtai.de](https://www.gtai.de/en) for German federal announcements.
- **Korea MOTIE** — [motie.go.kr/eng](https://www.motie.go.kr/eng) and **KOTRA** — [investkorea.org](https://www.investkorea.org/) for Korean inbound and outbound.
- **Japan METI** — [meti.go.jp/english](https://www.meti.go.jp/english/) and **JETRO** — [jetro.go.jp/en](https://www.jetro.go.jp/en/) for Japanese.
- **China MIIT** — [miit.gov.cn](https://www.miit.gov.cn/) and **NDRC** — [en.ndrc.gov.cn](https://en.ndrc.gov.cn/) for Chinese domestic. Note: many Chinese announcements appear first in Chinese-language press.
- **Mexico Secretaría de Economía** — [gob.mx/se](https://www.gob.mx/se) for Mexican inbound.
- **Brazil MDIC / ApexBrasil** — [gov.br/mdic](https://www.gov.br/mdic/) for Brazilian.
- **India MHI (Heavy Industries)** — [heavyindustries.gov.in](https://heavyindustries.gov.in/) and **Invest India** — [investindia.gov.in](https://www.investindia.gov.in/) for Indian.
- **Canada ISED** — [ised-isde.canada.ca](https://ised-isde.canada.ca/) for Canadian projects under the Strategic Innovation Fund.
- **Turkey Presidency Investment Office** — [invest.gov.tr](https://www.invest.gov.tr/en/) for Turkish.
- **UK OZEV / BEIS (DESNZ)** — [gov.uk/government/organisations](https://www.gov.uk/government/organisations) for UK.
- **Subnational incentive filings.** State/province/regional development agencies publish incentive grants with project specifics. Examples: [mwae.brandenburg.de](https://mwae.brandenburg.de/), [economicdevelopment.georgia.gov](https://www.georgia.gov/organization/economic-development), [michiganbusiness.org](https://www.michiganbusiness.org/). Search `<state/province> <company> tax incentive` or `<state> strategic investment <company>`.

### Facility databases (open/free)

- **Atlas EV Hub** — [atlasevhub.com](https://www.atlasevhub.com/). Free, public, 300+ US EV facilities. Start here for any US project.
- **Global Energy Monitor** — [globalenergymonitor.org](https://globalenergymonitor.org/). Primarily power/steel, lighter on EV, but their battery-facility tracker has been growing.
- **OSM + OpenInfraMap** — [openinframap.org](https://openinframap.org/). For coordinate verification and site-boundary checks.
- **European Battery Alliance — Battery Atlas** — check [eba250.com](https://www.eba250.com/) periodically for interactive maps.
- **JATO / EV-Volumes company reports** — occasional free summaries.

## Tier B — Named-author trade press (use second)

Trade coverage with named journalists is strong corroboration. Anonymous newswires are weaker; score them at Tier C.

### Battery + EV manufacturing

- **Electrive** — [electrive.com](https://www.electrive.com/). English + German. Named authors. Strong European and Asian coverage.
- **Battery-News.de** — [battery-news.de](https://battery-news.de/). German-language; fastest European battery-plant tracker.
- **InsideEVs** — [insideevs.com](https://insideevs.com/). US-focused, named authors.
- **Electrek** — [electrek.co](https://electrek.co/). Tesla-heavy but broad EV coverage.
- **CleanTechnica** — [cleantechnica.com](https://cleantechnica.com/). Wide EV/battery coverage.
- **Autonews** — [autonews.com](https://www.autonews.com/). Automotive industry coverage; paywalled but often syndicated.
- **Reuters Autos** — [reuters.com/business/autos-transportation](https://www.reuters.com/business/autos-transportation/). Primary newswire for investment announcements.
- **Bloomberg New Energy** — [bloomberg.com/news/newsletters/new-energy](https://www.bloomberg.com/). Paywalled; look for syndication.

### Regional trade press

- **Europe:** Automotive News Europe, Automobilwoche (DE), L'Argus (FR), Motor.es (ES), Ansa (IT business desk).
- **Korea:** The Elec (EN+KR) — [thelec.net](https://www.thelec.net/). Single best English-language source for Korean battery supply chain.
- **Japan:** Nikkei Asia — [asia.nikkei.com](https://asia.nikkei.com/). Paywalled; JIJI and Kyodo syndicate.
- **China:** CnEVPost — [cnevpost.com](https://cnevpost.com/). EN-language tracker for Chinese EV industry. Caixin, Yicai Global for financial context.
- **India:** Autocar Professional, The Hindu BusinessLine, Economic Times Auto.
- **Mexico:** El Financiero, Reforma, Mexico Industry (English). Also the Secretaría de Economía bulletin.
- **Brazil:** Valor Econômico, Folha de S.Paulo, Automotive Business.

## Tier C — Newswires and general press (use to corroborate)

- AP, AFP, DPA, Kyodo, Xinhua (state-affiliated; use with caution).
- Business Wire, PR Newswire, GlobeNewswire — these are paid distribution services for company press releases. They reproduce primary sources but are themselves not independent. Tag the underlying company press release as the source, not the wire.
- Local-city business journals: Atlanta Business Chronicle, Detroit Free Press, Nashville Business Journal. These often publish permit filings first.

## Tier D — Aggregators and proprietary DBs (dedup targets, not candidate sources)

**Do not use as primary sources.** These are where we check to avoid double-counting, not where we start.

- **fDi Markets (FT)** — `FDI_Combined.xlsx` is the local copy. Dedup only.
- **BloombergNEF Big Green Machine** — `nzipl_bnef_projects.json` is the local copy. Dedup only.
- **Benchmark Mineral Intelligence** — paid; public summaries occasionally usable as Tier B corroboration.
- **S&P Global Mobility / IHS Markit** — paid; rarely accessible.
- **Rho Motion** — paid battery/charging trackers; their public reports are Tier C at best.
- **Rhodium Group — Clean Investment Monitor** — [cleaninvestmentmonitor.org](https://www.cleaninvestmentmonitor.org/). US only; free dashboard but aggregated from primary sources — cite the underlying primary, not Rhodium.

## Language-first rule

For projects with an Asian or European parent, **search local-language sources first**. Often the company's Korean/Japanese/Chinese/German/French/Spanish press release appears days or weeks before the English version. You don't need to be fluent — machine translation suffices for confirming names, numbers, and dates.

- Korean: search `<company hangul> 배터리 공장 <city>` on Naver.
- Japanese: search `<company kanji> EV 工場 <city>` on Google.co.jp.
- Chinese: search `<company hanzi> 电池工厂 <city>` on Baidu.
- German: search `<company> Werk <city>` on Handelsblatt.de, Tagesschau.de.
- French: search `<company> usine <city>` on Le Monde, Les Échos.
- Spanish: search `<company> planta <city>` on El País, Reuters.es, Mexico News Daily.
- Portuguese: search `<company> fábrica <city>` on Valor Econômico, Folha.

## What NOT to use

- **Wikipedia.** Tertiary summary, not a source. Use for lead generation, never cite.
- **LinkedIn posts, X threads, Reddit.** Unless the post is from an official corporate/government account, treat as rumor.
- **Unnamed "industry sources" in trade press.** Down-weight any article that doesn't quote a company representative, government official, or name a primary document.
- **Chinese domestic social media (Weibo, WeChat) without independent corroboration.** Tier 3 at best.
- **Analyst consultancy reports behind a paywall** unless a free summary exists with the same facts.

## Updating this catalog

When you discover a new source that should live here permanently, append it to the appropriate tier above and log a one-line entry in `discoveries.md`. Sources drift: newsrooms shut down, URLs change, government portals reorganize. A quarterly walk-through of the Tier A list is worth scheduling.

---

# Verification protocol

A record's `verificationTier` is the most important field on the object. It signals to every downstream user — analysts, visualizations, external partners — how much weight to put on the entry. Tier inflation is the single most common quality failure on datasets like this one. Read this file carefully before assigning a tier.

## The three tiers

### Tier 1 — Confirmed

**Used for projects we are confident exist and that we stand behind publicly.**

Requires all three:

1. **Primary source.** One of:
   - Company press release on the company's own domain
   - Government filing (incentive grant, permit, loan program disclosure)
   - Regulatory disclosure (SEC 10-K / 20-F / 8-K, ESG report, annual report)
2. **Corroborating signal.** One of:
   - Government permit or incentive filing (if the primary is a company PR, this must be a separate document)
   - Named-author coverage from trade press of groundbreaking, construction, or operation
   - Satellite imagery showing site construction, timestamped (optional strengthener, not required)
3. **Independent news source.** One of:
   - Reuters, Bloomberg, FT, Nikkei Asia, Handelsblatt, WSJ (paywall OK if free mirror exists)
   - Named-author trade press (Electrive, InsideEVs, Electrek, Battery-News, The Elec, CnEVPost)

Three distinct sources minimum. Repeat syndication of a single press release does not count as three sources.

### Tier 2 — Likely

**Used for projects that appear real but where the evidence trail is thinner.**

One of these combinations:

- Company announcement + one independent named-author news source, no permit trail
- Two independent top-tier news sources covering the same project, neither derived from the other
- Government announcement + one independent news source, but no company confirmation (rare — usually a sign the parent company is being cagey; worth a red-flag check)

### Tier 3 — Announced-only

**Used for everything we've recorded but cannot yet verify at higher tiers.**

Any one of:

- A single company press release with no corroboration
- A single trade press article with no corroboration
- An entry pulled from BNEF, fDi Markets, Rhodium, or another aggregator, without independent verification
- MOUs, LOIs, feasibility announcements, "exploring" language
- Rumored projects from reputable sources that haven't been confirmed by the company

Tier 3 records are worth keeping — they become Tier 2 or Tier 1 as evidence accumulates. Mark them clearly and revisit.

## Status × tier constraint

Not every combination of status and tier is valid:

| Status | Tier 1 | Tier 2 | Tier 3 |
|--------|:------:|:------:|:------:|
| Operating | required | ✗ not allowed | ✗ not allowed |
| Under Construction | required | ✗ not allowed | ✗ not allowed |
| Planned | allowed | allowed | allowed |
| Announced | allowed | allowed | allowed |
| Paused | allowed | allowed | allowed |
| Cancelled | allowed | allowed | allowed |
| Closed | required | ✗ not allowed | ✗ not allowed |
| Rumored | ✗ not allowed | ✗ not allowed | required |

**Why:** if a plant is operating, we should have overwhelming evidence — the building exists, it hires people, it ships product. A Tier 2 "Operating" record is a contradiction. Conversely, a Tier 1 "Rumored" is also a contradiction — a rumor that has three primary sources isn't a rumor anymore.

If you find yourself writing a status-tier pair that's not allowed, something is wrong — either you have more evidence than you logged (upgrade tier) or less than you thought (change status).

## Disambiguation rule

If a company has multiple facilities in the same country, every source in the record's citation chain must **distinguish this specific facility**. Acceptable signals:

- City or municipality name (distinct from other facilities)
- Specific permit number or government filing reference
- Groundbreaking date (if different from sister plants)
- Production line or product assignment (e.g., "the Model Y line at Austin, not the Cybertruck line")

If sources conflate two facilities (e.g., "Ford's Kentucky battery plants" without distinguishing BlueOval SK 1 vs 2 vs 3), **drop a tier** until a disambiguating source is found.

Examples of high-ambiguity companies for which disambiguation rigor matters:

- Ford + SK On (BlueOval SK cluster, Kentucky + Tennessee)
- GM + LG Energy Solution (Ultium cluster, multiple states)
- Stellantis + Samsung SDI (StarPlus Energy, Kokomo)
- BYD (dozens of facilities in China, multiple globally)
- CATL (25+ facilities globally)

## Paywall rule

Paywalled primary sources are allowed for Tier 1 **only when a free mirror exists**. The citation URL in `sources.*` must be the free mirror, not the paywall. Examples:

- FT story → Reuters or Nikkei syndication with same facts: cite the syndication.
- Bloomberg story → Reuters pickup, Yahoo Finance repost: cite the free mirror.
- Nikkei Asia → JIJI, Kyodo, or major Japanese news syndicator: cite the syndication.

If no free mirror exists and the facts don't appear anywhere else, the citation fails. Treat that source as invisible and look for another.

Paywalled sources never count as one of the two non-primary signals for Tier 2 unless a free mirror exists.

## Time-bounded verification

**Verification has a shelf life.** A record verified in 2023 might be stale by 2026: the plant may have cancelled, changed ownership, doubled capacity, or relocated. When re-verifying:

- Update `verifiedDate` regardless of outcome.
- If evidence has strengthened, upgrade tier and add `sources.*` URLs.
- If evidence has weakened (cancelled, dormant, stale), downgrade tier.
- If the project has materially changed (new investment figure, new capacity, new status), add to `investmentM_history` and update `status`.

Weekly tier-audits sample 10% of Tier-1 records and force this loop.

## Handling conflicting sources

When sources disagree on a value:

- **Most recent verifiable figure** goes in the main field.
- **Earlier figures** move to `investmentM_history` (or an analogous field) with dated source URLs.
- Never silently average, interpolate, or split the difference. Pick a source and cite it.

When sources disagree on existence or status:

- If the company says "operating" but independent news says "delayed", trust the independent news and downgrade status. The company has an incentive to overstate.
- If the company says "cancelled" but independent news says "paused", trust the company. They know what they intend.

## Walk-through

A Lab member is verifying CATL's facility at Debrecen, Hungary.

1. **Primary.** CATL press release, 2022-08-12, on `catl.com/en/news`: announces 100 GWh plant at Debrecen, €7.3B investment. ✓
2. **Government filing.** Hungarian Ministry of Foreign Affairs and Trade press release, confirming HIPA's approval and site allocation in Debrecen's Southern Industrial Park. ✓
3. **Independent news.** Reuters, 2022-08-12: "CATL to build 7.3 bln euro battery plant in Hungary." Named author. ✓

Three sources, all independent, at least one primary. **Tier 1.** Status can be `Under Construction` if the third signal confirms construction (permit filing or groundbreaking coverage).

Now, two years later, what if a researcher is checking: did it actually start operating? They find:

- Construction photos from Electrive, 2024-03
- A Hungarian business press piece about delayed commissioning
- No explicit CATL announcement of production start

The record can hold Tier 1 at `Under Construction` but cannot advance to `Operating` without a company confirmation or a named-author trade press piece explicitly reporting production start.

## What to write in a record

`verificationTier`: the number, 1 2 or 3.

`verifiedBy`: your name.

`verifiedDate`: today's date, ISO-8601.

`sources.*`: one URL per field you sourced. The three-source minimum for Tier 1 is enforced by populating at least three distinct URLs across the `sources` object. The dedup protocol's origin keys (`bnef_origin`, `fdi_origin`) do not count toward this.

If you find yourself tempted to write Tier 1 but can only fill two URLs, you don't have Tier 1. Downgrade or keep searching.

---

# De-duplication protocol

Before writing a new record, check whether the project already exists in the Lab's other EV datasets. Writing a duplicate is worse than missing a record: analyses end up double-counting investment and capacity. This protocol is mandatory and runs *before* verification.

## Dedup targets

Two internal datasets need to be checked:

1. **`projects/nzipl/data/nzipl_bnef_projects.json`** — 37 Mexico-only records from BloombergNEF's Big Green Machine. Schema is the BNEF base schema the global dataset extends from. These 37 are the source of truth for their Mexican footprint; the global file **inherits** them when we encounter a match.
2. **`projects/nzipl/FDI_Combined.xlsx`** — 698 clean-energy FDI rows from fDi Markets (Financial Times). Battery, solar, and wind projects. Only the Battery rows are relevant to this skill. Rows 1-20 have already been source-enriched via the `/enrich-fdi` command; the remainder are in progress.

Do not check other files (BNEF is not a live feed; FDI_Combined is a point-in-time xlsx). Those are the only two sources the global dataset reconciles against.

## Matching procedure

For each candidate project, before verifying it, run these three matching passes in order. Stop at the first match.

### Pass 1 — Exact-ish match on company + city

Normalize the candidate's `company` and `city` fields (lowercase, strip punctuation, strip legal suffixes like `Inc.`, `Corp.`, `Ltd.`, `GmbH`, `S.A.`, `Co.`). Check for an exact match in both datasets.

If the candidate has `aliases`, include each alias in the match loop.

### Pass 2 — Fuzzy company match within country

If Pass 1 finds nothing, relax to: (normalized company) ∪ (known aliases of company) + country + sector. Look for partial company-name matches (substring or edit distance ≤ 2 words).

Company name traps:

- **Corporate restructurings.** FinDreams is a BYD subsidiary; CAES is a CATL subsidiary; StarPlus Energy is the Stellantis–Samsung SDI JV. Match across both names.
- **Local legal entities.** "LG Chem Poland" ≠ "LG Energy Solution Wrocław" ≠ "LG Chem Wrocław" — but they're the same plant. Match on geography.
- **Joint ventures.** "BlueOval SK" = Ford + SK On — Ford alone or SK On alone might match. Check both.
- **Transliteration.** Chinese company names may appear as pinyin, traditional characters, simplified characters, or Anglicized trade names. 比亚迪 ≈ BYD. 宁德时代 ≈ CATL ≈ Contemporary Amperex Technology.

### Pass 3 — Geography-only match

If Pass 2 finds nothing but you suspect a match (e.g., the candidate is a known sister-facility cluster), check all candidates in BNEF + FDI within ~100 km of the candidate's coordinates. Human review required — same city doesn't always mean same plant.

## Match outcomes

After matching, tag the candidate:

| Tag | Meaning | What to do |
|-----|---------|-----------|
| `new` | No match in either dataset | Proceed to verification + write new record |
| `update-bnef` | Matches a row in BNEF | Import BNEF fields as base, then verify + enrich |
| `update-fdi` | Matches a row in FDI_Combined | Import FDI fields as base, then verify + enrich |
| `update-both` | Matches both BNEF and FDI | Import the more complete record as base, reconcile conflicts, verify + enrich |
| `skip` | Matches and has already been fully verified in global JSON | Skip unless re-verifying a stale record |

## Import procedure — `update-bnef`

1. Copy every non-null BNEF field into the new global record.
2. Map BNEF fields to global schema. Nearly identical — BNEF already has `id`, `name`, `company`, `status`, `announced`, `prodStarted`, `targetYear`, `sector`, `product`, `lat`, `lng`, `city`, `state`, `investmentM`, etc.
3. Add the five new fields: `country` (always `"MEX"` for BNEF-originated records), `region` (`"North America"`), `projectType`, `aliases` (start empty unless known), `origin` (parent HQ — look it up if not in BNEF).
4. BNEF does not have `sources.*` URLs. You must run full verification from scratch to reach Tier 1 on these records. Starting tier is 3 (BNEF-only).
5. Set `sources.bnef_origin = "nzipl_bnef_projects.json:id=<BNEF id>"`. This is the dedup receipt — it documents where the record originated, not a real citation URL.
6. Upgrade tier by adding real citation URLs to `sources.*` from Tier A / B sources.

BNEF stays the system of record for those 37 Mexican records. Do not edit `nzipl_bnef_projects.json` — it's a raw snapshot. The global JSON is where enrichment happens.

## Import procedure — `update-fdi`

1. Open `FDI_Combined.xlsx` (use openpyxl or xlsx2csv). Find the matching row.
2. Map FDI columns to global schema:
   - FDI col C (Parent company) → `company`
   - FDI col D (Company Country HQ) → `origin`
   - FDI col E (Project Status) → `status`
   - FDI col F (Destination Country) → `country`
   - FDI col G (Destination city) → `city`
   - FDI col H (Year Announced) → `announced`
   - FDI col I (Year Completed) → `prodStarted`
   - FDI col K (Industry activity) → inform `projectType`
   - FDI col L (Capital Investment) → `investmentM`
   - FDI cols M-O (JV fields) → `aliases` (list JV partners) + `product` text
   - FDI cols P-W (source URLs already enriched) → seed `sources.*` if those rows have been processed
3. Set `region` based on destination country.
4. Set `sources.fdi_origin = "FDI_Combined.xlsx:row=<N>"` as the dedup receipt.
5. fDi Markets alone is not sufficient for Tier 1. Start at Tier 3 and upgrade via independent sources per `verification-protocol.md`.

## Import procedure — `update-both`

Prefer BNEF as the base (richer schema, more fields populated). Reconcile conflicts following the rules in `verification-protocol.md` ("Handling conflicting sources"). Record both origin receipts: `sources.bnef_origin` and `sources.fdi_origin`.

## Conflict handling

When BNEF says $500M and FDI says $800M:

- **Most recent wins** for the headline `investmentM` value.
- **Both values preserved** in `investmentM_history` with dated entries and source citations.
- If neither has a date, prefer the one with an independent third-party citation.
- Never silently average.

When BNEF says `Operating` and FDI says `Under Construction`:

- Find a third source (press, permit filing) to break the tie.
- Absent a tiebreaker, default to the less optimistic status (Under Construction) and flag for re-verification within 60 days.

## Writing the record

After matching + verifying:

- **`new`** → append to global JSON as new record.
- **`update-*`** → append as new record with the BNEF/FDI origin receipt(s). The global JSON is append-only; you don't edit the source BNEF or FDI files.

Each run of the skill re-reads the global JSON to find any pre-existing match (same project previously written during an earlier session). If found, update-in-place: increment `verifiedDate`, add new `sources.*` URLs, upgrade tier if new evidence supports it.

## When to skip

Skip a candidate if:

- It's already in the global JSON at your target tier or higher, and `verifiedDate` is within the last 90 days.
- It's outside scope (upstream mining, refining, pure EV infrastructure outside the 11 `projectType` categories).
- It fails a red-flag check per `red-flags.md`.

## Quick-reference Python snippet

Not a working pipeline, but a sketch a Lab member can adapt when scripting the dedup pass:

```python
import json
import openpyxl

with open("projects/nzipl/data/nzipl_bnef_projects.json") as f:
    bnef = json.load(f)

wb = openpyxl.load_workbook("projects/nzipl/FDI_Combined.xlsx")
ws = wb.active
fdi = [dict(zip([c.value for c in ws[1]], [c.value for c in row]))
       for row in ws.iter_rows(min_row=2)]

def normalize(s):
    if not s: return ""
    s = s.lower()
    for suf in [" inc", " corp", " ltd", " gmbh", " s.a.", " co.", ",", "."]:
        s = s.replace(suf, "")
    return " ".join(s.split())

def find_match(candidate, pool, key_fields=("company", "city")):
    ncand = {k: normalize(candidate.get(k, "")) for k in key_fields}
    for row in pool:
        if all(ncand[k] and ncand[k] == normalize(row.get(k, "") or row.get(k.capitalize(), ""))
               for k in key_fields):
            return row
    return None

match_bnef = find_match(candidate, bnef)
match_fdi  = find_match(candidate, fdi, ("Parent company", "Destination city"))
```

Adapt the key_fields list to the actual column names in FDI_Combined. The FDI column headers aren't guaranteed stable across sessions — re-read the header row.

## Logging the dedup decision

In each batch update to `tasks/ev-greenfield-<country>-progress.json`, log the dedup tag counts:

```json
{
  "candidates_found": 25,
  "dedup_new": 18,
  "dedup_update_bnef": 1,
  "dedup_update_fdi": 4,
  "dedup_update_both": 0,
  "dedup_skipped": 2
}
```

This makes it easy to spot under-dedup'd batches later (e.g., a batch with 0 `update-bnef` when scanning Mexico is suspicious).

---

# Per-record QA checklist

Run this checklist on every record before writing to the global JSON. Every item must pass, or the record is downgraded, reworked, or dropped. This page is designed to be printable / glanceable.

## Identity

- [ ] `id` matches `EV-<ISO3>-<NNNN>` (e.g., `EV-DEU-0042`). ISO-3 = destination country. Sequence is zero-padded and increments within country.
- [ ] `name` is the canonical facility name the operator uses.
- [ ] `aliases` includes any historical or commonly-used alternate names (rename chains, JV branding, local-entity names).
- [ ] `company` is the current majority operator (not the old name).
- [ ] `origin` is the parent HQ country as ISO-3.

## Geography

- [ ] `country` is ISO-3, matches the ISO-3 in `id`.
- [ ] `region` is one of the 10 enumerated regions in `schema.md`.
- [ ] `state` is the province / state / länder / autonomous community / prefecture.
- [ ] `city` is the primary municipality (not the industrial park brand name).
- [ ] `lat` and `lng` are within 5 km of the named `city`.
- [ ] Coordinates cited in `sources.lat_lng` (use composite key, not separate lat + lng keys).

## Project

- [ ] `sector` is `Batteries` \| `EVs` \| `Charging`.
- [ ] `projectType` is one of the 11 enumerated values. Picked the most specific applicable.
- [ ] `product` is free-text specifics — chemistry, model, capacity, etc.
- [ ] `status` is one of 8 enumerated values.
- [ ] Status × tier rule holds:
  - [ ] `Operating` / `Under Construction` / `Closed` require Tier 1.
  - [ ] `Rumored` requires Tier 3.
  - [ ] `Planned` / `Announced` / `Paused` / `Cancelled` accept any tier.
- [ ] `countAsNew` is `true` for a true new facility; `false` for phased-expansion counts.

## Dates

- [ ] `announced` parses as a date. Annotate `(year only)` or `(month only)` in the source if imprecise.
- [ ] `prodStarted` is ISO-8601 or null.
- [ ] `announced <= prodStarted` (if both set).
- [ ] `targetYear` is an integer year or null.
- [ ] `postIRA == (announced >= '2022-08-16')`.

## Finance and scale

- [ ] `investmentM` is a number (not a string), in USD millions.
- [ ] FX conversion: announcement-date rate, not today's rate.
- [ ] If multiple figures have been announced, `investmentM_history` contains each with a date + source.
- [ ] `targetProduction` is annual throughput, not cumulative.
- [ ] If `targetProduction` or `realizedProduction` is set, `productionUnits` is set.
- [ ] `productionUnits` is one of `vehicles/year`, `GWh/year`, `packs/year`, `tonnes/year`, `chargers/year`.
- [ ] `targetJobs` and `currentJobs` are integers or null.

## Verification

- [ ] `verificationTier` is `1`, `2`, or `3`.
- [ ] Tier 1: three distinct sources in `sources.*`, at least one primary, at least one independent news.
- [ ] Tier 2: at least two distinct sources, one of them a top-tier named-author.
- [ ] Tier 3: at least one source.
- [ ] `verifiedBy` is set.
- [ ] `verifiedDate` is today's date (or the most recent re-verification date).
- [ ] `license` is `CC-BY-4.0` unless a source restricts it.

## Sources

- [ ] Every URL in `sources.*` resolves (no 404).
- [ ] No paywalled URL unless a free mirror is used.
- [ ] No Wikipedia, LinkedIn post, Reddit, or X thread as a source.
- [ ] Chinese-domestic social media citations have independent corroboration.
- [ ] `sources.bnef_origin` and `sources.fdi_origin` are set if the record came from dedup (not counted as citations).

## De-duplication

- [ ] Dedup protocol from `dedup-protocol.md` has been run.
- [ ] Candidate is tagged `new` / `update-bnef` / `update-fdi` / `update-both`.
- [ ] If duplicate exists in the global JSON, update-in-place (bumped `verifiedDate`) instead of inserting.

## Red flags

- [ ] No red flag from `red-flags.md` fires.
- [ ] If a red flag fires, tier is demoted or record is dropped.
- [ ] Common mistakes from `common-mistakes.md` have been reviewed against this record.

## Write

- [ ] Appended to `projects/nzipl/data/nzipl_ev_greenfield_global.json`.
- [ ] Re-parsed after write — file is valid JSON.
- [ ] `tasks/ev-greenfield-<country>-progress.json` counters updated.
- [ ] Batch note added to `batches` array with date, count, operator, and notable findings.

## Discovery logging

- [ ] Novel source, query pattern, or rename chain logged to `discoveries.md`.
- [ ] Any recurring mistake pattern logged to `common-mistakes.md`.

---

## If you can't pass every item

**Downgrade before writing.** A Tier 2 record is more useful than a broken Tier 1 record.

- Fewer than three independent sources → drop to Tier 2 or 3.
- Operating status without a 2024+ confirmation → change status to Planned/Under Construction.
- Uncertain disambiguation (which of three sister plants?) → drop a tier until sources distinguish.
- Fabricated or unresolvable URL → remove that source entirely, re-evaluate tier.
- Cannot confirm it is greenfield (might be a brownfield expansion) → drop or reclassify `countAsNew: false`.

---

# Red flags

Signals that a candidate record is vaporware, duplicated, mis-scoped, or at the wrong tier. When any flag fires, demote tier, reclassify, or drop. Review this file before writing each record; re-read periodically as new patterns emerge.

## Existence flags — "is this project actually real?"

### 1. MOU-only announcement with no follow-up

A memorandum of understanding or letter of intent is not a project. It's an intention to discuss one. Look for:

- Language like "signed an MOU to explore", "intends to invest", "will study the feasibility of"
- No site selected, no permit filed, no groundbreaking date
- No updates in the 6+ months since the announcement

**Action:** If MOU-only, record at Tier 3 with `status: Announced`. If 12+ months old with no follow-up, drop or mark `status: Cancelled` and demote.

### 2. Stale announcement, no construction trail

Announcement is more than 18 months old, but no coverage of:

- Permit approval
- Site preparation
- Groundbreaking
- Equipment orders
- Hiring

**Action:** Mark `status: Paused` or `Cancelled`. Demote to Tier 2 or 3.

### 3. Paid-PR-wire-only coverage

Only sources are Business Wire, PR Newswire, or GlobeNewswire press releases — no independent news picked it up.

**Why it matters:** Wires reproduce company statements verbatim. No editorial filter. Companies sometimes announce aspirational projects with no intent to execute.

**Action:** Cite the underlying company PR, not the wire, and require at least one additional independent source. Without independent coverage, Tier 3 maximum.

### 4. Single-person announcement without company confirmation

A country's investment minister, governor, or mayor announces "X will invest Y billion in our region" but the company has issued no confirmation. Sometimes politicians front-run negotiations.

**Action:** Tier 3 at most. Re-verify in 60 days. Often dies quietly.

### 5. Shell-company subsidiary with no parent disclosure

The announced operator is a local SPV (special-purpose vehicle) or shell entity, and no parent company is named. Common in tax-advantaged jurisdictions.

**Action:** Search corporate registries to identify the parent. If the parent cannot be confirmed, drop. Knowing the parent company is a hard requirement for `origin`.

### 6. Reverse announcement trap

The announcement says "Company X will build a factory in Country Y" but Company X's own press page, investor relations page, and recent earnings calls make no mention of Country Y or the project.

**Action:** Very likely fabricated, exaggerated, or miscommunicated. Treat as rumor. Tier 3 or drop.

## Scope flags — "does this belong in the dataset?"

### 7. Brownfield expansion mis-labeled as greenfield

The "new" plant is actually an expansion of an existing facility — new production line, not a new facility. Double-counts investment and capacity if treated as greenfield.

**Signals:**
- Same site, same address as an existing plant
- "Phase 2", "expansion", "capacity addition" language
- BNEF or FDI already lists the original facility at the same coordinates

**Action:** Set `countAsNew: false`. Better yet, update the existing record's `investmentM_history` instead of creating a duplicate.

### 8. Upstream mining or refining

Lithium extraction, nickel or cobalt mining, nickel refining, cobalt refining, lithium carbonate / hydroxide refining, graphite processing — all **out of scope**.

**Action:** Drop. Do not record. Flag for a potential future `gather-ev-upstream` skill if the user raises it.

### 9. Cell repackaging / pack-assembly-only with imported cells

A "battery plant" that only assembles imported cells into packs isn't a cell factory. Scope-valid as `projectType: pack` but critical to distinguish from `cell`.

**Signals:**
- No chemical process on site (no cathode coating, no electrolyte filling)
- "Pack assembly" language in the announcement
- Capacity announced in "packs/year" not "GWh/year"

**Action:** Use `projectType: pack`. Adjust `productionUnits: packs/year`. Do not call it a gigafactory.

### 10. Non-EV project misclassified

Consumer electronics, grid-scale storage without EV supply chain linkage, military battery plants — these exist but are out of scope.

**Signals:**
- Capacity measured in small cells (coin cells, small prismatic)
- Customer base is laptops, grid storage, military
- No OEM supply agreement

**Action:** Drop. Log what you found in `common-mistakes.md` so future researchers don't repeat the scope check.

## Duplicate flags — "is this already in the dataset?"

### 11. Rebrand/rename not caught by dedup

CATL = 宁德时代 = Contemporary Amperex Technology. BYD = 比亚迪 = FinDreams (battery subsidiary). Stellantis = PSA + FCA merger. SVOLT = spun off from Great Wall Motor.

**Signals:**
- Company name differs slightly from BNEF / FDI
- Geographic coordinates within a few km of an existing record
- Investment figure similar to an existing record

**Action:** Check `aliases` of existing records. Check parent-subsidiary relationships. Update the existing record's `aliases` rather than create a new record.

### 12. Phased expansion counted as separate project

"Volkswagen expands Salzgitter Phase 2 by 40 GWh" — if Phase 1 is already in the dataset, Phase 2 is not a new project. Update `investmentM_history` and `targetProduction`.

**Action:** Update-in-place on the existing record.

### 13. JV branded as both partner names

"BlueOval SK", "StarPlus Energy", "Ultium Cells" — these are JVs with distinct brand names. Search under (a) the JV brand, (b) each partner's name, (c) the facility's city.

**Action:** Record under the JV brand as `company`. Put partner names in `aliases`. Check for duplicates under each partner's name.

## Evidence-quality flags — "is this Tier 1 claim actually supported?"

### 14. Three sources that are all the same press release

The company issued a PR, Reuters reproduced it, Electrive reproduced it. That's one source with three URLs. Doesn't meet the Tier 1 "three independent sources" requirement.

**Action:** Require at least one source that is NOT derived from the others. Typically the government filing or the named-author trade coverage of groundbreaking.

### 15. "Industry sources" quotes with no company confirmation

Named-author trade press article, but the only substantive claim is "according to industry sources familiar with the matter" — and the company declined to comment.

**Action:** Tier 3 maximum. Re-verify in 90 days. Often the project either becomes confirmed or evaporates.

### 16. Satellite imagery without timestamp

A tempting source of "proof" — but satellite imagery without a timestamp doesn't distinguish "plant under construction in 2022" from "existing plant in 2024." Use only timestamped imagery.

**Action:** Use as optional strengthener only, never as a primary Tier 1 source.

### 17. Local-press coverage that conflicts with company filing

A local newspaper says the plant is operating; the company's most recent 10-K says "expected to start operations in 2026."

**Action:** Trust the SEC filing. Local press sometimes mistakes pilot lines for commercial operation. Downgrade status if the company hasn't confirmed.

## Process flags — "did this record get the right treatment?"

### 18. Wrong status × tier

Status is `Operating` but only two sources. Status is `Rumored` but tier is 1. These are protocol violations.

**Action:** Fix status or tier. See `verification-protocol.md` for the matrix.

### 19. Missing `sources.*` for a claimed field

Record claims `targetProduction: 50` but `sources.targetProduction` is empty. Unsourced claim.

**Action:** Either source the claim or remove the field. Don't leave unsourced numbers in the record.

### 20. Currency not converted to USD

`investmentM: 50` with no note — is that $50M, €50M, or ₩50M? Big difference.

**Action:** All figures in USD. FX at announcement date. Annotate in `investmentM_history` if the original currency differed: `{"date": "2024-03-01", "valueM": 540, "source": "https://...", "original": "€500M"}`.

### 21. Record with mixed-precision dates and no annotation

`announced: "2023"` — year only, but the source actually has a specific date. Loses information.

**Action:** Use the most precise form the source supports. If source says "March 2023", write `announced: "2023-03"` and put `(month only)` in the source annotation.

## Cross-cutting: the BYD/China red-flag

Chinese company announcements deserve extra scrutiny:

- Chinese-domestic media coverage is sometimes translated inaccurately
- "Planned" investment figures in Chinese press often include phased numbers that English coverage reports as single-round
- Some announcements on Chinese social media (Weibo, WeChat) are aspirational rather than official
- Government press releases in Chinese provinces sometimes announce before the company has committed publicly

**Action:** For Chinese projects, require a Tier A source on the company's own site (catl.com, byd.com, gotion.com, etc.) in Chinese or English. If only Chinese-domestic media exists, Tier 3 maximum.

## When you hit a red flag

1. Log the specific flag in the record's write-up notes (task file batch notes).
2. Downgrade tier, reclassify status, or drop.
3. If the pattern is recurring, append it to `common-mistakes.md` so others learn.
4. If it's a brand-new pattern not covered here, raise a PR to add it to this file.

---

# Worked example — LG Energy Solution Wrocław

End-to-end walkthrough of adding a single Tier-1 record. The goal is not the specific URLs (those evolve) but the *process* — what a Lab member does, in what order, and why. Read it once fully before your first batch.

The candidate: LG Energy Solution's battery cell plant in Wrocław, Poland. Europe's largest EV-battery cell facility in 2024. A useful training case because it has (a) a Korean parent with Korean-language primary sources, (b) a complex name history (LG Chem → LG Energy Solution), (c) multiple revised investment figures over time, and (d) rich independent coverage.

## Step 1 — Scope check

Before searching, confirm the candidate fits scope. Read the skill's "Do not use this skill for..." section. LG Wrocław is:

- Battery cell plant → `projectType: cell`, `sector: Batteries` ✓
- Not upstream mining or refining ✓
- Greenfield (built on former General Motors site but operationally new) ✓

Scope confirmed. Proceed.

## Step 2 — Seed the candidate

Open a blank record object. Fill in what you know from the initial prompt:

```
name: LG Energy Solution Wrocław
company: LG Energy Solution
country: POL
city: Wrocław
sector: Batteries
projectType: cell
```

Don't write anything else yet. You need evidence.

## Step 3 — Dedup check (critical)

Before any web search, run the dedup protocol from `references/dedup-protocol.md`.

1. **BNEF check.** Load `projects/nzipl/data/nzipl_bnef_projects.json`. BNEF is Mexico-only; Wrocław won't be there. Quick visual scan confirms: no match.
2. **FDI check.** Open `projects/nzipl/FDI_Combined.xlsx`. Search Battery rows with company `"LG"` and destination country Poland. This may return a row. If it does, capture the row number and tag the candidate `update-fdi`. If not, tag `new`.

For this walkthrough, assume FDI has a matching row (likely — LG Chem Wrocław is a famously large FDI event). Say it's row 147. Log:

```
sources.fdi_origin = "FDI_Combined.xlsx:row=147"
```

## Step 4 — Primary source hunt

Start at the company's own domain. Open `lgensol.com/en/press` and look for the original Wrocław announcement. The company spun off from LG Chem in December 2020, so:

- Pre-2020 → announcements live in LG Chem archives
- Post-2020 → LG Energy Solution's own IR page

You find an October 2017 LG Chem press release announcing 1.2 GWh capacity, $1.63B investment. Save the URL. This is one primary source.

Log to `aliases`: `["LGES Wroclaw", "LG Chem Wroclaw"]`. This catches the rename.

## Step 5 — Independent news source

Search Reuters for the 2017 announcement:

```
"LG Chem" Wroclaw battery factory 2017
```

Reuters piece from Oct 2017 confirms the announcement, quotes a named LG Chem executive, corroborates the investment figure. Save the URL. Two sources so far.

## Step 6 — Government / incentive filing

Poland publishes investment decisions via PAIH (Polish Investment and Trade Agency). Search:

```
site:paih.gov.pl "LG Chem" OR "LG Energy Solution" Wroclaw
```

You find a press release documenting Lower Silesia's regional economic development package and EU state-aid clearance. Save the URL. That's your third, independent, primary-ish source. **Three sources.**

Also useful: Lower Silesian Voivodeship's `umwd.dolnyslask.pl` for permit-level detail.

## Step 7 — Capacity and revised figures

The original 2017 figure was $1.63B. Current figures are much larger — capacity expanded through 2020, 2022, 2023 rounds. Find each revision:

- 2020 Reuters: expansion to 65 GWh, investment now $3.4B
- 2023 Electrive: expansion to 90 GWh, cumulative investment $5B

Build `investmentM_history`:

```json
"investmentM_history": [
  {"date": "2017-10-01", "valueM": 1630, "source": "https://www.lgchem.com/..."},
  {"date": "2020-06-01", "valueM": 3400, "source": "https://www.reuters.com/..."},
  {"date": "2023-01-01", "valueM": 5000, "source": "https://electrive.com/..."}
]
```

`investmentM` headline value: `5000` (most recent verifiable).

## Step 8 — Status and dates

From sources:
- `announced: "2017-10"` (source: LG Chem press release, month only)
- `prodStarted: "2018-Q1"` (source: Reuters; quarter-precision acceptable)
- `status: "Operating"` — *verify explicitly*. Find a 2024 piece on Electrive confirming active production. Without this, you'd have to downgrade to Tier 2 because the status × tier rule (`verification-protocol.md`) says Operating requires Tier 1.

## Step 9 — Coordinates

Wrocław facility is in the Kobierzyce industrial park. Get coordinates from:
- OpenStreetMap directly
- Wrocław city portal geodata
- Google Maps if the facility has a registered address

Lat/lng: `51.0843, 16.9253`. Source: city geoportal. (Within 5 km of Wrocław city center, passes the `checklist.md` test.)

## Step 10 — Jobs

Announced jobs target: 10,000 (multiple Reuters pieces, Invest Wrocław portal). Current: roughly 8,000 (Electrive 2024 report). Some uncertainty between sources — use the most recent verifiable figure.

## Step 11 — Assign tier

Count independent sources (excluding `fdi_origin` and `bnef_origin` — those are dedup receipts, not citations):

- LG Chem 2017 press release (primary)
- Reuters 2017 (independent news)
- PAIH Poland 2017 (government)
- Reuters 2020 (independent news, revision)
- Electrive 2023 (trade press, revision)
- Electrive 2024 (trade press, status)

Six independent URLs across `sources.*`. Well past the three-source Tier 1 minimum. Primary source present. Status "Operating" supported by 2024 coverage.

**Tier 1.** ✓

## Step 12 — Checklist run

Open `references/checklist.md` and walk every item. Critical ones to verify:

- [x] `id = EV-POL-0001` (first Poland record, zero-padded)
- [x] `region = "Europe"`
- [x] `postIRA = false` (announced 2017, pre-IRA)
- [x] `status = Operating` allowed at Tier 1
- [x] `productionUnits = "GWh/year"` because `targetProduction` is set
- [x] `license = "CC-BY-4.0"`
- [x] `verifiedBy = "A. Rojas"` (your name)
- [x] `verifiedDate = "2026-04-24"`
- [x] Three+ distinct citation URLs populated

## Step 13 — Red-flag sweep

Open `references/red-flags.md`. For Wrocław, all flags clear:

- Not MOU-only: actual operating plant with groundbreaking in 2017
- Not stale-announcement vaporware: news coverage spans 7+ years
- Not single-source PR-wire: multiple independent named-author pieces
- No shell-company obfuscation: LG Energy Solution is the direct operator
- Rename handled via `aliases`

## Step 14 — Write record

Append to `projects/nzipl/data/nzipl_ev_greenfield_global.json`. Use a tool that preserves readable indentation. Re-read the file after write to verify it parses.

## Step 15 — Update progress

Edit `tasks/ev-greenfield-poland-progress.json`:

```json
{
  "task": "EV Greenfield Poland",
  "total_target": 20,
  "candidates_found": 1,
  "tier1": 1,
  "tier2": 0,
  "tier3": 0,
  "dropped": 0,
  "dedup_new": 0,
  "dedup_update_fdi": 1,
  "next_candidate": "Stellantis-LGES Gliwice (investigating)",
  "last_updated": "2026-04-24",
  "last_operator": "A. Rojas",
  "batches": [
    {
      "date": "2026-04-24",
      "records_added": 1,
      "notes": "LG Energy Solution Wrocław. Matched FDI row 147. Tier 1. Used 2017 LG Chem PR, Reuters, PAIH, and 2023/2024 Electrive for revision history."
    }
  ]
}
```

## Step 16 — Log discoveries

Two findings worth a one-liner in `discoveries.md`:

```
- 2026-04-24 | A. Rojas | PAIH Poland publishes investment decisions with EU state-aid clearance detail; great Tier-A source for Polish projects [ev-greenfield]
- 2026-04-24 | A. Rojas | Korean company name history matters: LG Chem → LG Energy Solution spin-off Dec 2020; always include both in aliases [ev-greenfield]
```

If a fellow Lab member extends this to Samsung SDI or SK On, they'll know.

## What took time vs. what was mechanical

Read this next-steps summary critically: it's the part most new Lab members underestimate.

- **Mechanical (~20 min):** the schema fields, the dedup lookup, the checklist, the write.
- **Judgment-heavy (~40 min):** deciding the status based on 2024 evidence, reconciling the three investment figures into `investmentM_history`, confirming the rename chain, checking whether the FDI row is the same project or a related LG Chem facility.

Your first records will take 2+ hours each. By record 10 you'll be at 45 minutes. By record 20, 20-30 minutes each with a pair-review bottleneck.

## Where to stop

The record is done when the checklist passes. Don't keep searching for more sources — diminishing returns kick in at four or five citations. Move to the next candidate. Weekly re-verification (per `verification-protocol.md`) catches anything that changes.

## If this were Tier 2 instead

Same record, fewer sources: imagine only the 2017 LG Chem PR and one Reuters piece. Two sources, both at announcement time, no government filing.

- Cannot be Tier 1 (need three sources including a primary + corroborator + independent).
- Cannot be `Operating` at Tier 2 (status × tier rule).
- Must change status to `Planned` or `Announced`, and log tier 2.

Re-verify in 60 days — by then a government filing or trade-press groundbreaking piece often surfaces and you can upgrade.

---

# Search playbook

Query templates by country and source type. Copy-paste into your search engine of choice (prefer the country's native engine when it exists — Naver for Korea, Baidu for China, Google.de for Germany, etc.).

## Query primitives

Every search starts from one of these primitives, combined with quotation marks for the company name:

1. `"<Company>" <project-type> <city> <country>`
2. `"<Company>" <project-type> factory site:<company-domain>`
3. `"<Company>" <project-type> "<city>" -site:wikipedia.org`
4. `"<Company>" <project-type> permit <state/province>`
5. `"<Company>" <project-type> groundbreaking <year>`
6. `"<Company>" <project-type> announcement <year>` (limit to a year to filter stale coverage)

Project-type keywords: `battery`, `cell`, `gigafactory`, `EV`, `cathode`, `anode`, `separator`, `electrolyte`, `recycling`, `assembly`, `motor`, `inverter`, `charger`.

## Country playbooks

### United States

Start with Atlas EV Hub. Then:

```
site:energy.gov "<Company>" "<State>"
site:selectusa.gov "<Company>"
site:<state>.gov "<Company>" tax incentive
"<Company>" "<City>" permit application
```

Key state agency domains:
- `gadc.georgia.gov` (Georgia)
- `michiganbusiness.org` (Michigan)
- `tnecd.com` (Tennessee)
- `texaswideopenforbusiness.com` (Texas)
- `ided.state.ia.us` (Iowa)
- `thinkkentucky.com` (Kentucky)

### Mexico

Start with `nzipl_bnef_projects.json` — 37 Mexican records already in hand. Then:

```
site:gob.mx/se "<Empresa>"
site:gob.mx "<Ciudad>" inversión
"<Company>" planta <ciudad> México
"<Empresa>" "<Estado>" nave industrial
```

The Secretaría de Economía publishes press releases on `gob.mx/se/prensa`. State-level: Nuevo León's `nl.gob.mx`, Coahuila's `coahuila.gob.mx`. Industrial parks: AMPIP `ampip.org.mx`.

### Germany

```
site:bmwk.de "<Company>"
site:gtai.de "<Company>"
"<Company>" Werk "<Stadt>"
"<Company>" Batteriewerk OR Zellfertigung "<Stadt>"
site:brandenburg.de OR site:sachsen.de OR site:nrw.de "<Company>"
```

Tier A German sources: BMWK, GTAI (Germany Trade & Invest), state economy ministries. Tier B: Handelsblatt, Süddeutsche, Tagesschau, Electrive.de, Battery-News.de.

### Hungary

```
site:kormany.hu "<Company>"
site:hipa.hu "<Company>"
"<Company>" gyár "<Város>"
```

HIPA (Hungarian Investment Promotion Agency) is the authoritative source. CATL Debrecen, BYD Szeged, Samsung SDI Göd all appear there first.

### Poland

```
site:paih.gov.pl "<Company>"
"<Company>" fabryka "<Miasto>"
"<Company>" Wrocław OR Gliwice OR Poznań
```

PAIH (Polish Investment and Trade Agency) is the national source.

### Spain

```
site:investinspain.org "<Company>"
"<Company>" fábrica "<Ciudad>"
"<Company>" planta baterías "<Región autónoma>"
```

### France

```
site:businessfrance.fr "<Company>"
"<Company>" usine "<Ville>"
"<Company>" gigafactory "<Région>"
```

### Turkey

```
site:invest.gov.tr "<Company>"
"<Company>" fabrika "<Şehir>"
"<Company>" elektrikli araç tesisi
```

### South Korea

Outbound investments (Korean firms building overseas) — always check Korean-language sources first.

```
site:motie.go.kr "<Company>" "<Country>"
site:investkorea.org "<Company>"
"<Company-hangul>" 배터리 공장
"<Company-hangul>" 셀 공장 "<City-transliteration>"
```

The Elec (`thelec.net`) is the best English-language source. Names to translate: LG에너지솔루션 (LG Energy Solution), 삼성SDI (Samsung SDI), SK온 (SK On), 포스코퓨처엠 (POSCO Future M), 에코프로 (Ecopro).

### Japan

```
site:meti.go.jp "<Company>"
site:jetro.go.jp "<Company>"
"<Company-kanji>" 工場 "<Prefecture>"
"<Company-kanji>" EV 工場
```

Nikkei Asia is the English source. Local press in Japanese: NHK, Asahi, Nikkei Japan. Companies to translate: パナソニック (Panasonic), トヨタ (Toyota), ホンダ (Honda), 日産 (Nissan), デンソー (Denso), AESC.

### China

```
site:miit.gov.cn "<Company-hanzi>"
site:ndrc.gov.cn "<Company-hanzi>"
"<Company-hanzi>" 工厂 "<City-hanzi>"
"<Company-hanzi>" 电池 新基地
```

CnEVPost is the best English-language aggregator. Transliteration traps: 比亚迪 (BYD), 宁德时代 (CATL), 亿纬锂能 (EVE Energy), 国轩高科 (Gotion), 蜂巢能源 (SVOLT), 孚能科技 (Farasis).

### India

```
site:investindia.gov.in "<Company>"
site:heavyindustries.gov.in "<Company>"
"<Company>" plant "<City>" battery OR EV
"<Company>" gigafactory India
```

PLI (Production Linked Incentive) scheme notifications on `heavyindustries.gov.in` are the authoritative source for Indian battery investments. Key names: Tata, Ola Electric, Mahindra, Ather, Reliance, Amara Raja, Exide.

### Brazil

```
site:gov.br/mdic "<Company>"
site:apexbrasil.com.br "<Company>"
"<Company>" fábrica "<Cidade>"
"<Company>" planta "<Estado>"
```

BYD São Paulo, Great Wall Motor Iracemápolis, Stellantis Betim. Valor Econômico and Automotive Business are the best trade press.

### Canada

```
site:ised-isde.canada.ca "<Company>"
site:invest.gc.ca "<Company>"
"<Company>" "<City>" battery plant
"<Company>" strategic innovation fund
```

Federal Strategic Innovation Fund disclosures are authoritative. Key locations: Windsor (Stellantis–LGES NextStar), Bécancour (Quebec battery cluster).

## Query anti-patterns

Avoid these:

- **Date-bounded "<Company> 2024"** alone — too noisy. Pair with project-type and geography.
- **Generic "battery plant <country>"** — returns aggregator listicles. Start with the company.
- **Relying on Wikipedia infobox numbers** — they lag real announcements by months and often cite the largest announced figure, not the current one.
- **Using the first result uncritically** — the first hit is usually a press release repackaged by a wire service. Check the original company domain.

## Dead-end recovery

When a search returns nothing useful:

1. **Switch language.** If the company is Asian or European, try the native-language query.
2. **Narrow on permits.** `"<Company>" "<State/Province>" "permit" OR "incentive" OR "grant"`.
3. **Widen to the parent.** If the facility operator is a subsidiary, search the parent company.
4. **Check supplier announcements.** Equipment vendors (Manz, Wuxi Lead, Schuler) announce plant orders. These often confirm a plant exists even when the operator hasn't publicized it.
5. **Check construction contractor announcements.** Bechtel, M+W Group, Exyte regularly announce battery-plant contracts.
6. **Check city-level economic development news.** "Site selection" trade press (areadevelopment.com, businessfacilities.com) covers announcements the company doesn't heavily promote.
7. **Last resort: log the candidate at Tier 3** with the single source and revisit in 30 days.

## Logging searches

When you find a genuinely new source type or a useful query pattern — especially a local-language query that unlocked a difficult record — append it to `discoveries.md`. The playbook gets smarter over time. Significant patterns get promoted into this file via PR.

---

# Common mistakes

Append-only log of mistakes Lab members have made while gathering EV greenfield records. Follows the same pattern as `discoveries.md` at the kit root — one line per entry, most recent at the top. Read before each batch. Add a line every time you discover you made (or nearly made) a mistake, so the next researcher doesn't repeat it.

## Format

```
- YYYY-MM-DD | Name | One-line description of the mistake and how to avoid it [tags]
```

Tags: `[tier]`, `[dedup]`, `[scope]`, `[source]`, `[schema]`, `[currency]`, `[locale]`.

## Seed entries (from protocol design)

These are mistakes worth anticipating before the first real batch. Delete or expand as real patterns emerge.

- 2026-04-24 | Gilberto | Tier 2 inflation: counting three URLs that are all reproductions of one press release as "three sources". Require that at least one source be independently authored (not derived). [tier] [source]
- 2026-04-24 | Gilberto | Using the largest announced investment figure instead of the most recent — some projects are revised downward after initial announcements. Track all revisions in investmentM_history. [currency]
- 2026-04-24 | Gilberto | Confusing MWh storage capacity with annual GWh throughput. targetProduction is per-year, not cumulative nameplate. [schema]
- 2026-04-24 | Gilberto | Writing parent HQ country (origin) as destination country. Example: Tesla is USA, but Tesla Giga Berlin's country is DEU. [schema]
- 2026-04-24 | Gilberto | Skipping Korean / Chinese / Japanese sources for projects with Asian parents. The English press lags — usually by days to weeks. Use the search-playbook language queries. [locale] [source]
- 2026-04-24 | Gilberto | Treating a Phase 2 expansion as a new record instead of updating the existing record's investmentM_history and targetProduction. Check coordinates and existing records before creating new ones. [dedup]
- 2026-04-24 | Gilberto | Marking a project "Operating" based on a single 2024 trade-press mention. Status "Operating" requires explicit confirmation (company PR, annual report, or named-author piece describing current production). [tier]
- 2026-04-24 | Gilberto | Recording an MOU as status "Planned" at Tier 1. MOUs are Tier 3, status "Announced" at most. Require a permit filing or groundbreaking date for higher status. [tier] [scope]
- 2026-04-24 | Gilberto | Citing paywalled FT/Bloomberg articles without finding the Reuters/Nikkei free mirror. The public-citable policy requires public URLs. [source]
- 2026-04-24 | Gilberto | Using a fabricated URL when a search returns nothing. Leave the field empty rather than inventing a citation. [source]
- 2026-04-24 | Gilberto | Forgetting to update aliases when a company renames (LG Chem → LG Energy Solution, FCA+PSA → Stellantis, Contemporary Amperex → CATL). The dedup protocol depends on this. [dedup]
- 2026-04-24 | Gilberto | Treating pack assembly plants as cell factories. They're scope-valid but go under projectType: pack, not cell — critical for capacity math. [scope] [schema]

## Promotion

When a mistake keeps appearing (three+ entries of the same pattern), promote it to `references/red-flags.md` as a permanent red flag and remove the log entries. Use a PR per `CONTRIBUTING.md`.

## What NOT to log here

- One-off typos in a specific record (fix the record, move on)
- Tool-specific frustrations unrelated to methodology (log in `discoveries.md` or `gotchas.md`)
- Pattern observations that aren't actionable mistakes (those go in `discoveries.md`)
