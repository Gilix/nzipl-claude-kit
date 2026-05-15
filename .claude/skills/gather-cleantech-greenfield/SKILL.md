---
name: gather-cleantech-greenfield
description: "Grow and maintain the Lab's global clean-tech FDI dataset across solar PV, wind, hydrogen / electrolyzers, and heat pumps. Use when the user asks to gather, verify, audit, or extend greenfield manufacturing records — solar polysilicon/wafer/cell/module/inverter plants, wind turbine/blade/tower/nacelle plants, electrolyzer / fuel-cell / green-ammonia / e-methanol facilities, heat-pump assembly — anywhere in the world. Primary invocation is gap-filling: 'add N cleantech records', 'add 5 solar greenfield records for Germany', 'verify the next 10 wind announcements'. Also handles single-record verification and stale-record audits. Out of scope: EV / batteries (use gather-ev-greenfield instead) and upstream mining / refining. Writes to projects/nzipl/infra-mx/data/cleantech_greenfield/<tech>/<ISO3>.json, enforced by data/validate_cleantech_record.py."
---

# Gather Cleantech FDI

Maintain a global, publicly-citable dataset of greenfield manufacturing investments across four clean technologies: **solar PV, wind, hydrogen / electrolyzers, heat pumps**. Each record carries a `tech` field; cross-border (`origin ≠ country`) records are tagged `isFDI: true`; domestic investments are tagged `isFDI: false`. Both are in scope.

**Out of scope:**
- EV / batteries / charging — use `gather-ev-greenfield` instead.
- Upstream extraction: lithium / nickel / cobalt mining, polysilicon precursor chemistry, rare-earth refining, hydrogen feedstock production from natural gas without CCUS, copper smelting.
- Grid hardware (transformers, switchgear, HV cables) — separate workstream.

## Primary invocation: gap-fill

> "Add 20 cleantech records." "Add 5 solar greenfield records for Germany." "Fill the next 15 hydrogen gaps." "Extend with recently-announced wind projects."

1. **Pick tech + scope.** From the user ask, identify which tech (`solar` / `wind` / `hydrogen` / `heatpumps`) and any country / company filter.
2. **Load state** — read every `projects/nzipl/infra-mx/data/cleantech_greenfield/<tech>/*.json` file in scope. Read the matching seed (`data/seeds/<tech>_seed.json`) if non-empty.
3. **Pick gaps** — prefer seed candidates not yet present in the global dataset, prioritized by `investmentM` and country coverage (avoid over-indexing on any single country unless the user asks). If seed is empty or exhausted, search trade press for the last 12 months — see `references/sources.md` for Tier-A outlets per tech and `references/appendix/search-playbook.md` for query templates.
4. **Verify** — for each candidate, gather sources per `references/verification-protocol.md`. Minimum 1 URL; Tier 1 needs 3 distinct citation URLs.
5. **Write + validate** — append each record to the correct file: `cleantech_greenfield/<tech>/<ISO3>.json`. Sequential ID per file (`SOL-DEU-0001`, `SOL-DEU-0002`, …). Run:
   ```bash
   python3 data/validate_cleantech_record.py projects/nzipl/infra-mx/data/cleantech_greenfield/
   ```
   Exit non-zero = fix and re-run before reporting done.

## Secondary invocations

| Ask | Do |
|-----|----|
| "Verify this announcement" | Single-record: dedup, verify, write one record into the correct `<tech>/<ISO3>.json` file. |
| "Audit stale Tier 1 records" | Sample records with `verifiedDate < 90 days ago`; re-check sources; demote or update. |
| "Gather N records for <country>" | Country-scoped gap-fill: pick seed candidates with `country = <ISO-3>` across all techs (or one tech if the user names it), verify, write. |
| "Add the <Company> plant in <City>" | Identify tech from the company / project; dedup against the global dataset; verify; write. |

## ID format

`<TECH>-<ISO3>-<NNNN>`, sequential per tech-country file:

