# CI/CD Pipeline and Deployment (Phase 5)

This document describes the continuous integration and deployment (CI/CD) setup implemented for the Prompt Injection Classification system. The pipeline ensures reproducible training, infrastructure automation, and seamless deployment of all system components to AWS ECS.

## CI/CD Overview
The project uses GitHub Actions to orchestrate the CI/CD pipeline. The pipeline automates the following:

1. Code Quality Checks: Ensures consistent code formatting and linting using pre-commit.

2. Infrastructure Provisioning: Uses Terraform to deploy and manage cloud resources (VPC, ECS, EC2, ECR, etc.).

3. Model Training & Promotion: Retrains the FastText model and automatically promotes it to the W&B model registry if performance improves.

4. Docker Image Build & Push: Builds custom Docker images and pushes them to AWS ECR.

5. ECS Deployment: Restarts the ECS task to pull new Docker images and serve updated components.

6. Infra Teardown (optional): Dedicated workflow to destroy infrastructure if needed.

## Key Pipeline Features

### ✅ Model Training Enhancements

The training script now auto-promotes the model in Weights & Biases (W&B) model registry as the latest version if the new model achieves higher F1-score than the current latest version.

A standalone training pipeline script was created. It is driven by a YAML config and handles:

- Data fetching
- Preprocessing
- Dataset splitting
- Training
- Logging to W&B
- Saving the model

### ✅ GitHub Actions Trigger on Config Change

A GitHub Actions workflow is set to trigger automatically when:

- The training config file configs/training/train.yaml changes
- Source code or Docker image definitions are updated

## Local Development & Workflow Testing

Install act for local GitHub Actions testing
To test workflows locally, we use act. Instructions are available in the help/ folder.

``` bash
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
```

Use .env.local and .secrets.local

Create two files at the project root:

- .env.local: for env vars like AWS_REGION
- .secrets.local: for GitHub secrets like AWS_ACCESS_KEY_ID

Then run:

``` bash
act -j build-and-push-images --env-file .env.local --secret-file .secrets.local
```

## Infrastructure Setup

### ✅ Terraform-Based Infrastructure

Infrastructure as code is managed using Terraform modules under deployment/aws/.
The following resources are provisioned:

- VPC with public subnet
- EC2 instances with ECS Agent installed
- ECS Cluster with EC2 launch type
- AWS ECR repositories for:
    - fastapi-app-prompt-injection-classifier
    - custom-prometheus
    - custom-grafana
- IAM roles, security groups, and instance profiles
- Remote S3 state backend and DynamoDB locking

### 🔧 Install Terraform Locally

To use Terraform locally:

``` bash
# Or use the official site:
https://developer.hashicorp.com/terraform/downloads
```

``` bash
cd deployment/aws
terraform init
terraform apply
```

## GitHub Actions Workflows

`.github/workflows/build-deploy.yaml`
Used to retrain the FastText model and push it to the W&B model registry.

`.github/workflows/build-deploy.yml`
Orchestrates the end-to-end build, deploy, and retrain process:

- pre-commit-check: Code quality enforcement
- provision-infra: Terraform apply
- build-and-push-images: Docker build and push to ECR
- deploy-to-ecs: Forces ECS to pull latest images and restart containers

`.github/workflows/shutdown-infra.yml`
Used to destroy all infrastructure:

- Safely destroys VPC, ECS cluster, EC2 instances, and all supporting resources
- Leaves Docker images in ECR intact

Run this workflow manually from the GitHub UI when you want to clean up the environment.
