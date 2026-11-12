output "managed_rule_name" {
  value = aws_config_config_rule.s3_public_read_prohibited.name
}

output "custom_rule_name" {
  value = aws_config_config_rule.custom_s3_public_access_block.name
}
