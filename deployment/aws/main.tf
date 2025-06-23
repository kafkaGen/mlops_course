module "remote_state_backend" {
  source          = "./modules/remote-state"
  bucket_name     = "prompt-injection-classifier-terraform-state-bucket"
  lock_table_name = "terraform-locks"
  tags = {
    project = "prompt-injection"
  }
}

module "ecr" {
  source = "./modules/ecr"
  repositories = var.ecr_repositories
}

module "ecs" {
  source           = "./modules/ecs"
  repository_urls  = module.ecr.repository_urls
  wandb_api_key    = var.wandb_api_key
}