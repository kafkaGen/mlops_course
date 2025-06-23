resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = true
  tags = {
    Name = "ecs-vpc"
  }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "eu-central-1a"
  tags = {
    Name = "ecs-public-subnet"
  }
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

resource "aws_security_group" "ecs_sg" {
  name        = "ecs-sg"
  description = "Allow access to app and monitoring ports"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 9090
    to_port     = 9090
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # You can restrict to your IP for security
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_iam_role" "ecs_instance_role" {
  name = "ecs-instance-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = { Service = "ec2.amazonaws.com" }
    }]
  })
}

resource "aws_iam_instance_profile" "ecs_instance_profile" {
  name = "ecs-instance-profile"
  role = aws_iam_role.ecs_instance_role.name
}

resource "aws_iam_role_policy_attachment" "ecs_instance_policy" {
  role       = aws_iam_role.ecs_instance_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
}

resource "aws_ecs_cluster" "main" {
  name = "prompt-injection-cluster"
}

resource "aws_launch_template" "ecs" {
  name_prefix   = "ecs-launch-"
  image_id      = data.aws_ami.ecs.id
  instance_type = "t3.xlarge"
  key_name      = "ec2-debug"
  iam_instance_profile {
    name = aws_iam_instance_profile.ecs_instance_profile.name
  }
  network_interfaces {
    associate_public_ip_address = true
    security_groups             = [aws_security_group.ecs_sg.id]
  }
  user_data = base64encode("#!/bin/bash\necho ECS_CLUSTER=${aws_ecs_cluster.main.name} >> /etc/ecs/ecs.config")
}

data "aws_ami" "ecs" {
  most_recent = true
  owners      = ["amazon"]
  filter {
    name   = "name"
    values = ["amzn2-ami-ecs-hvm-*-x86_64-ebs"]
  }
}

resource "aws_autoscaling_group" "ecs" {
  desired_capacity     = 1
  max_size             = 1
  min_size             = 1
  vpc_zone_identifier  = [aws_subnet.public.id]
  launch_template {
    id      = aws_launch_template.ecs.id
    version = "$Latest"
  }
  tag {
    key                 = "Name"
    value               = "ecs-instance"
    propagate_at_launch = true
  }
  lifecycle {
    ignore_changes = [desired_capacity]
  }
}

resource "aws_cloudwatch_log_group" "monitoring_stack" {
  name              = "/ecs/monitoring-stack"
  retention_in_days = 7
}

resource "aws_ecs_task_definition" "monitoring_stack" {
  depends_on = [aws_cloudwatch_log_group.monitoring_stack]
  family                   = "monitoring-task"
  network_mode             = "bridge"
  requires_compatibilities = ["EC2"]
  cpu                      = "4096"
  memory                   = "8192"

  container_definitions = jsonencode([
    {
      name      = "fastapi-app-prompt-injection-classifier",
      image     = "${lookup(var.repository_urls, "fastapi-app-prompt-injection-classifier")}:latest",
      portMappings = [{ containerPort = 8000, hostPort = 8000 }],
      environment = [
        { name = "WANDB_API_KEY", value = var.wandb_api_key },
        { name = "MODEL_REGISTRY_PROVIDER", value = "wandb" },
        { name = "MODEL_REGISTRY_PROJECT_NAME", value = "model-registry" },
        { name = "MODEL_REGISTRY_MODEL_NAME", value = "Prompt-injection-classifier" },
        { name = "MODEL_REGISTRY_MODEL_ALIAS", value = "latest" },
        { name = "INJECTION_THRESHOLD", value = "0.6" },
        { name = "PROMPT_INJECTION_CLASSIFIER_APP_PORT", value = "8000" }
      ],
      logConfiguration = {
        logDriver = "awslogs",
        options = {
          awslogs-group         = "/ecs/monitoring-stack",
          awslogs-region        = "eu-central-1",
          awslogs-stream-prefix = "fastapi"
        }
      }
    },
    {
      name      = "custom-prometheus",
      image     = "${lookup(var.repository_urls, "custom-prometheus")}:latest",
      portMappings = [{ containerPort = 9090, hostPort = 9090 }],
      logConfiguration = {
        logDriver = "awslogs",
        options = {
          awslogs-group         = "/ecs/monitoring-stack",
          awslogs-region        = "eu-central-1",
          awslogs-stream-prefix = "custom-prometheus"
        }
      }
    },
    {
      name      = "node-exporter",
      image     = "quay.io/prometheus/node-exporter:latest",
      portMappings = [{ containerPort = 9100, hostPort = 9100 }],
      logConfiguration = {
        logDriver = "awslogs",
        options = {
          awslogs-group         = "/ecs/monitoring-stack",
          awslogs-region        = "eu-central-1",
          awslogs-stream-prefix = "node-exporter"
        }
      }
    },
    {
      name      = "cadvisor",
      image     = "gcr.io/google-containers/cadvisor:latest",
      portMappings = [{ containerPort = 8080, hostPort = 8080 }],
      logConfiguration = {
        logDriver = "awslogs",
        options = {
          awslogs-group         = "/ecs/monitoring-stack",
          awslogs-region        = "eu-central-1",
          awslogs-stream-prefix = "cadvisor"
        }
      }
    },
    {
      name      = "custom-grafana",
      image     = "${lookup(var.repository_urls, "custom-grafana")}:latest",
      portMappings = [{ containerPort = 3000, hostPort = 3000 }],
      logConfiguration = {
        logDriver = "awslogs",
        options = {
          awslogs-group         = "/ecs/monitoring-stack",
          awslogs-region        = "eu-central-1",
          awslogs-stream-prefix = "custom-grafana"
        }
      }
    }
  ])
}

resource "aws_ecs_service" "monitoring" {
  name            = "monitoring-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.monitoring_stack.arn
  launch_type     = "EC2"
  desired_count   = 1
}
