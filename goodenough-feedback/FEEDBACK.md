# goodenough · feedback rubric for lab testers

## What this is

A structured-but-fast form for lab researchers to write feedback after running a query through goodenough. The point is to capture judgment the automated test gates can't:

- `tests/run_evals.py` checks that Claude calls the right tool and the result has the right keys.
- `tests/stress_gaps.py` hand-checks 8 SHAP scenarios for classification correctness.
- This rubric is what *you* notice when you sit with the tool: did the answer feel honest, did it stay at category level (WP-4 p.10), did the live tool indicators help, did the share link work.

Fill out one rubric per query, ~5 minutes. Submit by committing the file. The author of goodenough triages each session and routes findings back to the right file (`bot.py`, `system-prompt.md`, `chat.html`, `tools.json`, the data CSVs, the OEC cache).

The most demanding scenario is `analyze_capability_gaps` (the SHAP method on a country × tech). It exercises every dimension of this rubric. A worked example is at the bottom.

## How to test

1. Pick a question. Use one from [demo-queries.md](demo-queries.md) or invent one; questions that require multiple tools are most useful.
2. Run it at https://atlas-nzipl.fly.dev (basic auth: `team` / Fly secret `ATLAS_PASSWORD`).
3. Click **Share** to get a durable `#share=` link. Do this *after* the answer renders, not before.
4. Copy the per-session template below into a new file: `goodenough-feedback/sessions/YYYY-MM-DD-yourtag.md` (in the public `nzipl-claude-kit` repo).
5. Fill the seven dimensions. Each is rated Fail / Partial / Pass with one or two lines of note. Don't over-write; the goal is to surface what's wrong, not to defend the rating.
6. Open a PR. Merge yourself; no review needed. The PR body can be one line. **First time?** [HOW_TO_SUBMIT.md](HOW_TO_SUBMIT.md) walks through three paths (GitHub web UI, Claude Code, terminal git) with no prior assumptions.

## The seven dimensions

Each dimension maps to a specific surface the goodenough author can fix. Stay concrete. "It felt off" is not actionable; "Mexico's PC score for batteries was reported as 0.42 but my CVCE notebook shows 0.31 for 2024" is.

### A. Tool routing

Did Claude pick the right tool? Did the routing heuristic (Sonnet vs Haiku, single tool vs composed) seem sensible?

- **Pass:** Called the expected tool(s); composed multiple tools when the question warranted it; no fall-through to text-only when data was available.
- **Partial:** Called something workable but missed a useful tool. Example: used `query_pc_features` when `analyze_capability_gaps` was the right call. Or used Haiku on a multi-turn reasoning question that needed Sonnet.
- **Fail:** Refused, hallucinated tool data, or used a clearly wrong tool. Example: used `explain_methodology` to answer a numeric ranking question.

Routes to: `tools.json` descriptions, `system-prompt.md` "How to Answer" section, `_route_model` in `bot.py`.

### B. Answer correctness (data)

Do the numbers match what CVCE or OEC would return? Are classifications consistent with the methodology?

- **Pass:** Numbers match a CVCE notebook or OEC API spot-check; classifications follow the WP-4 thresholds (RCA strength ≥ 1.0, partial ≥ 0.5; SHAP critical_driver ≥ 25%, important_driver ≥ 10%).
- **Partial:** Roughly right but a figure looks off by a small amount, or a classification is borderline and the tool picked the less defensible side.
- **Fail:** Wrong country, wrong year, hallucinated value, classification flatly contradicts the data. Example: tool says Mexico chemicals is `build_up` when the RCA is 0.31 (should be `critical_gap`).

Routes to: data CSVs in `data/`, OEC cache, the relevant tool implementation in `bot.py`.

### C. Methodology discipline (the WP-4 SHAP rule)

The load-bearing dimension for SHAP and capability-gap queries. WP-4 p.10 says: never recommend at the HS6 level. The model speaks at the capability-cluster level. HS6 codes are the evidentiary trail, not policy targets.

- **Pass:** Stayed at the 5-cluster level (Electronics, Machinery, Mining & Metals, Industrial Materials, Chemicals). HS6 codes only appeared as "the features the model weighted most heavily" or framed as discovery prompts. Quoted F1 once. Used `bonus_strength` correctly when a cluster has RCA ≥ 1.0 but is a supporting driver.
- **Partial:** Mostly category-level but slipped one HS6 prescription, or cited F1 without explaining what it implies, or labelled a real `bonus_strength` as a `mature_strength`.
- **Fail:** Prescribed at HS6 ("Mexico should produce germanium oxides to win electrolyzers"). Or didn't cite F1 at all on a low-F1 tech (Electrolyzers 0.65, Batteries 0.67). Or treated `bonus_strength` as a tech-specific anchor.

Routes to: `system-prompt.md` (lines 57-67 SHAP discipline; lines 85-103 narrative shape), `SHAP_INTERPRETATION_GUARDRAIL` in `bot.py`.

### D. Narrative shape

