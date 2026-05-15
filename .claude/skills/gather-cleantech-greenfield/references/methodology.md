# Methodology rationale

This document explains the design choices behind the gather-cleantech-greenfield skill: why one omnibus skill across four technologies, why the per-tech matrices live in code, why per-tech-per-country output files, and how the skill resolves conflicts between company, government, and independent-press sources. Read alongside `verification-protocol.md`, which states the rules, and the `validate_cleantech_record.py` script, which enforces them.

The cleantech skill is the second instance of this discipline at the Lab. The first is `gather-ev-greenfield`. The two skills share design DNA: same tier matrix, same status × tier rule, same forbidden-domain blocklist, same auto-derived fields. Where they diverge — projectType enums, productionUnits, dataset path, ID prefix — the divergence is technology-specific and lives in code. The shared design rationale is documented at length in `gather-ev-greenfield/references/methodology.md`. This document covers what is specific to cleantech.

## Why one omnibus skill across four technologies

A family of per-tech skills (one for solar, one for wind, etc.) was the obvious alternative. The reason to consolidate into one skill is that the failure modes are tech-specific but the response patterns are nearly identical. A new red flag found in solar (polysilicon vaporware) is structurally the same kind of warning as a new red flag found in hydrogen (MOU-only). When both live in one skill, the cross-tech learning compounds — a sentence in `red-flags.md` covers both. Per-tech skills would force the same insight to be duplicated four times and would risk drifting versions.

The cost is that the skill description has to mention four technologies and four invocation patterns. That cost is paid once, in `SKILL.md`. The benefit — single methodology, single validator, single source catalog — accumulates per record and per discovery.

## Why per-tech-per-country output files

The EV skill writes to one global JSON file. Cleantech instead splits into `cleantech_greenfield/<tech>/<ISO3>.json`. Three reasons.

**File size at saturation.** Solar alone has on the order of 2,000+ greenfield announcements globally over the past five years. A single global JSON for all four techs would grow to tens of MB and become slow to read, write, and diff. Per-tech-per-country files cap any individual file at a reasonable size — a few hundred KB at most.

**Concurrent edits.** When two Lab members are working in parallel — one adding solar records for Germany, one adding wind records for the US — they touch different files. Merge conflicts collapse from "everyone editing the same array" to "everyone editing their own slice."

**Path-derived integrity.** Splitting by tech and country makes the dataset self-checking. The validator compares a record's ID prefix (`SOL`/`WND`/`HYD`/`HPU`) and ISO-3 segment against the file path. A record placed in the wrong file is caught at write time, not at consumption time.

The cost is that a downstream consumer who wants the full dataset has to glob and concatenate. That's a five-line script. The integrity and concurrency benefits are durable.

## Why a `tech` field even though it's encoded in the ID prefix

Redundancy on purpose. The ID prefix is a string convention; the `tech` field is a typed enum. The validator confirms they agree, which catches both typos in the ID and category errors in the schema. Downstream consumers can filter on `tech` without parsing the ID. The cost (one extra field per record) is trivial; the benefit (immediate filterability + dual-coded consistency) is real.

## Why per-tech projectType enums

Solar polysilicon and wind blades have nothing in common. A flat `projectType` enum that lists every valid option across all techs would lose the most useful constraint — that `polysilicon` only makes sense paired with `tech: solar`. The `(tech, projectType)` matrix in code makes that constraint mechanical. A researcher who tries to write `tech: solar, projectType: blade` gets an explicit validator error, not a silent acceptance.

The matrix grows organically. When a new technology variant emerges (e.g., perovskite tandem cells, or floating offshore foundations distinct from fixed), add the value to the matrix in `validate_cleantech_record.py`, document it in `schema.md`, and propagate any new red flags. The validator is the single source of truth for what's allowed.

## Why hydrogen has the strictest red flags

Hydrogen has the highest ratio of announced projects to FID-stage projects of any cleantech sector. The 2022–2024 wave of hydrogen MOUs and "hub" announcements has produced more vaporware per dollar than any other tech in living memory. The skill's response is to default hydrogen records to Tier 3 unless the company has publicly disclosed FID, and to require company-side confirmation (not just government-side or partner-side) before upgrading. This is heavier discipline than solar or wind, and intentional.

## Why heat pumps have a brand-vs-OEM red flag

Unlike solar / wind / hydrogen, where the announcing company is usually the operator, the heat-pump industry has heavy use of licensed contract manufacturing. A "Daikin plant in <state>" can mean (a) a Daikin-owned Goodman subsidiary plant, (b) a third-party OEM building Daikin-branded units, or (c) a future plant where Daikin will license its IP to a partner. These are very different signals. The skill's red flag is to record the operator, not the brand, in `company`, and to put the brand in `aliases`.

## Why scope excludes EVs and upstream extraction

Two boundaries: one with `gather-ev-greenfield`, one with the upstream commodities universe.

**vs `gather-ev-greenfield`.** EVs, batteries, and charging belong in the EV skill. They have their own dataset, their own seed list, their own dedup target (the Mexico BNEF snapshot). Cross-coupling would create dedup ambiguity: is a battery cell plant for EV use also a "fuel cell" project under cleantech? No — it's an EV record. Sharp scope rule: EV / battery / charging → EV skill; everything else clean → cleantech skill.

**vs upstream extraction.** Lithium brine, nickel mining, polysilicon precursor chemistry, copper smelting, fossil-feedstock hydrogen — these are different industries with different financing, different permits, different supply chains, and different stakeholders. Including them would dilute the dataset's signal. A clean industrial-policy lens needs to distinguish "manufacturing of clean technology equipment" from "extraction of inputs feeding all manufacturing." This skill draws that line at the manufacturing boundary.

## Extending the skill to a fifth technology

When the Lab adds a new technology family (CCUS / nuclear / geothermal / biofuels), extend in this order:

1. Add the tech to the `TECHS` set, `TECH_PREFIX` map, and `TECH_PROJECT_TYPES` matrix in `validate_cleantech_record.py`.
2. Add per-projectType `productionUnits` to the `PROJECT_TYPE_UNITS` matrix.
3. Update the schema in `references/schema.md`.
4. Add tech-specific red flags to `references/red-flags.md`.
5. Add Tier-A sources to `references/sources.md`.
6. Add country query templates to `references/appendix/search-playbook.md`.
7. Create the empty output directory: `cleantech_greenfield/<new-tech>/`.

A new tech is roughly half a day of curation. Don't add a tech without committing to the seed-list growth and the red-flag discipline. A new tech with no red flags and no seed is worse than no tech.
