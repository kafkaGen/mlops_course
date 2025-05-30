# Model Deployment (Phase 3)

In this third phase of my MLOps project, I focused on deploying the prompt injection detection model that I trained and evaluated in [Phase 2](./ModelTrainingAndEvaluation.md). My goal was to make the model accessible via an API and to set up robust deployment pipelines using both Docker and Kubernetes for different needs.

## 1. FastAPI Service for Model Serving

I implemented a model serving application using FastAPI. This provides a RESTful API endpoint that accepts user prompts and returns predictions indicating whether a prompt is an injection attempt.

Key aspects of the FastAPI service include:

- **Configuration via `.env` file**: I designed the service to be configurable through environment variables loaded from a `.env` file. This allows for easy management of settings like API keys, model paths, and other environment-specific parameters without needing to modify the code.
- **Integration with Model Registry**: The service integrates with the Weights & Biases Model Registry (set up in Phase 2) to load the appropriate version of the trained model. This ensures that the deployed service always uses the intended model.

## 2. Deployment with Docker & Docker Compose

To ensure consistency and ease of deployment, I containerized the FastAPI application using Docker.

- **Containerization**: The Dockerfile packages the application and all its dependencies.
- **Orchestration**: I used Docker Compose to manage the deployment of the application alongside other services that are part of my MLOps infrastructure (e.g., MinIO, Label Studio).

I created Makefile commands to simplify the lifecycle management:

- To start all Docker-based services, including the model API:

  ```bash
  make run-docker-services
  ```

- To test the deployed API endpoint:

  ```bash
  python src/test/test_api.py
  ```

## 3. Deployment with Kubernetes (using Kind)

For a more scalable and production-like deployment, I also set up a deployment pipeline using Kubernetes, with `kind` (Kubernetes in Docker) for local development and testing.

This setup allows me to:

- Simulate a production Kubernetes environment locally.
- Test Kubernetes configurations, including auto-scaling.

I've streamlined the Kubernetes lifecycle management with the following Makefile commands:

- To start the local Kubernetes cluster (Kind):

  ```bash
  make run-kubernetes-server
  ```

- To deploy the model serving application to the Kubernetes cluster:

  ```bash
  make run-kubernetes-app
  ```

- To monitor the application running in Kubernetes (e.g., check logs, resource usage):

  ```bash
  make monitor-kubernetes-app
  ```

- To perform load testing on the application and observe its behavior under stress (download hey from https://github.com/rakyll/hey):

  ```bash
  make test-kubernetes-app
  ```

- To stop/undeploy the application from the Kubernetes cluster:

  ```bash
  make stop-kubernetes-app
  ```

- To shut down the local Kubernetes cluster (Kind):

  ```bash
  make stop-kubernetes-server
  ```
