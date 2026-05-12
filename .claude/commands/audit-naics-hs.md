---
description: Audit a NAICS-HS mapping CSV, add review workflow fields, and generate issue files for manual concordance review.
---

# Audit NAICS-HS Mapping

Use the `naics-hs-matching` skill.

## Input

The user should provide:

- Mapping CSV path.
- Output directory for audit files.
- Optional final NAICS column name. Default: `final_naics6`.
- Optional candidate columns. Default: `source_naics6,source_naics6_nace,source_naics6_all,naics6,naics6_all`.

## Workflow

1. Inspect the mapping CSV headers.
2. If review workflow columns are missing, run:

```bash
python .claude/skills/naics-hs-matching/scripts/add_review_fields.py \
  INPUT.csv \
  OUTPUT_WITH_REVIEW.csv \
  --final-col final_naics6 \
  --overwrite
```

3. Audit the mapping:

```bash
python .claude/skills/naics-hs-matching/scripts/audit_mapping.py \
  OUTPUT_WITH_REVIEW.csv \
  AUDIT_OUTPUT_DIR \
  --final-col final_naics6
```

4. Summarize the audit metrics and point the user to:

- `naics_hs_mapping_consistency_audit.md`
- `issues_for_review.csv`
- `manual_overrides.csv`
- `unmapped_rows.csv`
- `hs_multi_naics_review.csv`

## Rules

- Do not invent `override_reason`.
- Do not infer reviewer names.
- Treat broad HS codes mapping to multiple NAICS as a review item, not an automatic error.
- Recommend a correction only when the evidence is visible in the candidate fields or reference material.