| Prefix | Tech | Example | Lives in |
|--------|------|---------|----------|
| `SOL` | solar | `SOL-DEU-0001` | `cleantech_greenfield/solar/DEU.json` |
| `WND` | wind | `WND-CHN-0001` | `cleantech_greenfield/wind/CHN.json` |
| `HYD` | hydrogen | `HYD-USA-0001` | `cleantech_greenfield/hydrogen/USA.json` |
| `HPU` | heatpumps | `HPU-FRA-0001` | `cleantech_greenfield/heatpumps/FRA.json` |

The validator enforces the ID-prefix↔tech relationship and the ID↔file-path relationship.

## Workflow constraints

- **Never cite** `wikipedia.org`, `grokipedia.com`, `linkedin.com`, `reddit.com`, `twitter.com`, `x.com`, `facebook.com`, `instagram.com`, `medium.com`. The validator hard-rejects these.
- **Never dedup against** `FDI_Combined.xlsx`. That's the separate `/enrich-fdi` workstream. Dedup target is the global dataset itself.
- **Stay in scope.** EV / battery investments belong in `gather-ev-greenfield`, not here. Upstream mining / refining is out of scope.
- **Batch search queries.** One search per 3–5 candidates, not per candidate. Group by company or country.
- **Write lean.** Required fields only; leave optional fields empty when not confirmable. Partial-correct beats speculative-complete.
- **Run the validator after every batch.** Fix errors; don't write through them.

## File structure

```
.claude/skills/gather-cleantech-greenfield/
├── SKILL.md                                  ← You are here
├── README.md                                 ← Share-package quickstart
└── references/
    ├── schema.md                             ← Schema + per-tech enums + example record
    ├── sources.md                            ← Tier A primaries per tech + forbidden domains
    ├── verification-protocol.md              ← Tier matrix + status×tier rule
    ├── red-flags.md                          ← Cross-cutting + per-tech red flags
    ├── methodology.md                        ← Design rationale
    └── appendix/
        ├── search-playbook.md                ← Query templates per tech and country
        ├── worked-example.md                 ← One worked example per tech
        └── common-mistakes.md                ← Append when you find a new recurring error

data/                                         ← Share-package mirror (production lives in infra-mx/data/)
├── validate_cleantech_record.py              ← Run before every write
├── seeds/
│   ├── solar_seed.json                       ← []
│   ├── wind_seed.json
│   ├── hydrogen_seed.json
│   └── heatpumps_seed.json
└── cleantech_greenfield/
    ├── solar/
    ├── wind/
    ├── hydrogen/
    └── heatpumps/

projects/nzipl/infra-mx/data/cleantech_greenfield/   ← Production output (consumed by play cards)
├── solar/<ISO3>.json
├── wind/<ISO3>.json
├── hydrogen/<ISO3>.json
└── heatpumps/<ISO3>.json
```

## Reading budget

Two files, ~15 minutes:
1. `references/schema.md` — fields, per-tech projectType matrix, example record
2. `references/verification-protocol.md` — tier matrix + status×tier rule

Everything else is referenced on demand.

## Defaults

| Decision | Default |
|----------|---------|
| Currency | USD millions, FX at announcement date |
| License | `CC-BY-4.0` per record |
| Paywalled sources | Allowed only with free mirror; cite the mirror |
| `isFDI` | Auto-derived: `origin ≠ country` |
| `region` | Auto-derived from `country` ISO-3 via continent lookup |
| `postIRA` | Auto-derived: `announced >= '2022-08-16'` |
| Status × tier | `Operating` / `Under Construction` / `Closed` → Tier 1 required; `Rumored` → Tier 3 required |
| Tier-1 min citations | 3 distinct citation URLs |
| Receipt keys | None at v1 (no dedup-target snapshots integrated yet) |

## Related

- `gather-ev-greenfield` — sibling skill for EV / batteries / charging. Same discipline, separate dataset and validator.
- `/enrich-fdi` — separate workstream for the proprietary fDi Markets spreadsheet. Do not couple to it.
- `nzipl-design` — apply when rendering this dataset.

## Done

- Target record count hit.
- `python3 data/validate_cleantech_record.py projects/nzipl/infra-mx/data/cleantech_greenfield/` exits 0.
- New records distributed across countries (not all one country) unless the user asked for a country-scoped batch.
- Each record has the correct `tech` field, lives in the matching `<tech>/<ISO3>.json` file, and meets its tier's citation minimum.
