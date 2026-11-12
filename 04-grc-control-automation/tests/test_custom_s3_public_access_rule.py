from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

import boto3
import pytest
from botocore.exceptions import ClientError
from moto import mock_aws

from handlers import custom_s3_public_access_rule as rule
from handlers.custom_s3_public_access_rule import SETTINGS, evaluate


def bucket_item(name: str) -> dict[str, str]:
    return {
        "resourceType": "AWS::S3::Bucket",
        "resourceId": name,
        "resourceName": name,
        "configurationItemStatus": "OK",
        "configurationItemCaptureTime": "2026-11-11T12:00:00Z",
    }


@mock_aws
def test_custom_rule_marks_unconfigured_bucket_non_compliant() -> None:
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket="grc-demo-rule-bucket")

    compliance, _ = evaluate(bucket_item("grc-demo-rule-bucket"), s3)

    assert compliance == "NON_COMPLIANT"


@mock_aws
def test_custom_rule_marks_protected_bucket_compliant() -> None:
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket="grc-demo-protected-rule-bucket")
    s3.put_public_access_block(
        Bucket="grc-demo-protected-rule-bucket",
        PublicAccessBlockConfiguration={setting: True for setting in SETTINGS},
    )

    compliance, _ = evaluate(bucket_item("grc-demo-protected-rule-bucket"), s3)

    assert compliance == "COMPLIANT"


@mock_aws
def test_custom_rule_marks_partially_protected_bucket_non_compliant() -> None:
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket="grc-demo-partial-rule-bucket")
    s3.put_public_access_block(
        Bucket="grc-demo-partial-rule-bucket",
        PublicAccessBlockConfiguration={setting: setting != "BlockPublicPolicy" for setting in SETTINGS},
    )

    compliance, annotation = evaluate(bucket_item("grc-demo-partial-rule-bucket"), s3)

    assert compliance == "NON_COMPLIANT"
    assert "BlockPublicPolicy" in annotation


def test_custom_rule_marks_deleted_bucket_not_applicable() -> None:
    item = bucket_item("deleted-bucket")
    item["configurationItemStatus"] = "ResourceDeleted"

    compliance, _ = evaluate(item, object())

    assert compliance == "NOT_APPLICABLE"


class FakeConfig:
    def __init__(self, history_item: dict[str, Any] | None = None, failed: list[dict[str, str]] | None = None) -> None:
        self.history_item = history_item
        self.failed = failed or []
        self.history_calls: list[dict[str, Any]] = []
        self.evaluations: list[dict[str, Any]] = []

    def get_resource_config_history(self, **kwargs: Any) -> dict[str, Any]:
        self.history_calls.append(kwargs)
        return {"configurationItems": [] if self.history_item is None else [self.history_item]}

    def put_evaluations(self, **kwargs: Any) -> dict[str, Any]:
        self.evaluations.append(kwargs)
        return {"FailedEvaluations": self.failed}


class FakeS3:
    def __init__(self, configuration: dict[str, bool] | None = None, error: ClientError | None = None) -> None:
        self.configuration = configuration
        self.error = error

    def get_public_access_block(self, **_kwargs: Any) -> dict[str, Any]:
        if self.error:
            raise self.error
        return {"PublicAccessBlockConfiguration": self.configuration}


def invoke_event(message_type: str, payload_key: str, item: dict[str, Any]) -> dict[str, str]:
    return {
        "resultToken": "token",
        "invokingEvent": json.dumps({"messageType": message_type, payload_key: item}),
    }


def test_lambda_handles_oversized_event_and_uses_aware_timestamp(monkeypatch: pytest.MonkeyPatch) -> None:
    item = bucket_item("oversized-bucket")
    history_item = dict(item)
    history_item["configurationItemCaptureTime"] = datetime(2026, 11, 11, 12, tzinfo=timezone.utc)
    config = FakeConfig(history_item=history_item)
    s3 = FakeS3({setting: True for setting in SETTINGS})
    monkeypatch.setattr(rule.boto3, "client", lambda service: config if service == "config" else s3)

    result = rule.lambda_handler(
        invoke_event("OversizedConfigurationItemChangeNotification", "configurationItemSummary", item), None
    )

    assert result["compliance"] == "COMPLIANT"
    assert config.history_calls[0]["resourceType"] == "AWS::S3::Bucket"
    assert config.history_calls[0]["laterTime"] == datetime(2026, 11, 11, 12, tzinfo=timezone.utc)
    assert config.evaluations[0]["Evaluations"][0]["OrderingTimestamp"].tzinfo is not None


def test_lambda_rejects_malformed_event(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(rule.boto3, "client", lambda _service: FakeConfig())

    with pytest.raises(ValueError, match="valid JSON"):
        rule.lambda_handler({"resultToken": "token", "invokingEvent": "not-json"}, None)


def test_lambda_raises_when_config_rejects_evaluation(monkeypatch: pytest.MonkeyPatch) -> None:
    item = bucket_item("rejected-bucket")
    config = FakeConfig(failed=[{"ComplianceResourceId": "rejected-bucket"}])
    s3 = FakeS3({setting: True for setting in SETTINGS})
    monkeypatch.setattr(rule.boto3, "client", lambda service: config if service == "config" else s3)

    with pytest.raises(RuntimeError, match="rejected evaluations"):
        rule.lambda_handler(invoke_event("ConfigurationItemChangeNotification", "configurationItem", item), None)


def test_lambda_propagates_s3_api_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    item = bucket_item("denied-bucket")
    config = FakeConfig()
    error = ClientError({"Error": {"Code": "AccessDenied", "Message": "denied"}}, "GetPublicAccessBlock")
    monkeypatch.setattr(rule.boto3, "client", lambda service: config if service == "config" else FakeS3(error=error))

    with pytest.raises(ClientError):
        rule.lambda_handler(invoke_event("ConfigurationItemChangeNotification", "configurationItem", item), None)