The `analyze_capability_gaps` and `query_pc_features` outputs are a hard contract: 3 sections (Lead → Table → Read) + 1 italic caveat. Target ~250 words, never more than 400. One consolidated table, 5 rows ordered by SHAP share descending, only critical drivers in bold.

- **Pass:** All three named sections present, no extras. Single table, 5 rows ordered correctly, bold on critical drivers only. Italic caveat at the bottom with F1 and year. Word count under 400.
- **Partial:** Extra subsection ("Recommendations" or "Key Takeaways"). F1 cited twice (once in prose, once in caveat). Table missing bold or rows out of order.
- **Fail:** Prose dump with no table. No caveat. Subsection headers beyond Lead / Table / Read. Word count over 400.

Routes to: `system-prompt.md` (the contract is there verbatim).

### E. Uncertainty handling

Several tool results carry explicit uncertainty metadata (`as_of`, `model_f1`, `uncertainty_note`, `model_note`). Did Claude actually surface them when they matter?

- **Pass:** Surfaced low F1 on noisy techs (Electrolyzers, Batteries). Flagged thin baskets when citing municipality-level RCA. Called out null fields explicitly (ORBIS not loaded; `value_chain_position` not computable). Quoted `as_of` year next to numeric scores.
- **Partial:** Cited F1 but didn't explain implications. Missed an obvious caveat. Cited a high-RCA municipality without flagging that its basket has 1 product.
- **Fail:** Confident about clearly noisy data. Presented null fields as if they were real numbers. No `as_of`. Quoted Vietnam's PC for Nuclear (F1 0.65) as a clean point estimate.

Routes to: `bot.py` (`uncertainty_note`, `model_f1`, `model_note` surfacing logic), `system-prompt.md` "Surfacing uncertainty honestly" section.

### F. UX & transparency

The streaming UI is supposed to keep you oriented while Claude runs tools, and the share + replay flow is supposed to produce a durable artifact you can send to a collaborator.

- **Pass:** Live tool indicators showed (`Atlas is calling X…`) and resolved to `✓ X(...) · Nms` with timing. Charts rendered. Download PNG and CSV worked. Share button enabled after the first server turn and copied a `#share=` URL that loads the conversation cleanly in a fresh browser. Entity auto-linking made sense (clicked countries/techs seeded follow-ups, no false positives).
- **Partial:** Minor friction. SSE stream stalled briefly. Share button stayed disabled longer than expected. Chart rendered but axis labels overlapped. Entity-linking wrapped a country name inside an unrelated word.
- **Fail:** Chart broken or empty. Share link 404'd or replayed onto the homepage. Live indicator stuck on "calling X…" with no resolution. Tool result rendered as raw JSON.

Routes to: `chat.html`, `server.py` SSE, `snapshot_store.py` for share-link issues.

### G. Open feedback

Free text, four prompts. Be specific. One concrete observation beats a paragraph of impressions.

- What surprised you?
- What did you want it to do that it couldn't?
- Did anything feel like a hallucination? Quote the sentence.
- What would have made the answer more useful for your work?

Routes to: anything. New fixtures for `tests/fixtures/core_queries.json`, new scenarios for `stress_gaps.py`, system-prompt tweaks, new tools, data refreshes.

## Per-session template

Copy this block into `goodenough-feedback/sessions/YYYY-MM-DD-yourtag.md` (in `nzipl-claude-kit`) and fill it in.

```markdown
# YYYY-MM-DD · <yourtag> · <one-line query summary>

- **Tester:**
- **Query:**
- **Tech / country:**
- **Model observed:** sonnet | haiku | cache_hit (check the streamed tool indicators or `/admin/stats`)
- **Session URL:** <paste the #share= or #s= URL>

## Ratings

| Dim | Rating | Note |
|-----|--------|------|
| A. Tool routing | Pass / Partial / Fail | |
| B. Answer correctness | Pass / Partial / Fail | |
| C. Methodology discipline | Pass / Partial / Fail | |
| D. Narrative shape | Pass / Partial / Fail | |
| E. Uncertainty handling | Pass / Partial / Fail | |
| F. UX & transparency | Pass / Partial / Fail | |

## Open feedback

**Surprise:**

**Wanted but didn't get:**

**Hallucination flag (with quote):**

**Would be more useful if:**
```

## Worked example: applying SHAP to Mexico × Batteries

Query: *"Apply the SHAP method to Mexico for batteries."*

This is the canonical capability-gap test. Expected output shape from `system-prompt.md`: Lead → Table → Read → italic caveat. Target ~250 words. Two filled rubrics below show what Pass and Flawed look like in practice.

### Reference: what a Pass response should look like

