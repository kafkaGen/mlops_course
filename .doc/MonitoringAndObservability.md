# Monitoring and Observability (Phase 4)

This document describes the monitoring system integrated into the Prompt Injection Classification project. The monitoring pipeline is fully automated and deployed alongside the application.

## Monitoring Stack Overview

Monitoring is powered by **Prometheus** and **Grafana**, with the following components:

* **Prometheus**: Scrapes and stores metrics from the application and the system.

  * **Node Exporter**: Captures host machine metrics.
  * **cAdvisor**: Captures container-level metrics (CPU, memory, disk I/O, network I/O).
* **Grafana**: Visualizes metrics in structured dashboards.

Both Prometheus and Grafana are configured automatically using provisioning files.

## Dashboards Available

After starting the monitoring stack, you can find the following dashboards in Grafana:

### 1. System Metrics Dashboard

This dashboard provides detailed insights into system-level performance and container health:

* **CPU usage** (host and per-container)
* **Memory usage** (host and per-container)
* **Disk space** (host and per-container)
* **Network I/O** (host and per-container, bytes sent/received)
* **Disk I/O** (read/write bytes)
* **Container uptime and restart count**

This is critical for evaluating infrastructure behavior, spotting performance bottlenecks, and detecting container-level issues.

### 2. Prompt Injection Classification App Dashboard

This dashboard focuses on application-level metrics for the text classification API:

* **Requests per minute**: Tracks the frequency of API usage.
* **Average request latency**: Shows how long each prediction request takes to process.
* **Error rate per 5 minutes**: Displays the rate and type of classification or validation errors.
* **Class distribution per minute**: Breakdown of predicted labels over time.
* **Confidence distribution per minute**: Tracks how confident the model is across prediction ranges, broken into fixed buckets (e.g., 0.0–0.2, 0.2–0.4, etc.).

These insights help monitor real-time prediction behavior and model performance.

## Stress Testing the API

To evaluate the robustness of the classification endpoint under load, a stress test script is included. You can run it with:

```bash
make stress-test-endpoint
```

This will generate a high volume of requests to simulate real-world conditions and observe system and model-level performance.

---

This monitoring integration enables detailed observability for both system infrastructure and ML model behavior, helping ensure stability, traceability, and high service quality in production environments.
