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

variable "deploy_conformance_pack" {
  description = "Set true only when ready to deploy AWS Config billable resources."
  type        = bool
  default     = false
}

provider "aws" {
  region = var.aws_region
}

resource "aws_config_conformance_pack" "cis_foundations_mapped" {
  count                 = var.deploy_conformance_pack ? 1 : 0
  conformance_pack_name = "grc-demo-cis-foundations-mapped"
  template_body         = file("${path.module}/../../conformance-pack/grc-demo-cis-foundations-mapped.yaml")
}
