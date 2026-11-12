from __future__ import annotations

import boto3
from moto import mock_aws

from scripts.check_s3_public_access import REQUIRED_BLOCKS, evaluate_buckets


@mock_aws
def test_all_enabled_bucket_is_compliant() -> None:
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket="grc-demo-compliant-bucket")
    s3.put_public_access_block(
        Bucket="grc-demo-compliant-bucket",
        PublicAccessBlockConfiguration={setting: True for setting in REQUIRED_BLOCKS},
    )

    report = evaluate_buckets(s3)

    assert report["summary"] == {
        "buckets_checked": 1,
        "compliant": 1,
        "non_compliant": 0,
        "errors": 0,
    }
    assert report["findings"][0]["status"] == "COMPLIANT"


@mock_aws
def test_missing_block_configuration_is_non_compliant() -> None:
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket="grc-demo-noncompliant-bucket")

    report = evaluate_buckets(s3)

    assert report["summary"]["non_compliant"] == 1
    finding = report["findings"][0]
    assert finding["status"] == "NON_COMPLIANT"
    assert finding["missing_or_disabled_settings"] == list(REQUIRED_BLOCKS)
