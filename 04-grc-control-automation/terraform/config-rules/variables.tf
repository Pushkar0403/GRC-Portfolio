variable "aws_region" {
  description = "AWS region for the custom-rule Lambda. AWS Config records S3 globally."
  type        = string
  default     = "us-east-1"
}

variable "name_prefix" {
  description = "Prefix for resources created by this demonstration."
  type        = string
  default     = "grc-demo"
}
