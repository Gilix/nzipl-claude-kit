# Methodology rationale

This document explains the design choices behind the gather-ev-greenfield skill: why three tiers, why the status-tier matrix is enforced mechanically, and how the skill resolves conflicts between company, government, and independent-press sources. Read alongside `verification-protocol.md`, which states the rules, and the `validate_ev_record.py` script (shipped under `data/` in the skill share, or at `projects/nzipl/data/` in the NZIPL Lab repo), which enforces them.

## Why a tiered evidence scheme

A flat dataset where every record carries equal weight forces downstream users to re-derive confidence from the citations themselves. That re-derivation does not scale. By assigning a tier at write time, the skill commits to a confidence claim that propagates with the record. Visualizations, briefs, and external partners can filter by tier and trust the result.

## Why three tiers, not five

Three buckets separate three meaningful states: records the Lab will defend publicly (Tier 1), records that look real but have thin evidence (Tier 2), and records that exist as announcements or aggregator entries without independent confirmation (Tier 3). Five tiers create false precision and decision fatigue at write time. One tier loses the most useful distinction, defensible versus not. Three is the minimum granularity that does real work without inviting hair-splitting.

## Why Tier 1 requires three independent sources

Two-source records are the most common quality failure on datasets like this one. They are easy to construct from a single press release picked up by Reuters and a trade outlet, which together represent one substantive claim and two reproductions. The three-source rule forces real triangulation: at least one primary (company newsroom or government filing), at least one corroborator (permit, named-author trade coverage, or regulatory disclosure), and at least one independent news source. The validator counts distinct citation URLs across `sources.*` and rejects Tier 1 records below the threshold. The dedup receipt `bnef_origin` does not count toward the total, since it documents provenance, not evidence.

## Why the status-tier matrix is enforced

The most damaging failure mode is a record claiming `Operating` status with weak evidence. It asserts capacity that may not exist, and downstream maps and reports inherit that error. The validator therefore requires Tier 1 for any `Operating`, `Under Construction`, or `Closed` record, and Tier 3 for any `Rumored` record. The middle states (`Planned`, `Announced`, `Paused`, `Cancelled`) accept any tier because the claim being made is softer. If a researcher finds themselves writing an invalid pair, the response is to fix one side or the other, never to leave the contradiction. Mechanical enforcement removes the temptation to round up.

## How conflicts get resolved

Source disagreement is normal. Four rules cover the cases that actually appear.

**Investment figures conflict.** The most recent verifiable figure becomes the headline `investmentM`. Earlier figures move into `investmentM_history`, each with a date and a source URL. The skill never silently averages. Multiple announcements at different scales typically reflect phased commitments or revised plans, and preserving them lets future analysts reconstruct the trajectory rather than inheriting a single number with no context.

**Company says "Operating", independent says "delayed".** Trust the independent source and downgrade status. Companies have a structural incentive to overstate progress on quarterly calls, in investor decks, and in press releases. Independent named-author trade coverage of a delayed commissioning is a stronger signal of current state than a company line that has not been updated.

**Company says "Cancelled", independent says "Paused".** Trust the company. They know what they intend to do. Trade press sometimes reports "paused" when a cancellation has just landed and is not yet widely covered. The cost of being wrong on the optimistic side (recording a paused project that is in fact dead) is higher than the cost of recording an early cancellation.

**Government announces, company silent.** A subnational governor or a national investment agency sometimes front-runs a deal that is not yet finalized. These announcements get Tier 3 at most until the company confirms on its own domain. Re-verify in 60 days, since these often die quietly.

## Why some domains are hard-rejected

Wikipedia, Grokipedia, LinkedIn, Reddit, X, Facebook, Instagram, and Medium are blocked at write time by the validator. These are derivative summaries (Wikipedia), self-published content with no editorial filter (Medium), or anonymous-by-default social posts (Reddit, X). Putting the rejection in code, not in prose, is cheaper than relying on researcher discipline. See `sources.md` for the full list and the Tier A primaries that should be cited instead. Wikipedia remains useful for lead generation, but never as a citation.

## Re-verification has a shelf life

A record verified in 2023 can be cancelled, rebranded, or doubled in capacity by 2025. The `verifiedDate` field ages out and triggers re-checks. When evidence has strengthened, the tier upgrades. When evidence has weakened, the tier or status downgrades. The skill treats the dataset as a living artifact, not a snapshot. The Northvolt Heide record is the obvious working example: announced 2022, verified at Tier 1, downgraded to `Cancelled` after the November 2024 Chapter 11 filing and June 2025 Lyten acquisition.

## Extending these rules

These rules are starting points. Lab members are expected to push back on individual tier assignments, propose new red flags when they spot recurring patterns, and extend the source catalog in `sources.md` as new authoritative outlets emerge. The validator is the floor, not the ceiling. Document your reasoning in `appendix/common-mistakes.md` when you deviate or discover a new failure mode worth banning.
