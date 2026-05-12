from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import pandas as pd


ROLE_EXPECTED_PREFIXES = {
    "Process Equipment": {"333", "334", "335", "336", "339"},
    "Raw Material": {"111", "112", "113", "114", "115", "211", "212", "213", "311", "321", "322", "324", "325", "326", "327", "331"},
    "Processed Material": {"311", "321", "322", "324", "325", "326", "327", "331", "332", "339"},
    "Product Component": {"325", "326", "327", "331", "332", "333", "334", "335", "336", "339"},
    "Final Product": {"333", "334", "335", "336"},
}

DEFAULT_CANDIDATE_COLUMNS = ["source_naics6", "source_naics6_nace", "source_naics6_all", "naics6", "naics6_all"]


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


def sorted_join(values: pd.Series) -> str:
    return "; ".join(sorted({clean(value) for value in values if clean(value)}))


def candidate_sources(row: pd.Series, columns: list[str]) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for column in columns:
        if column not in row.index:
            continue
        for code in re.findall(r"\d{6}", clean(row[column])):
            out.setdefault(code, []).append(column)
    return out


def classify(row: pd.Series, final_col: str, candidate_cols: list[str]) -> tuple[str, str, list[str]]:
    final = norm_code(row.get(final_col, ""))
    sources = candidate_sources(row, candidate_cols)
    candidates = sorted(sources)
    if final and final in sources:
        return "candidate_match", ";".join(sorted(set(sources[final]))), candidates
    if final and sources:
        return "manual_override", "outside_candidate_set", candidates
    if final:
        return "manual_only", "no_candidate_source", candidates
    if sources:
        return "unmapped_with_candidates", "candidate_set_available_no_final", candidates
    return "unmapped_no_candidates", "no_candidate_source", candidates


def role_stage_mismatch(row: pd.Series, final_col: str) -> bool:
    final = norm_code(row.get(final_col, ""))
    role = clean(row.get("role", ""))
    if not final or role not in ROLE_EXPECTED_PREFIXES:
        return False
    return final[:3] not in ROLE_EXPECTED_PREFIXES[role]


