from __future__ import annotations

from datetime import UTC, datetime, timedelta

import boto3
from moto import mock_aws

from scripts.export_iam_inventory import export_inventory


@mock_aws
def test_export_includes_mfa_and_access_key_age() -> None:
    iam = boto3.client("iam", region_name="us-east-1")
    iam.create_user(UserName="grc-demo-user")
    access_key = iam.create_access_key(UserName="grc-demo-user")["AccessKey"]

    records = export_inventory(iam, now=datetime.now(UTC) + timedelta(days=10))

    assert len(records) == 1
    assert records[0]["user_name"] == "grc-demo-user"
    assert records[0]["mfa_enabled"] is False
    assert records[0]["access_key_id"] == access_key["AccessKeyId"]
    assert records[0]["access_key_age_days"] >= 9
