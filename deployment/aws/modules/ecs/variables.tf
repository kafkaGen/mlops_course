variable "wandb_api_key" {
  description = "W&B API Key"
  type        = string
  sensitive   = true
}

variable "repository_urls" {
  description = "ECR repository URLs from the ECR module"
  type        = map(string)
}