def severity(flags: list[str]) -> str:
    if "unmapped_with_candidates" in flags or "same_technology_hs_has_multiple_final_naics" in flags or "same_hs_component_has_multiple_final_naics" in flags:
        return "high"
    medium = {
        "manual_override",
        "manual_only",
        "unmapped_no_candidates",
        "role_stage_prefix_mismatch",
        "cross_context_hs_has_multiple_final_naics",
        "missing_override_reason",
        "missing_reviewer",
    }
    if any(flag in medium for flag in flags):
        return "medium"
    return "low" if flags else "none"


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit NAICS-HS mapping consistency.")
    parser.add_argument("mapping_csv")
    parser.add_argument("output_dir")
    parser.add_argument("--final-col", default="final_naics6")
    parser.add_argument("--candidate-cols", default=",".join(DEFAULT_CANDIDATE_COLUMNS))
    parser.add_argument("--strict-review", action="store_true", help="Flag missing override_reason/reviewer on non-candidate matches.")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    candidate_cols = [col.strip() for col in args.candidate_cols.split(",") if col.strip()]

    df = pd.read_csv(args.mapping_csv, dtype=str).fillna("")
    if args.final_col not in df.columns:
        raise SystemExit(f"Missing final NAICS column: {args.final_col}")

    classified = df.apply(lambda row: classify(row, args.final_col, candidate_cols), axis=1)
    df["mapping_method"] = [item[0] for item in classified]
    df["candidate_source"] = [item[1] for item in classified]
    df["candidate_naics6"] = [";".join(item[2]) for item in classified]
    if "review_status" not in df.columns:
        df["review_status"] = ""
    df["review_status"] = df["review_status"].where(
        df["review_status"] != "",
        df["mapping_method"].map(lambda x: "accepted" if x == "candidate_match" else "needs_review"),
    )

    mapped = df[df[args.final_col].map(norm_code) != ""].copy()
    tech_hs_counts = mapped.groupby(["technology", "hs_code"])[args.final_col].nunique() if {"technology", "hs_code"}.issubset(df.columns) else pd.Series(dtype=int)
    hs_component_counts = mapped.groupby(["hs_code", "component_name"])[args.final_col].nunique() if {"hs_code", "component_name"}.issubset(df.columns) else pd.Series(dtype=int)
    hs_counts = mapped.groupby("hs_code")[args.final_col].nunique() if "hs_code" in df.columns else pd.Series(dtype=int)

    flags_by_row = []
    for _, row in df.iterrows():
        flags = []
        if row["mapping_method"] != "candidate_match":
            flags.append(row["mapping_method"])
        if not tech_hs_counts.empty and tech_hs_counts.get((row.get("technology", ""), row.get("hs_code", "")), 0) > 1:
            flags.append("same_technology_hs_has_multiple_final_naics")
        if not hs_component_counts.empty and hs_component_counts.get((row.get("hs_code", ""), row.get("component_name", "")), 0) > 1:
            flags.append("same_hs_component_has_multiple_final_naics")
        if not hs_counts.empty and hs_counts.get(row.get("hs_code", ""), 0) > 1:
            flags.append("cross_context_hs_has_multiple_final_naics")
        if role_stage_mismatch(row, args.final_col):
            flags.append("role_stage_prefix_mismatch")
        if args.strict_review and row["mapping_method"] != "candidate_match":
            if not clean(row.get("override_reason", "")):
                flags.append("missing_override_reason")
            if not clean(row.get("reviewer", "")):
                flags.append("missing_reviewer")
        flags_by_row.append(sorted(set(flags)))

    df["audit_flags"] = [";".join(flags) for flags in flags_by_row]
    df["audit_severity"] = [severity(flags) for flags in flags_by_row]

    review_cols = [
        "audit_severity",
        "audit_flags",
        "mapping_method",
        "candidate_source",
        "candidate_naics6",
        "review_status",
        "override_reason",
        "reviewer",
    ]
    front = [col for col in review_cols if col in df.columns]
    rest = [col for col in df.columns if col not in front]
    row_audit = df[front + rest]
    row_audit.to_csv(output_dir / "mapping_row_audit.csv", index=False)
    row_audit[row_audit["audit_severity"].isin(["high", "medium"])].to_csv(output_dir / "issues_for_review.csv", index=False)
    row_audit[row_audit["mapping_method"].eq("manual_override")].to_csv(output_dir / "manual_overrides.csv", index=False)
    row_audit[row_audit["mapping_method"].str.startswith("unmapped")].to_csv(output_dir / "unmapped_rows.csv", index=False)

    if "hs_code" in df.columns:
        agg_spec = {
            "rows": (args.final_col, "count"),
            "final_naics_count": (args.final_col, "nunique"),
            "final_naics6": (args.final_col, sorted_join),
        }
        if "technology" in mapped.columns:
            agg_spec["technologies"] = ("technology", sorted_join)
        if "component_name" in mapped.columns:
            agg_spec["components"] = ("component_name", sorted_join)
        hs_multi = mapped.groupby("hs_code").agg(**agg_spec).reset_index().query("final_naics_count > 1")
    else:
        hs_multi = pd.DataFrame()
    hs_multi.to_csv(output_dir / "hs_multi_naics_review.csv", index=False)

    flag_counts = (
        row_audit.assign(flag=row_audit["audit_flags"].str.split(";"))
        .explode("flag")
        .query("flag != ''")
        .groupby("flag")
        .size()
        .sort_values(ascending=False)
        .rename("rows")
        .reset_index()
    )
    flag_counts.to_csv(output_dir / "flag_counts.csv", index=False)
    df["mapping_method"].value_counts().rename_axis("mapping_method").reset_index(name="rows").to_csv(output_dir / "criterion_counts.csv", index=False)
    df["audit_severity"].value_counts().rename_axis("severity").reset_index(name="rows").to_csv(output_dir / "severity_counts.csv", index=False)

    metrics = {
        "mapping_rows": int(len(df)),
        "mapped_rows": int((df[args.final_col].map(norm_code) != "").sum()),
        "unmapped_rows": int((df[args.final_col].map(norm_code) == "").sum()),
        "candidate_matches": int(df["mapping_method"].eq("candidate_match").sum()),
        "manual_overrides": int(df["mapping_method"].eq("manual_override").sum()),
        "manual_only": int(df["mapping_method"].eq("manual_only").sum()),
        "unmapped_with_candidates": int(df["mapping_method"].eq("unmapped_with_candidates").sum()),
        "hs_codes_with_multiple_final_naics": int(len(hs_multi)),
        "high_severity_rows": int(df["audit_severity"].eq("high").sum()),
        "medium_severity_rows": int(df["audit_severity"].eq("medium").sum()),
    }
    (output_dir / "audit_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    (output_dir / "naics_hs_mapping_consistency_audit.md").write_text(
        "# NAICS-HS Mapping Consistency Audit\n\n"
        f"- Mapping rows: {metrics['mapping_rows']:,}\n"
        f"- Candidate matches: {metrics['candidate_matches']:,}\n"
        f"- Manual overrides: {metrics['manual_overrides']:,}\n"
        f"- Manual-only rows: {metrics['manual_only']:,}\n"
        f"- Unmapped rows with candidates: {metrics['unmapped_with_candidates']:,}\n"
        f"- HS codes with multiple final NAICS across contexts: {metrics['hs_codes_with_multiple_final_naics']:,}\n\n"
        "Review `issues_for_review.csv` first, then document accepted manual overrides in `override_reason`.\n",
        encoding="utf-8",
    )
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
