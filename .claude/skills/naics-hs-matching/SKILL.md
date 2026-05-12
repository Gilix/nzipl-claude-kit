---
name: naics-hs-matching
description: "Audit, clean, validate, and maintain NAICS-HS concordance mappings for economic complexity and clean technology work. Use when the user asks about HS-to-NAICS or NAICS-to-HS matching, manual concordance review, Green Dictionary mappings, S&P firm NAICS matching, candidate NAICS selection, mapping_method/candidate_source/override_reason workflow columns, split weights, same-HS multiple-NAICS issues, or GitHub-ready validation of mapping files."
---

# NAICS-HS Matching

Use this skill to turn manual HS-to-NAICS mappings into auditable concordances. The core principle is simple: many HS codes can map to one NAICS, and broad HS machinery codes can map differently by clean-tech context. The risk is not one-to-many mapping; the risk is undocumented exception logic.

## Standard Workflow

1. Identify the mapping table and preserve source columns.
2. Normalize HS and NAICS codes as text, not numbers.
3. Extract candidate NAICS codes from available concordance fields.
4. Classify each row with `mapping_method`.
5. Add or update review workflow columns.
6. Audit consistency across repeated HS codes, candidate sets, split weights, role/stage, and unmapped rows.
7. Produce a row-level audit CSV plus a short memo.
8. Recommend edits, but do not invent `override_reason` values without user approval.

## Required Review Fields

Every mapping table should include:

| Field | Purpose |
|---|---|
| `mapping_method` | Audit classification: `candidate_match`, `manual_override`, `manual_only`, `unmapped_with_candidates`, or `unmapped_no_candidates`. |
| `candidate_source` | Source of evidence for the selected final NAICS, such as `source_naics6`, `source_naics6_nace`, or `source_naics6_all`. |
| `override_reason` | Human-entered rationale for manual overrides or nonstandard mappings. Leave blank until reviewed. |
| `review_status` | Workflow status. Use `accepted`, `needs_review`, `revised`, `out_of_scope`, or `unmapped_pending_evidence`. |
| `reviewer` | Person responsible for the decision. |

## Mapping Method Rules

Use candidate columns as the default evidence base. Common source columns are:

- `source_naics6`
- `source_naics6_nace`
- `source_naics6_all`
- `naics6`
- `naics6_all`

Classify rows as:

- `candidate_match`: `final_naics6` appears in the candidate set.
- `manual_override`: `final_naics6` does not appear in the candidate set, but candidates exist.
- `manual_only`: `final_naics6` exists, but no candidate evidence exists.
- `unmapped_with_candidates`: no `final_naics6`, but candidate evidence exists.
- `unmapped_no_candidates`: no `final_naics6` and no candidate evidence.

Default `review_status`:

- `accepted` for `candidate_match`.
- `needs_review` for all other methods.

## Audit Checks

Always check:

- `same technology + HS code` mapping to multiple final NAICS.
- `same HS + component name` mapping to multiple final NAICS.
- Same HS code mapping to multiple final NAICS across contexts.
- Split weights sum to 1 within each `technology + hs_code` group when repeated rows represent a split.
- Rows without `final_naics6`.
- Mapped rows without candidate evidence.
- Manual overrides outside the candidate set.
- Final NAICS definitions missing from the reference table.
- Process equipment rows mapped outside likely equipment-producing NAICS groups, especially 333/334/335/336/339.

## Interpreting Results

Do not over-penalize broad HS codes. HS codes such as `847989`, `841989`, `841990`, and other machinery parts can legitimately map to different NAICS depending on the component and clean technology context. Flag them for documentation, not automatic correction.

Manual overrides are acceptable when the component description materially narrows a broad HS code to a better NAICS industry. The workbook must record the rationale.

## Pipeline Order

A full mapping refresh runs in this order. Each step is independent; rerun any one without rerunning earlier steps.

1. `profile_workbook.py` — list sheets, headers, row counts, and type profiles of the source `.xlsx`. Use to learn the shape before writing the source-specific cleaning step.
2. **Source-specific cleaning step** — read the source workbook, normalize HS and NAICS as text, extract candidate NAICS columns, write `csv/naics_hs_map.csv` and any companion tables. Not bundled because the sheet names, column names, and join keys are dataset-specific. See `outputs/sp_company_naics_hs_cleaning/scripts/clean_source.py` in GripPoint for one worked example against the S&P firm workbook.
3. `add_review_fields.py` — add the five review workflow columns to `csv/naics_hs_map.csv`.
4. `audit_mapping.py` — classify every row, flag exceptions, write the audit memo and row-level review CSVs.
5. `build_streaming_workbook.py` — rebuild the analyst-facing `.xlsx` from the cleaned CSVs using a streaming writer (handles 300k+ rows without exhausting memory). Adds autofilters and frozen headers, writes a verification JSON.
6. `inspect_output.py` — quick sanity check: sheet names plus sample rows.
7. `validate_mapping_review.py` — CI-friendly check that all review columns are present with allowed values. Use non-strict mode while review is in progress; switch to `--strict` once the mapping is treated as production data.
8. `compare_mapping_versions.py` — diff a new mapping CSV against the prior version by `mapping_id`. Produces added rows, removed rows, field-level change tables, and a Markdown changelog for the PR description.

## Bundled Resources

- `scripts/profile_workbook.py`: profile a source `.xlsx` — sheets, headers, row counts, duplicate headers, sample values, type profiles. Read-only.
- `scripts/add_review_fields.py`: add `mapping_method`, `candidate_source`, `override_reason`, `review_status`, and `reviewer` to a mapping CSV.
- `scripts/audit_mapping.py`: audit mapping consistency and write review CSVs plus a Markdown memo. Argparse-driven; supports `--final-col`, `--candidate-cols`, `--strict-review`.
- `scripts/build_streaming_workbook.py`: rebuild the analyst-facing `.xlsx` from cleaned CSVs using openpyxl's streaming writer. Writes a verification JSON alongside the workbook.
- `scripts/inspect_output.py`: print sheet names and sample rows of a rebuilt workbook for a quick sanity check.
- `scripts/validate_mapping_review.py`: CI check for required review columns and allowed `mapping_method` / `review_status` values. `--strict` fails if any row remains `needs_review` or if accepted non-candidate matches lack `override_reason` / `reviewer`. `--output-json` writes a machine-readable result.
- `scripts/compare_mapping_versions.py`: diff two mapping CSVs by `mapping_id` — added rows, removed rows, field-level changes, and a Markdown changelog. Useful as a PR-description input.
- `references/matching-criteria.md`: criteria and examples for classification.
- `references/automation-targets.md`: automation ideas and implementation patterns for future pipelines and CI.

All scripts are stdlib + `pandas` (+ `openpyxl` for the workbook steps). No other dependencies.

## Output Standard

For audit tasks, produce:

- `mapping_row_audit.csv`
- `issues_for_review.csv`
- `manual_overrides.csv`
- `unmapped_rows.csv`
- `hs_multi_naics_review.csv`
- `audit_metrics.json`
- `naics_hs_mapping_consistency_audit.md`

For cleaned workbook tasks, include `NAICS_HS_Map` with the required review fields and preserve the original candidate/source columns.
