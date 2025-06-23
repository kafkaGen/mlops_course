FROM grafana/grafana:10.1.0

COPY configs/grafana/provisioning-ecs /etc/grafana/provisioning
COPY configs/grafana/dashboards /var/lib/grafana/dashboards
