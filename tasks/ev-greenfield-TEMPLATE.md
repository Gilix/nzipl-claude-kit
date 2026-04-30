# Task: EV Greenfield — <COUNTRY or SCOPE>

> **Training mode only.** Production runs of the `gather-ev-greenfield` skill skip this template — they go straight from candidate seeding to validator-enforced write. Use this file only when onboarding a new Lab member or when `target_count <= 20` and the user wants process overhead.
>
> Copy to `tasks/ev-greenfield-<country>.md` and copy `ev-greenfield-TEMPLATE-progress.json` to the matching `-progress.json`.

## Assignee and scope

- **Assignee:** <Lab member name>
- **Scope:** <country, region, or topical subset — e.g., "Germany EV cell plants, 2020–2026">
- **Target count:** <20 for training cycle, 100+ for production cycle>
- **Priority:** <largest-investment-first | newest-first | country-native-first>
- **Start date:** <YYYY-MM-DD>
- **Target finish date:** <YYYY-MM-DD>

## What this task is

Gather and verify EV greenfield manufacturing records for the assigned scope. Write verified records to `projects/nzipl/data/nzipl_ev_greenfield_global.json` following the `gather-ev-greenfield` skill protocol.

Records include: battery cells/packs, EV assembly, cathode/anode/separator/electrolyte plants, motors/inverters, recycling, charging equipment. Out of scope: upstream mining and refining.

## How to run it

From a Claude Code session opened in `nzipl-claude-kit/`:

1. Read the skill: `.claude/skills/gather-ev-greenfield/SKILL.md` and every file in `references/`. Budget 45–60 minutes.
2. Invoke the skill with your scope: *"Gather EV greenfield investments in <scope>"*.
3. Claude will walk through: candidate seeding → dedup → verification → record write → progress update. You review every tier and source.

## Sources to prioritize

See `references/sources.md`. For this task specifically, emphasize:

- <list any country-specific gold sources, e.g., BMWK / GTAI for Germany>
- <list any local-language queries likely to be needed>
- <note any BNEF / FDI rows likely to match this scope>

## What "done" looks like

- Target record count hit.
- Every record has `verificationTier`, `verifiedBy`, `verifiedDate`, `license`, and at least one `sources.*` URL.
- Operating / Under-Construction records are all Tier 1.
- First 5 records pair-reviewed.
- Task progress JSON counters reconcile with records in global JSON.
- Any novel findings logged to `discoveries.md` or `references/common-mistakes.md`.

## How to QA each batch

1. **Spot-check 10% of URLs.** Open them. Confirm:
   - URL resolves.
   - Article mentions the company and project.
   - Claimed data point (investment, date, location) appears in the article.
2. **Check status × tier.** Any Operating / Under-Construction at < Tier 1 must be fixed.
3. **Run dedup receipts.** Every `update-bnef` and `update-fdi` candidate must have the corresponding origin receipt in `sources`.
4. **Scan for red flags.** Walk `references/red-flags.md`. Any hit = demote or drop.
5. **Reconcile counters.** Progress JSON counts should equal records matching this task's scope in the global JSON.

## Edge cases

| Situation | What to do |
|-----------|-----------|
| Candidate is in BNEF but only has Mexico data | Search BNEF `aliases` and parent-company relationships; BNEF's 37 are Mexico-focused but parent companies (BMW, Tesla, Solarever) have records elsewhere |
| Candidate in the proprietary fDi Markets workbook | That's a separate `/enrich-fdi` workstream. Do NOT dedup against it here and do NOT copy `fdi_origin` receipts into the global JSON |
| Company renamed / restructured mid-project | Current name goes in `company`, prior names in `aliases`; pick the most recent announcement as primary |
| Project announcement uses local currency | Convert to USD at announcement-date FX; annotate in `investmentM_history.original` |
| Only source is a paywalled FT / Bloomberg / Nikkei article | Find the free mirror (Reuters, Yahoo, local-language syndication) or downgrade tier |

## Pair review

The first 5 records on this task must be pair-reviewed by a second Lab member before you proceed to record 6. Reviewer checks:

- Tier is justified by sources (not inflated)
- Status × tier rule holds
- No red flags missed
- Schema compliant

Log the reviewer's name and date at the top of the progress file batch entry.

## Progress tracking

Live state is in `tasks/ev-greenfield-<country>-progress.json`. Update after each batch:

- Top-level counters: `candidates_found`, `tier1`, `tier2`, `tier3`, `dropped`, `dedup_new`, `dedup_update_bnef`, `dedup_update_fdi`, `dedup_update_both`, `dedup_skipped`.
- `next_candidate`: so whoever resumes the task knows where to start.
- `last_updated`, `last_operator`.
- Append a batch entry with date, records added, tier breakdown, operator, reviewer (if applicable), and freeform notes.

## Closing the task

When target count hit and QA complete:

1. Final check: counters in progress JSON reconcile with records in global JSON for this scope.
2. Update the Tasks table in `CLAUDE.md` — change status from "In progress" to "Complete".
3. Promote any recurring mistakes logged in this task to permanent entries in `references/common-mistakes.md` (or `references/red-flags.md` / `gotchas.md` if significant).
4. Leave the task and progress files in place as the audit trail. Do not delete.
