# MLOps Course Project: LLM Prompt Injection Detection

## Overview

This repository contains the work for an MLOps course project focused on building a robust machine learning pipeline for detecting malicious prompt injections in Large Language Models (LLMs). The project demonstrates the implementation of MLOps best practices through a series of practical tasks, starting with data management and labeling processes.

## Problem Statement

LLM prompt injections represent a significant security threat where malicious users attempt to manipulate AI systems by crafting inputs that bypass safety measures or extract sensitive information. This project aims to build a classification system that can identify potentially harmful prompts, distinguishing between:

- **Clean Prompts**: Normal, safe user inputs
- **Injection Prompts**: Malicious inputs designed to manipulate the system

The [deepset/prompt-injections](https://huggingface.co/datasets/deepset/prompt-injections) dataset from Hugging Face was used, which contains examples of both clean and injection prompts for training and evaluation.

## Project Structure

``` none
mlops_course/
├── data/                  # Dataset storage
├── docker/                # Docker configuration
│   ├── compose/           # Modular docker-compose files
│   └── docker-compose.yaml # Main compose file
├── help/                  # Helper scripts
│   └── download_dataset.py # Script to download and format dataset
├── .dvc/                  # DVC configuration
├── .env                   # Environment variables (not tracked by git)
├── .env.example           # Example environment variables
├── Makefile               # Makefile for common tasks
├── pyproject.toml         # Poetry project configuration
└── poetry.lock            # Poetry lock file
```

## Environment Setup

### Prerequisites

- Python 3.11+, <3.12
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management
- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)

### Setting Up the Python Environment

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd mlops_course
   ```

2. Install dependencies using Poetry:

   ```bash
   poetry install
   ```

3. Activate the virtual environment:

   ```bash
   poetry shell
   ```

4. Set up pre-commit hooks:

   ```bash
   pre-commit install
   ```

5. Create your `.env` file from the example:

   ```bash
   cp .env.example .env
   ```

   Then edit the `.env` file to add your credentials.

## Project Development Stages

This project is developed in several continuous stages, each focusing on different aspects of the MLOps lifecycle. Detailed documentation for each stage is available in the `.doc` directory:

1. [Data Management](.doc/DataManagement.md) - Setting up data acquisition, labeling, and versioning
2. [Model Training and Evaluation](.doc/ModelTrainingAndEvaluation.md) - Training and evaluating a prompt injection detection model, saving to model registry
3. [Model Deployment](.doc/ModelDeployment.md) - Deploying the prompt injection detection model with FastAPI and Kubernetes
4. [Monitoring and Observability](.doc/MonitoringAndObservability.md) - Implementing monitoring and observability for the deployed model
5. [CI/CD Pipeline](Comming Soon) - Setting up a CI/CD pipeline for automated testing and deployment

## License

This project is licensed under the MIT License - see the LICENSE file for details.
