terraform {
  backend "s3" {
    bucket         = "prompt-injection-classifier-terraform-state-bucket"
    key            = "aws-infra/terraform.tfstate"
    region         = "eu-central-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
