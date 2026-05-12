from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import pandas as pd


REQUIRED_COLUMNS = {
    "mapping_method",
    "candidate_source",
    "override_reason",
    "review_status",
    "reviewer",
}

ALLOWED_METHODS = {
    "candidate_match",
    "manual_override",
    "manual_only",
    "unmapped_with_candidates",
    "unmapped_no_candidates",
}

ALLOWED_STATUSES = {
    "accepted",
    "needs_review",
    "revised",
    "out_of_scope",
    "unmapped_pending_evidence",
}


def clean(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value).strip())


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate NAICS-HS mapping review workflow fields.")
    parser.add_argument("mapping_csv")
    parser.add_argument("--strict", action="store_true", help="Fail if any rows still need review.")
    parser.add_argument("--output-json", help="Optional path for validation results JSON.")
    args = parser.parse_args()

    df = pd.read_csv(args.mapping_csv, dtype=str).fillna("")
    issues: list[dict[str, Any]] = []

    missing_columns = sorted(REQUIRED_COLUMNS - set(df.columns))
    for column in missing_columns:
        issues.append({"severity": "error", "type": "missing_column", "column": column})

    if missing_columns:
        result = {"ok": False, "rows": len(df), "issues": issues}
        print(json.dumps(result, indent=2))
        raise SystemExit(1)

    bad_methods = sorted(set(df["mapping_method"]) - ALLOWED_METHODS - {""})
    for method in bad_methods:
        issues.append({"severity": "error", "type": "invalid_mapping_method", "value": method})

    bad_statuses = sorted(set(df["review_status"]) - ALLOWED_STATUSES - {""})
    for status in bad_statuses:
        issues.append({"severity": "error", "type": "invalid_review_status", "value": status})

    blank_review_status = int(df["review_status"].map(clean).eq("").sum())
    if blank_review_status:
        issues.append({"severity": "error", "type": "blank_review_status", "rows": blank_review_status})

    needs_review = int(df["review_status"].eq("needs_review").sum())
    if args.strict and needs_review:
        issues.append({"severity": "error", "type": "rows_still_need_review", "rows": needs_review})

    accepted_exceptions = df[(df["review_status"].eq("accepted")) & (~df["mapping_method"].eq("candidate_match"))]
    missing_reason = int(accepted_exceptions["override_reason"].map(clean).eq("").sum())
    missing_reviewer = int(accepted_exceptions["reviewer"].map(clean).eq("").sum())
    if missing_reason:
        issues.append({"severity": "error", "type": "accepted_exception_missing_override_reason", "rows": missing_reason})
    if missing_reviewer:
        issues.append({"severity": "error", "type": "accepted_exception_missing_reviewer", "rows": missing_reviewer})

    result = {
        "ok": not any(issue["severity"] == "error" for issue in issues),
        "rows": len(df),
        "method_counts": df["mapping_method"].value_counts().to_dict(),
        "status_counts": df["review_status"].value_counts().to_dict(),
        "issues": issues,
    }

    if args.output_json:
        Path(args.output_json).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output_json).write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
