FROM prom/prometheus:v2.36.2

COPY configs/prometheus/prometheus-ecs.yaml /etc/prometheus/prometheus.yml
