"""AWS Config custom rule: require all bucket Block Public Access settings."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

import boto3
from botocore.exceptions import ClientError

SETTINGS = ("BlockPublicAcls", "IgnorePublicAcls", "BlockPublicPolicy", "RestrictPublicBuckets")
DELETED_STATUSES = {"ResourceDeleted", "ResourceNotRecorded"}


def evaluate(configuration_item: dict[str, Any], s3_client: Any) -> tuple[str, str]:
    """Return AWS Config compliance and a short annotation for one S3 bucket."""
    if configuration_item.get("resourceType") != "AWS::S3::Bucket":
        return "NOT_APPLICABLE", "The resource is not an S3 bucket."
    if configuration_item.get("configurationItemStatus") in DELETED_STATUSES:
        return "NOT_APPLICABLE", "The bucket is deleted or not recorded."
    bucket = configuration_item["resourceName"]
    try:
        configuration = s3_client.get_public_access_block(Bucket=bucket)["PublicAccessBlockConfiguration"]
    except ClientError as error:
        if error.response["Error"].get("Code") == "NoSuchPublicAccessBlockConfiguration":
            return "NON_COMPLIANT", "Bucket has no Block Public Access configuration."
        raise
    missing = [setting for setting in SETTINGS if configuration.get(setting) is not True]
    if missing:
        return "NON_COMPLIANT", "Disabled settings: " + ", ".join(missing)
    return "COMPLIANT", "All four Block Public Access settings are enabled."


def parse_capture_time(capture_time: Any) -> datetime:
    """Return an aware ordering timestamp accepted by AWS Config."""
    if isinstance(capture_time, datetime):
        return capture_time.replace(tzinfo=timezone.utc) if capture_time.tzinfo is None else capture_time
    if not isinstance(capture_time, str):
        raise ValueError("configurationItemCaptureTime must be an ISO-8601 string or datetime")
    try:
        parsed = datetime.fromisoformat(capture_time.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError("configurationItemCaptureTime is not a valid ISO-8601 timestamp") from error
    return parsed.replace(tzinfo=timezone.utc) if parsed.tzinfo is None else parsed


def configuration_item_for_event(invoking_event: dict[str, Any], config_client: Any) -> dict[str, Any]:
    """Get the full item, looking it up when Config sends an oversized event."""
    message_type = invoking_event.get("messageType")
    if message_type == "ConfigurationItemChangeNotification":
        item = invoking_event.get("configurationItem")
        if not isinstance(item, dict):
            raise ValueError("ConfigurationItemChangeNotification has no configurationItem")
        return item
    if message_type != "OversizedConfigurationItemChangeNotification":
        raise ValueError(f"Unsupported AWS Config message type: {message_type!r}")

    summary = invoking_event.get("configurationItemSummary")
    if not isinstance(summary, dict):
        raise ValueError("Oversized notification has no configurationItemSummary")
    try:
        history = config_client.get_resource_config_history(
            resourceType=summary["resourceType"],
            resourceId=summary["resourceId"],
            laterTime=parse_capture_time(summary["configurationItemCaptureTime"]),
            limit=1,
        )
        return history["configurationItems"][0]
    except (KeyError, IndexError) as error:
        raise ValueError("Could not retrieve a configuration item for oversized notification") from error


def lambda_handler(event: dict[str, Any], _context: Any) -> dict[str, str]:
    """Evaluate a Config event and report the result to AWS Config."""
    if not isinstance(event, dict) or not isinstance(event.get("invokingEvent"), str):
        raise ValueError("AWS Config event must include an invokingEvent string")
    if not isinstance(event.get("resultToken"), str):
        raise ValueError("AWS Config event must include a resultToken")
    try:
        invoking_event = json.loads(event["invokingEvent"])
    except json.JSONDecodeError as error:
        raise ValueError("invokingEvent is not valid JSON") from error
    if not isinstance(invoking_event, dict):
        raise ValueError("invokingEvent must be a JSON object")

    config = boto3.client("config")
    item = configuration_item_for_event(invoking_event, config)
    try:
        resource_type = item["resourceType"]
        resource_id = item["resourceId"]
        ordering_timestamp = parse_capture_time(item["configurationItemCaptureTime"])
    except KeyError as error:
        raise ValueError(f"Configuration item is missing {error.args[0]}") from error
    compliance, annotation = evaluate(item, boto3.client("s3"))
    response = config.put_evaluations(
        Evaluations=[
            {
                "ComplianceResourceType": resource_type,
                "ComplianceResourceId": resource_id,
                "ComplianceType": compliance,
                "Annotation": annotation[:256],
                "OrderingTimestamp": ordering_timestamp,
            }
        ],
        ResultToken=event["resultToken"],
    )
    if response.get("FailedEvaluations"):
        raise RuntimeError(f"AWS Config rejected evaluations: {response['FailedEvaluations']}")
    return {"compliance": compliance, "annotation": annotation}
