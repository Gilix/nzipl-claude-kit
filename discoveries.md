# Discoveries

The Lab's collective knowledge log. When you learn something that would make a colleague's Claude session smarter, add it here. This covers anything worth sharing:

- A data source you found useful
- An API behavior (working or broken)
- A methodology insight or pattern that worked
- A reusable command or pipeline you built
- A gotcha that cost you time

Significant entries get promoted to `gotchas.md` or `glossary.md` during periodic reviews.

## Schema

Each entry is one line:

```
- YYYY-MM-DD | Author | Finding text [pipeline:X] [deliverable:X] [ref:PR#N]
```

### Required
| Field | Position | Format |
|-------|----------|--------|
| Date | 1st | YYYY-MM-DD |
| Author | 2nd | First name or handle |
| Finding | 3rd | One-line description of what was learned |

### Optional tags (append after finding text)
| Tag | Values (extend as needed) | Example |
|-----|--------------------------|---------|
| `[pipeline:X]` | `enrichment`, `playcard`, `rca`, `denue`, `parks`, `energy`, `trade` | `[pipeline:enrichment]` |
| `[deliverable:X]` | `play-cards`, `constraint-maps`, `chart-packs`, `infra-map`, `platform` | `[deliverable:play-cards]` |
| `[ref:X]` | PR number, issue, or commit hash | `[ref:PR#15]` |

Tags are optional. An untagged entry is still valid.

Append and push. No PR needed.

## Log

- 2026-04-07 | Gilberto | DataMexico /data endpoint silently drops manufacturing sectors 31-33; use /stats/rca with multi-month parameter instead [pipeline:denue]
- 2026-04-07 | Gilberto | OEC requires browser User-Agent header (Cloudflare); requests without it return empty responses or 403 [pipeline:trade]
- 2026-04-07 | Gilberto | Mexico BACI country ID is "namex" not "mexxx" in trade_i_baci_a_22 [pipeline:rca]
- 2026-04-07 | Gilberto | HS6 870839 (braking systems) missing from baci_a_22; fall back to baci_a_02 with year=2024 [pipeline:playcard]
- 2026-04-07 | Gilberto | Municipality HS4 IDs in DataMexico include chapter prefix (e.g., 20702); extract last 4 digits for actual HS4 code [pipeline:rca]
- 2026-04-08 | Gilberto | FDI enrichment: one web search per row covers 5-7 of 8 source columns; don't search per-column [pipeline:enrichment]
- 2026-04-08 | Gilberto | FDI enrichment: sort by investment size descending; projects >$1B have near-100% press coverage, <$100M drops off sharply [pipeline:enrichment]
- 2026-04-08 | Gilberto | FDI enrichment: Battery post-2020 covered by electrive, InsideEVs, Battery-News; Solar by PV Magazine, PV Tech, Renewables Now; Wind coverage thinner [pipeline:enrichment]
- 2026-04-08 | Gilberto | FDI enrichment: fDi Markets investment figures sometimes include projected multi-phase totals; press releases cite initial phase only (e.g., LG/GM Spring Hill: $3.2B fDi vs $2.575B press) [pipeline:enrichment]
- 2026-04-08 | Gilberto | FDI enrichment: Column T (ownership share) and V (completion date) are hardest to source; skip on first pass if initial search misses them [pipeline:enrichment]
- 2026-04-24 | Gilberto | EV greenfield Germany: `invest-in-thuringia.de` is a high-quality Tier A source for Thuringia projects (CATL Arnstadt, Kedali Erfurt, Stellantis Eisenach) — curated company profiles with start dates, capacity, jobs [pipeline:gather-ev-greenfield]
- 2026-04-24 | Gilberto | EV greenfield Germany: FDI row 86 labelled "CATL Kirchardt" is actually the Valmet Automotive Kirchardt battery pack plant — CATL holds a 23.08% stake in Valmet. Naming in FDI reflects the upstream investor, not the operator. Match dedup on geography + activity type, not just company name [pipeline:gather-ev-greenfield]
- 2026-04-24 | Gilberto | EV greenfield Germany: 3 of the top 5 largest projects are cancelled — Northvolt Heide (Chapter 11 Nov 2024, sold to Lyten June 2025), SVOLT Überherrn (SVOLT withdrawal from Europe Jan 2025), ACC Kaiserslautern (definitively shelved Feb 2026). 2024-2026 European battery capex reversal; re-verify German cell projects quarterly [pipeline:gather-ev-greenfield]
- 2026-04-24 | Gilberto | EV greenfield Germany: CATL's German footprint is three-plant (Arnstadt cell mfg, Bad Friedrichshall R&D, Munich R&D) plus minority-held Valmet Kirchardt. R&D-only sites are out of greenfield manufacturing scope; drop FDI rows 87 and 88 rather than record them [pipeline:gather-ev-greenfield]
- 2026-04-24 | Gilberto | EV greenfield Germany: VW Group has 4 distinct German EV-related greenfield records — Salzgitter (cell, PowerCo), Zwickau (vehicle, MEB conversion), Emden (vehicle, MEB conversion), Wolfsburg (Trinity cancelled). Don't consolidate; treat each as a separate facility with its own capex [pipeline:gather-ev-greenfield]
- 2026-04-24 | Gilberto | EV greenfield Germany: "Electrive.com" is the single most productive named-author source for German EV projects — covers both primary announcements and status changes; cite under `status` for Tier-1 status confirmation. Battery-News.de is the fastest but has fewer English-language pieces [pipeline:gather-ev-greenfield]
