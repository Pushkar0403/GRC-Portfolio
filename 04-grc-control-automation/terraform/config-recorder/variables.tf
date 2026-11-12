variable "aws_region" {
  description = "Region in which AWS Config records the S3 bucket resource type."
  type        = string
  default     = "us-east-1"
}

variable "aws_profile" {
  description = "Named AWS CLI SSO profile to use; credentials remain outside Terraform."
  type        = string
  default     = "grc-lab"
}

variable "name_prefix" {
  description = "Lowercase prefix used for all demonstration resources."
  type        = string
  default     = "grc-demo"
}

variable "evidence_prefix" {
  description = "Optional prefix below which AWS Config writes delivered evidence."
  type        = string
  default     = "aws-config"
}

variable "tags" {
  description = "Additional tags to apply to resources that support tags."
  type        = map(string)
  default     = {}
}
