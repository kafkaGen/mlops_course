variable "bucket_name" {
  type        = string
  description = "Name of the S3 bucket for remote state"
}

variable "lock_table_name" {
  type        = string
  description = "Name of the DynamoDB table for state locking"
}

variable "tags" {
  type    = map(string)
  default = {}
}