> Batteries are driven by chemicals (49% SHAP) and machinery (33%). Mexico falls short on both: RCA 0.31 and 0.47 respectively, both classified as critical gaps.
>
> | Cluster | SHAP share | Country RCA | Classification |
> |---|---|---|---|
> | **Chemicals** | 49% | 0.31 | critical_gap |
> | **Machinery** | 33% | 0.47 | critical_gap |
> | Electronics | 8% | 0.62 | not_priority |
> | Metals | 6% | 1.05 | bonus_strength |
> | Industrial Materials | 4% | 0.41 | not_priority |
>
> Mexico's strategic position on batteries is weak: the two clusters the model weights most heavily, chemicals and machinery, are exactly where Mexico lacks RCA. Closing chemicals is the hardest problem and requires upstream investment. Machinery is closer and may benefit from supplier-development programs anchored on existing automotive depth. Mexico's metals RCA shows up as bonus_strength: real capability, but not decisive for batteries; more useful for transmission or solar. Strength categories in the tool result carry firm_view_hook entries usable as discovery prompts in firm databases.
>
> *Source: NZIPL PC model (WP-4) × BACI 2024. Model F1 = 0.67; directional rankings, the bottom half is noisier than the top.*

Three sections plus a caveat. ~150 words. Critical drivers bold, supporting rows un-bold. F1 cited once. `bonus_strength` used correctly. No HS6 prescriptions. firm_view_hook acknowledged in one sentence.

### Session A · Pass across the board

| Dim | Rating | Note |
|-----|--------|------|
| A. Tool routing | Pass | Called `analyze_capability_gaps` directly. No detour through `query_pc_features` first. |
| B. Answer correctness | Pass | RCA 0.31 for chemicals matches the WP-4 Figure 4 example; Metals at 1.05 spot-checked against my BACI extract. |
| C. Methodology discipline | Pass | Category-level only. HS6 codes never appeared in prose; the firm_view_hook reference points to them without enumerating. |
| D. Narrative shape | Pass | Three sections, single table, italic caveat. ~150 words. |
| E. Uncertainty handling | Pass | F1 0.67 cited once in caveat; "directional rankings" qualifier present. |
| F. UX & transparency | Pass | Tool indicator resolved to `✓ analyze_capability_gaps(...) · 2.1s`. Share link replayed cleanly in a private window. |

**Surprise:** It used `bonus_strength` and explained the cross-tech read on metals without being prompted.

**Wanted but didn't get:** A pointer to the analogous Hungary diagnostic, since WP-4 Figure 4 contrasts the two.

**Hallucination flag:** None.

**Would be more useful if:** The metals `bonus_strength` line linked back to a follow-up suggestion ("ask about Mexico × Solar to see this cluster as a mature_strength").

### Session B · Slipped on methodology and uncertainty

| Dim | Rating | Note |
|-----|--------|------|
| A. Tool routing | Pass | Called `analyze_capability_gaps`. |
| B. Answer correctness | Pass | Numbers match. |
| C. Methodology discipline | Fail | Prose said "Mexico should produce cathode active materials (HS 280530) and lithium hexafluorophosphate (HS 282612) to close the chemicals gap." Direct WP-4 p.10 violation. |
| D. Narrative shape | Partial | Added a "Recommendations" subsection with three bullets after the Read. Cited F1 once in prose and again in the caveat. ~310 words. |
| E. Uncertainty handling | Fail | F1 0.67 cited as a value but no qualifier. "Mexico's PC for batteries is 0.42" with no `as_of`. No mention that the bottom half of the ranking is noisier. |
| F. UX & transparency | Pass | UI worked. |

**Surprise:** The HS6 prescriptions read like consultant boilerplate and felt confident enough to mislead a non-WP-4-fluent reader.

**Wanted but didn't get:** A clear "this is not the level of precision the model supports" guardrail in the prose, mirroring `SHAP_INTERPRETATION_GUARDRAIL`.

**Hallucination flag:** "lithium hexafluorophosphate (HS 282612)". The HS6 is a real code, but the prescriptive framing is the WP-4-forbidden move.

**Would be more useful if:** The system prompt is updated to make the never-at-HS6 rule a refusal trigger, not just a guideline. Or the tool result's `interpretation_guardrail` field is auto-prepended in prose when the answer mentions any HS6 code.

The Session B feedback is the most useful kind: each Failure is concrete, quoted, and routes to a specific file. The goodenough author can read this and know which lines of `system-prompt.md` to tighten and whether to add a new fixture to `tests/stress_gaps.py`.

## Where feedback routes back to

| Dimension finding | Likely fix surface |
|---|---|
| Tool routing wrong | `tools.json` descriptions; `system-prompt.md` examples; `_route_model` heuristic in `bot.py` |
| Number wrong | Data CSVs, OEC cache, tool implementation in `bot.py` |
| Methodology slip (HS6 prescription, missing F1, bonus_strength misread) | `system-prompt.md` lines 57-67 and 85-103; `SHAP_INTERPRETATION_GUARDRAIL` |
| Narrative shape broken | `system-prompt.md` lines 85-103 (the contract is the prompt) |
| Uncertainty not surfaced | `bot.py` uncertainty plumbing; system-prompt "Surfacing uncertainty honestly" section |
| UX broken | `chat.html`, `server.py` SSE, `snapshot_store.py` |
| Hallucination | New fixture in `tests/fixtures/core_queries.json` (structural) or `tests/stress_gaps.py` (qualitative) |
