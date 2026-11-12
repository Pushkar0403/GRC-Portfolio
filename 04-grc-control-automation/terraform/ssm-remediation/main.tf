terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "name_prefix" {
  type    = string
  default = "grc-demo"
}

provider "aws" { region = var.aws_region }

data "aws_iam_policy_document" "automation_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ssm.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "automation" {
  name               = "${var.name_prefix}-s3-public-access-automation-role"
  assume_role_policy = data.aws_iam_policy_document.automation_assume_role.json
}

resource "aws_iam_role_policy" "automation" {
  name = "${var.name_prefix}-s3-public-access-automation-policy"
  role = aws_iam_role.automation.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["s3:GetBucketPublicAccessBlock", "s3:PutBucketPublicAccessBlock"]
      Resource = "*"
    }]
  })
}

resource "aws_ssm_document" "reapply_s3_public_access_block" {
  name            = "${var.name_prefix}-reapply-s3-public-access-block"
  document_type   = "Automation"
  document_format = "YAML"
  content         = <<-YAML
    schemaVersion: '0.3'
    description: Reapply all S3 Block Public Access settings. DryRun defaults to true.
    parameters:
      BucketName:
        type: String
        description: Existing S3 bucket name to assess or remediate.
      DryRun:
        type: String
        default: 'true'
        allowedValues: ['true', 'false']
        description: true reports only; false changes the bucket configuration.
      AutomationAssumeRole:
        type: String
        default: '${aws_iam_role.automation.arn}'
    assumeRole: '{{ AutomationAssumeRole }}'
    mainSteps:
      - name: ApplyPublicAccessBlock
        action: aws:executeScript
        isEnd: true
        inputs:
          Runtime: python3.11
          Handler: handler
          InputPayload:
            BucketName: '{{ BucketName }}'
            DryRun: '{{ DryRun }}'
          Script: |-
            import boto3
            def handler(events, context):
                bucket = events['BucketName']
                if events.get('DryRun', 'true').lower() == 'true':
                    return {'status': 'WOULD_REMEDIATE', 'bucket': bucket}
                boto3.client('s3').put_public_access_block(
                    Bucket=bucket,
                    PublicAccessBlockConfiguration={
                        'BlockPublicAcls': True,
                        'IgnorePublicAcls': True,
                        'BlockPublicPolicy': True,
                        'RestrictPublicBuckets': True})
                return {'status': 'REMEDIATED', 'bucket': bucket}
  YAML
}

output "automation_document_name" { value = aws_ssm_document.reapply_s3_public_access_block.name }
