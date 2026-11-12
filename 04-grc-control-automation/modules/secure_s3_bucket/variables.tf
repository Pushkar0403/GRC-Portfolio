variable "bucket_name" {
  description = "Globally unique S3 bucket name; use the grc-demo- prefix for test resources."
  type        = string
}

variable "tags" {
  description = "Tags to add to the bucket."
  type        = map(string)
  default     = {}
}
