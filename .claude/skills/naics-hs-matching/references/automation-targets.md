# Automation Targets

## High-Value Automations

1. **Review field injection**
   - Add `mapping_method`, `candidate_source`, `override_reason`, `review_status`, and `reviewer`.
   - Safe to run whenever a mapping table changes.

2. **Mapping consistency audit**
   - Classify rows and generate `issues_for_review.csv`.
   - Check candidate-set consistency, unmapped rows, split weights, and repeated HS behavior.

3. **GitHub validation**
   - Fail CI when required review columns are missing.
   - In strict mode, fail when `needs_review` rows lack an `override_reason` after review is supposed to be complete.

4. **Version change log**
   - Compare previous and current mapping files.
   - Report changed `final_naics6`, changed `review_status`, new manual overrides, and newly unmapped rows.

5. **Description enrichment**
   - Add HS descriptions and NAICS definitions from authoritative reference files.
   - Use this to support reviewer decisions, not as automatic proof.

6. **Candidate scoring**
   - Score candidate NAICS using text overlap, role/stage fit, and prior accepted decisions.
   - Treat scores as triage aids; final decisions remain human-reviewed.

7. **Override reason drafting**
   - Draft a proposed reason for manual overrides.
   - Require human acceptance before writing the final `override_reason`.

## Suggested GitHub Action Pattern

Run validation on pull requests that touch mapping files:

```bash
python .claude/skills/naics-hs-matching/scripts/audit_mapping.py path/to/naics_hs_map.csv audit/naics_hs
```

In early review phases, use non-strict validation so CI reports issues without blocking work. Switch to strict mode when the mapping is treated as production data.

## Recommended Artifact Contract

Every mapping refresh should produce:

- Clean mapping CSV with review fields.
- Audit memo.
- Row-level audit table.
- Issues-for-review table.
- Change log against prior mapping version.
- Workbook or analyst-facing export, if needed.
