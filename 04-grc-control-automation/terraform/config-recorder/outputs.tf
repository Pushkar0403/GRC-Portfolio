output "evidence_bucket_name" {
  description = "Bucket receiving AWS Config history and snapshots. Preserve its contents as audit evidence."
  value       = aws_s3_bucket.config_evidence.bucket
}

output "configuration_recorder_name" {
  value = aws_config_configuration_recorder.s3_only.name
}

output "delivery_channel_name" {
  value = aws_config_delivery_channel.s3_evidence.name
}
