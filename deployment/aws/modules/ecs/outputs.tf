data "aws_instances" "ecs_instances" {
  filter {
    name   = "tag:Name"
    values = ["ecs-instance"]
  }

  filter {
    name   = "instance-state-name"
    values = ["running"]
  }

  depends_on = [aws_autoscaling_group.ecs]
}

data "aws_instance" "ecs_instance" {
  instance_id = element(data.aws_instances.ecs_instances.ids, 0)
}

output "ecs_instance_public_dns" {
  description = "Public DNS of ECS EC2 instance"
  value       = data.aws_instance.ecs_instance.public_dns
}