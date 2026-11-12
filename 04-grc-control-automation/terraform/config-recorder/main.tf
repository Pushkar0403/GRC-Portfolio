data "aws_caller_identity" "current" {}
data "aws_partition" "current" {}

locals {
  evidence_bucket_name = "${var.name_prefix}-config-evidence-${data.aws_caller_identity.current.account_id}-${var.aws_region}"
  common_tags = merge(
    {
      Project     = "grc-control-automation"
      Environment = "lab"
      Purpose     = "aws-config-evidence"
      ManagedBy   = "terraform"
    },
    var.tags,
  )
}

resource "aws_s3_bucket" "config_evidence" {
  bucket = local.evidence_bucket_name
  tags   = local.common_tags

  # Evidence must be retained deliberately; Terraform destroy will stop here.
  force_destroy = false

  lifecycle {

  }
}

resource "aws_s3_bucket_public_access_block" "config_evidence" {
  bucket = aws_s3_bucket.config_evidence.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "config_evidence" {
  bucket = aws_s3_bucket.config_evidence.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "config_evidence" {
  bucket = aws_s3_bucket.config_evidence.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

data "aws_iam_policy_document" "config_evidence_bucket" {
  statement {
    sid     = "DenyInsecureTransport"
    effect  = "Deny"
    actions = ["s3:*"]
    resources = [
      aws_s3_bucket.config_evidence.arn,
      "${aws_s3_bucket.config_evidence.arn}/*",
    ]
    principals {
      type        = "*"
      identifiers = ["*"]
    }
    condition {
      test     = "Bool"
      variable = "aws:SecureTransport"
      values   = ["false"]
    }
  }

  statement {
    sid       = "AllowConfigToCheckBucketAcl"
    effect    = "Allow"
    actions   = ["s3:GetBucketAcl"]
    resources = [aws_s3_bucket.config_evidence.arn]
    principals {
      type        = "Service"
      identifiers = ["config.amazonaws.com"]
    }
    condition {
      test     = "StringEquals"
      variable = "AWS:SourceAccount"
      values   = [data.aws_caller_identity.current.account_id]
    }
    condition {
      test     = "ArnLike"
      variable = "AWS:SourceArn"
      values = [
        "arn:${data.aws_partition.current.partition}:config:${var.aws_region}:${data.aws_caller_identity.current.account_id}:*",
      ]
    }
  }

  statement {
    sid     = "AllowConfigToDeliverEvidence"
    effect  = "Allow"
    actions = ["s3:PutObject"]
    resources = [
      "${aws_s3_bucket.config_evidence.arn}/${var.evidence_prefix}/AWSLogs/${data.aws_caller_identity.current.account_id}/Config/*",
    ]
    principals {
      type        = "Service"
      identifiers = ["config.amazonaws.com"]
    }
    condition {
      test     = "StringEquals"
      variable = "AWS:SourceAccount"
      values   = [data.aws_caller_identity.current.account_id]
    }
    condition {
      test     = "StringEquals"
      variable = "s3:x-amz-acl"
      values   = ["bucket-owner-full-control"]
    }
    condition {
      test     = "ArnLike"
      variable = "AWS:SourceArn"
      values = [
        "arn:${data.aws_partition.current.partition}:config:${var.aws_region}:${data.aws_caller_identity.current.account_id}:*",
      ]
    }
  }
}

resource "aws_s3_bucket_policy" "config_evidence" {
  bucket = aws_s3_bucket.config_evidence.id
  policy = data.aws_iam_policy_document.config_evidence_bucket.json
}

data "aws_iam_policy_document" "config_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["config.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "config_recorder" {
  name               = "${var.name_prefix}-config-recorder-role"
  assume_role_policy = data.aws_iam_policy_document.config_assume_role.json
  tags               = local.common_tags
}

resource "aws_iam_role_policy_attachment" "config_recorder" {
  role       = aws_iam_role.config_recorder.name
  policy_arn = "arn:${data.aws_partition.current.partition}:iam::aws:policy/service-role/AWS_ConfigRole"
}

resource "aws_config_delivery_channel" "s3_evidence" {
  name           = "${var.name_prefix}-s3-evidence"
  s3_bucket_name = aws_s3_bucket.config_evidence.bucket
  s3_key_prefix  = var.evidence_prefix

  depends_on = [aws_s3_bucket_policy.config_evidence]
}

resource "aws_config_configuration_recorder" "s3_only" {
  name     = "${var.name_prefix}-s3-only"
  role_arn = aws_iam_role.config_recorder.arn

  recording_group {
    all_supported                 = false
    include_global_resource_types = false
    resource_types                = ["AWS::S3::Bucket"]

    recording_strategy {
      use_only = "INCLUSION_BY_RESOURCE_TYPES"
    }
  }

  depends_on = [aws_iam_role_policy_attachment.config_recorder]
}

resource "aws_config_configuration_recorder_status" "s3_only" {
  name       = aws_config_configuration_recorder.s3_only.name
  is_enabled = true

  depends_on = [
    aws_config_delivery_channel.s3_evidence,
    aws_config_configuration_recorder.s3_only,
  ]
}
