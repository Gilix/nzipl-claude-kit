from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


DEFAULT_COMPARE_COLUMNS = [
    "technology",
    "hs_code",
    "component_name",
    "role",
    "stage",
    "final_naics6",
    "mapping_method",
    "candidate_source",
    "override_reason",
    "review_status",
    "reviewer",
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare two NAICS-HS mapping CSV versions.")
    parser.add_argument("old_csv")
    parser.add_argument("new_csv")
    parser.add_argument("output_dir")
    parser.add_argument("--key", default="mapping_id", help="Stable row key. Default: mapping_id.")
    parser.add_argument("--columns", default=",".join(DEFAULT_COMPARE_COLUMNS), help="Comma-separated columns to compare.")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    old = pd.read_csv(args.old_csv, dtype=str).fillna("")
    new = pd.read_csv(args.new_csv, dtype=str).fillna("")
    if args.key not in old.columns or args.key not in new.columns:
        raise SystemExit(f"Key column must exist in both files: {args.key}")

    old = old.drop_duplicates(args.key).set_index(args.key)
    new = new.drop_duplicates(args.key).set_index(args.key)

    old_keys = set(old.index)
    new_keys = set(new.index)
    added_keys = sorted(new_keys - old_keys)
    removed_keys = sorted(old_keys - new_keys)
    common_keys = sorted(old_keys & new_keys)
    columns = [col.strip() for col in args.columns.split(",") if col.strip()]
    columns = [col for col in columns if col in old.columns or col in new.columns]

    changes = []
    for key in common_keys:
        for column in columns:
            old_value = old.at[key, column] if column in old.columns else ""
            new_value = new.at[key, column] if column in new.columns else ""
            if old_value != new_value:
                changes.append(
                    {
                        args.key: key,
                        "column": column,
                        "old_value": old_value,
                        "new_value": new_value,
                    }
                )

    added = new.loc[added_keys].reset_index() if added_keys else pd.DataFrame(columns=[args.key] + list(new.columns))
    removed = old.loc[removed_keys].reset_index() if removed_keys else pd.DataFrame(columns=[args.key] + list(old.columns))
    changed = pd.DataFrame(changes)

    added.to_csv(output_dir / "mapping_rows_added.csv", index=False)
    removed.to_csv(output_dir / "mapping_rows_removed.csv", index=False)
    changed.to_csv(output_dir / "mapping_cell_changes.csv", index=False)

    summary = {
        "old_rows": int(len(old)),
        "new_rows": int(len(new)),
        "rows_added": int(len(added)),
        "rows_removed": int(len(removed)),
        "cell_changes": int(len(changed)),
        "changed_rows": int(changed[args.key].nunique() if not changed.empty else 0),
    }
    (output_dir / "mapping_change_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    lines = [
        "# NAICS-HS Mapping Change Log",
        "",
        f"- Old rows: {summary['old_rows']:,}",
        f"- New rows: {summary['new_rows']:,}",
        f"- Rows added: {summary['rows_added']:,}",
        f"- Rows removed: {summary['rows_removed']:,}",
        f"- Rows changed: {summary['changed_rows']:,}",
        f"- Cell changes: {summary['cell_changes']:,}",
        "",
        "Review `mapping_cell_changes.csv` for field-level changes.",
    ]
    (output_dir / "mapping_change_log.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
