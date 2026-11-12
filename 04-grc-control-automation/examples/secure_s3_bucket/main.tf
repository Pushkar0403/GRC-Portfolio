terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 6.0" }
  }
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "bucket_name" {
  type = string
}

provider "aws" {
  region = var.aws_region
}

module "secure_bucket" {
  source      = "../../modules/secure_s3_bucket"
  bucket_name = var.bucket_name
  tags = {
    Project = "grc-control-automation"
    Purpose = "demo"
  }
}
