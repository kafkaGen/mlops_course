variable "ecr_repositories" {
  description = "List of ECR repositories to create"
  type        = list(string)
}

variable "wandb_api_key" {
  description = "API Key for W&B"
  type        = string
  sensitive   = true
}
