from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

import pandas as pd


DEFAULT_CANDIDATE_COLUMNS = [
    "source_naics6",
    "source_naics6_nace",
    "source_naics6_all",
    "naics6",
    "naics6_all",
]


def clean(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value).strip())


def norm_code(value: Any) -> str:
    text = clean(value)
    if re.fullmatch(r"\d+\.0", text):
        text = text[:-2]
    match = re.search(r"\d{6}", text)
    return match.group(0) if match else ""


def candidate_sources(row: pd.Series, columns: list[str]) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for column in columns:
        if column not in row.index:
            continue
        for code in re.findall(r"\d{6}", clean(row[column])):
            out.setdefault(code, []).append(column)
    return out


def classify(row: pd.Series, final_col: str, candidate_cols: list[str]) -> tuple[str, str, str]:
    final = norm_code(row.get(final_col, ""))
    sources = candidate_sources(row, candidate_cols)
    if final and final in sources:
        method = "candidate_match"
        source = ";".join(sorted(set(sources[final])))
    elif final and sources:
        method = "manual_override"
        source = "outside_candidate_set"
    elif final:
        method = "manual_only"
        source = "no_candidate_source"
    elif sources:
        method = "unmapped_with_candidates"
        source = "candidate_set_available_no_final"
    else:
        method = "unmapped_no_candidates"
        source = "no_candidate_source"
    status = "accepted" if method == "candidate_match" else "needs_review"
    return method, source, status


def main() -> None:
    parser = argparse.ArgumentParser(description="Add NAICS-HS mapping review workflow fields to a CSV.")
    parser.add_argument("input_csv")
    parser.add_argument("output_csv")
    parser.add_argument("--final-col", default="final_naics6")
    parser.add_argument("--candidate-cols", default=",".join(DEFAULT_CANDIDATE_COLUMNS))
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing workflow field values.")
    args = parser.parse_args()

    candidate_cols = [col.strip() for col in args.candidate_cols.split(",") if col.strip()]
    df = pd.read_csv(args.input_csv, dtype=str).fillna("")
    if args.final_col not in df.columns:
        raise SystemExit(f"Missing final NAICS column: {args.final_col}")

    values = df.apply(lambda row: classify(row, args.final_col, candidate_cols), axis=1)
    methods = [item[0] for item in values]
    sources = [item[1] for item in values]
    statuses = [item[2] for item in values]

    assignments = {
        "mapping_method": methods,
        "candidate_source": sources,
        "override_reason": [""] * len(df),
        "review_status": statuses,
        "reviewer": [""] * len(df),
    }
    for column, column_values in assignments.items():
        if args.overwrite or column not in df.columns:
            df[column] = column_values

    Path(args.output_csv).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output_csv, index=False)
    print(df["mapping_method"].value_counts().to_string())


if __name__ == "__main__":
    main()
