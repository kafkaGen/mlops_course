FROM prom/prometheus:v2.36.2

COPY configs/prometheus/prometheus.yaml /etc/prometheus/prometheus.yaml
