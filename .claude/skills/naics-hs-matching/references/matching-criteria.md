# Matching Criteria

## Evidence Hierarchy

1. Use an official or source-provided candidate set when available.
2. Treat `final_naics6` inside the candidate set as the default valid outcome.
3. Allow manual overrides only when the clean-tech component description narrows a broad HS code to a better industry.
4. Leave `override_reason` blank only while the row is still under review.
5. Do not infer reviewer names.

## Candidate Sources

Common candidate fields:

- `source_naics6`
- `source_naics6_nace`
- `source_naics6_all`
- `naics6`
- `naics6_all`

When multiple fields support the same final NAICS, join sources with semicolons.

## Method Definitions

| mapping_method | Definition | Default review_status |
|---|---|---|
| `candidate_match` | Final NAICS appears in candidate set. | `accepted` |
| `manual_override` | Final NAICS exists but is outside candidate set. | `needs_review` |
| `manual_only` | Final NAICS exists but no candidate set exists. | `needs_review` |
| `unmapped_with_candidates` | Candidate evidence exists but no final NAICS selected. | `needs_review` |
| `unmapped_no_candidates` | No final NAICS and no candidate evidence. | `needs_review` |

## Review Logic

- If a row is `candidate_match`, check only for repeated-HS conflicts or missing definitions.
- If a row is `manual_override`, require a written `override_reason`.
- If a row is `manual_only`, require external evidence or a source note.
- If a row is `unmapped_with_candidates`, choose a candidate or mark `out_of_scope`.
- If a row is `unmapped_no_candidates`, research or mark `unmapped_pending_evidence`.

## Broad HS Codes

Broad machinery HS codes can validly map to multiple NAICS across contexts. Do not force one global NAICS if component descriptions point to different industries.

Examples that usually need context-specific review:

- `847989`: machines and mechanical appliances with individual functions.
- `841989`: machinery for treatment by temperature change.
- `841990`: parts of heat-exchange or temperature-treatment machinery.
- `842139`: filtering or purifying machinery.

## Role/Stage Sanity Checks

Use these as flags, not automatic corrections:

- Process Equipment: usually NAICS `333`, `334`, `335`, `336`, or `339`.
- Raw Material: usually `111`, `21x`, `311`, `321`, `322`, `324`, `325`, `326`, `327`, or `331`.
- Processed Material: usually `311`, `321`, `322`, `324`, `325`, `326`, `327`, `331`, `332`, or `339`.
- Product Component: usually `325`, `326`, `327`, `331`, `332`, `333`, `334`, `335`, `336`, or `339`.
- Final Product: usually `333`, `334`, `335`, or `336`.
