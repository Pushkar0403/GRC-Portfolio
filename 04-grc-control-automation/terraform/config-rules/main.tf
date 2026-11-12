data "archive_file" "custom_s3_rule" {
  type        = "zip"
  source_file = "${path.module}/../../handlers/custom_s3_public_access_rule.py"
  output_path = "${path.module}/custom_s3_public_access_rule.zip"
}

data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

data "aws_caller_identity" "current" {}
data "aws_partition" "current" {}
data "aws_region" "current" {}

resource "aws_iam_role" "custom_rule" {
  name               = "${var.name_prefix}-config-s3-public-access-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

resource "aws_iam_role_policy" "custom_rule" {
  name = "${var.name_prefix}-config-s3-public-access-policy"
  role = aws_iam_role.custom_rule.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:GetBucketPublicAccessBlock"]
        Resource = "arn:${data.aws_partition.current.partition}:s3:::*"
      },
      {
        Effect   = "Allow"
        Action   = ["config:GetResourceConfigHistory", "config:PutEvaluations"]
        Resource = "*"
      },
      {
        Effect   = "Allow"
        Action   = ["logs:CreateLogGroup"]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = ["logs:CreateLogStream", "logs:PutLogEvents"]
        Resource = format(
          "arn:%s:logs:%s:%s:log-group:/aws/lambda/%s:*",
          data.aws_partition.current.partition,
          data.aws_region.current.region,
          data.aws_caller_identity.current.account_id,
          aws_lambda_function.custom_s3_rule.function_name,
        )
      }
    ]
  })
}

resource "aws_lambda_function" "custom_s3_rule" {
  function_name    = "${var.name_prefix}-config-s3-public-access"
  filename         = data.archive_file.custom_s3_rule.output_path
  source_code_hash = data.archive_file.custom_s3_rule.output_base64sha256
  role             = aws_iam_role.custom_rule.arn
  handler          = "custom_s3_public_access_rule.lambda_handler"
  runtime          = "python3.12"
  timeout          = 30
}

resource "aws_config_config_rule" "s3_public_read_prohibited" {
  name = "${var.name_prefix}-s3-bucket-public-read-prohibited"
  source {
    owner             = "AWS"
    source_identifier = "S3_BUCKET_PUBLIC_READ_PROHIBITED"
  }
}

resource "aws_config_config_rule" "custom_s3_public_access_block" {
  name = "${var.name_prefix}-s3-public-access-block-required"
  source {
    owner             = "CUSTOM_LAMBDA"
    source_identifier = aws_lambda_function.custom_s3_rule.arn
    source_detail {
      event_source = "aws.config"
      message_type = "ConfigurationItemChangeNotification"
    }
    source_detail {
      event_source = "aws.config"
      message_type = "OversizedConfigurationItemChangeNotification"
    }
  }
  scope {
    compliance_resource_types = ["AWS::S3::Bucket"]
  }
}

resource "aws_lambda_permission" "allow_config" {
  statement_id   = "AllowExecutionFromConfig"
  action         = "lambda:InvokeFunction"
  function_name  = aws_lambda_function.custom_s3_rule.function_name
  principal      = "config.amazonaws.com"
  source_account = data.aws_caller_identity.current.account_id
}
