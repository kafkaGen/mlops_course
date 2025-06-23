output "ecr_repository_urls" {
  value = module.ecr.repository_urls
}

output "fastapi_app_public_dns" {
  description = "Public DNS for FastAPI app"
  value       = "http://${module.ecs.ecs_instance_public_dns}:8000"
}

output "prometheus_public_dns" {
  description = "Public DNS for Prometheus monitoring UI"
  value       = "http://${module.ecs.ecs_instance_public_dns}:9090"
}

output "grafana_public_dns" {
  description = "Public DNS for Grafana dashboard"
  value       = "http://${module.ecs.ecs_instance_public_dns}:3000"
}