#!/usr/bin/env python3
"""Create evidence for the S3 Block Public Access account-control check."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import boto3
from botocore.exceptions import ClientError

REQUIRED_BLOCKS = (
    "BlockPublicAcls",
    "IgnorePublicAcls",
    "BlockPublicPolicy",
    "RestrictPublicBuckets",
)


def evaluate_buckets(s3_client: Any) -> dict[str, Any]:
    """Read each bucket's public-access-block setting; this function never mutates AWS."""
    checked_at = datetime.now(UTC).isoformat()
    findings: list[dict[str, Any]] = []

    for bucket in s3_client.list_buckets().get("Buckets", []):
        name = bucket["Name"]
        finding: dict[str, Any] = {"bucket_name": name}
        try:
            configuration = s3_client.get_public_access_block(Bucket=name)[
                "PublicAccessBlockConfiguration"
            ]
            missing = [key for key in REQUIRED_BLOCKS if configuration.get(key) is not True]
            finding["public_access_block"] = configuration
            finding["status"] = "COMPLIANT" if not missing else "NON_COMPLIANT"
            finding["missing_or_disabled_settings"] = missing
        except ClientError as error:
            code = error.response["Error"].get("Code", "Unknown")
            if code == "NoSuchPublicAccessBlockConfiguration":
                finding["status"] = "NON_COMPLIANT"
                finding["missing_or_disabled_settings"] = list(REQUIRED_BLOCKS)
                finding["reason"] = "No bucket-level Block Public Access configuration exists."
            else:
                finding["status"] = "ERROR"
                finding["error_code"] = code
                finding["reason"] = error.response["Error"].get("Message", "AWS API error")
        findings.append(finding)

    non_compliant = sum(item["status"] == "NON_COMPLIANT" for item in findings)
    errors = sum(item["status"] == "ERROR" for item in findings)
    return {
        "control_id": "S3-BLOCK-PUBLIC-ACCESS",
        "checked_at_utc": checked_at,
        "required_settings": list(REQUIRED_BLOCKS),
        "summary": {
            "buckets_checked": len(findings),
            "compliant": sum(item["status"] == "COMPLIANT" for item in findings),
            "non_compliant": non_compliant,
            "errors": errors,
        },
        "findings": findings,
    }


def write_report(report: dict[str, Any], output_path: Path) -> None:
    """Write the evidence report locally, creating its parent directory if needed."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check S3 bucket Block Public Access settings.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("evidence/s3_public_access_report.json"),
        help="Local JSON evidence path (default: evidence/s3_public_access_report.json).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = evaluate_buckets(boto3.client("s3"))
    write_report(report, args.output)
    summary = report["summary"]
    print(f"Evidence written: {args.output}")
    print(
        "Buckets checked: {buckets_checked}; compliant: {compliant}; "
        "non-compliant: {non_compliant}; errors: {errors}".format(**summary)
    )
    return 2 if summary["errors"] else 1 if summary["non_compliant"] else 0


if __name__ == "__main__":
    sys.exit(main())
