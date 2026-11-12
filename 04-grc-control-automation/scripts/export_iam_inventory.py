#!/usr/bin/env python3
"""Export IAM user MFA and access-key-age evidence without changing AWS."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import boto3

FIELDS = ("user_name", "user_id", "arn", "mfa_enabled", "access_key_id", "access_key_age_days")


def access_key_age_days(created: datetime, now: datetime) -> int:
    """Return whole UTC days since an IAM access key was created."""
    return max(0, (now - created.astimezone(UTC)).days)


def export_inventory(iam_client: Any, now: datetime | None = None) -> list[dict[str, Any]]:
    """Collect one record per IAM user/access key, including users without keys."""
    now = now or datetime.now(UTC)
    records: list[dict[str, Any]] = []
    for page in iam_client.get_paginator("list_users").paginate():
        for user in page["Users"]:
            user_name = user["UserName"]
            mfa_enabled = bool(iam_client.list_mfa_devices(UserName=user_name)["MFADevices"])
            keys = iam_client.list_access_keys(UserName=user_name)["AccessKeyMetadata"]
            base = {
                "user_name": user_name,
                "user_id": user["UserId"],
                "arn": user["Arn"],
                "mfa_enabled": mfa_enabled,
            }
            if not keys:
                records.append({**base, "access_key_id": "", "access_key_age_days": ""})
            for key in keys:
                records.append(
                    {
                        **base,
                        "access_key_id": key["AccessKeyId"],
                        "access_key_age_days": access_key_age_days(key["CreateDate"], now),
                    }
                )
    return records


def write_evidence(records: list[dict[str, Any]], json_path: Path, csv_path: Path) -> None:
    """Write the same inventory to JSON and CSV evidence files."""
    for path in (json_path, csv_path):
        path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(records, indent=2, default=str) + "\n", encoding="utf-8")
    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(records)


def main() -> None:
    parser = argparse.ArgumentParser(description="Export IAM users, MFA, and access-key age.")
    parser.add_argument("--json-output", type=Path, default=Path("evidence/iam_inventory.json"))
    parser.add_argument("--csv-output", type=Path, default=Path("evidence/iam_inventory.csv"))
    args = parser.parse_args()
    records = export_inventory(boto3.client("iam"))
    write_evidence(records, args.json_output, args.csv_output)
    print(f"Exported {len(records)} IAM inventory records.")
    print(f"JSON: {args.json_output}")
    print(f"CSV: {args.csv_output}")


if __name__ == "__main__":
    main()
