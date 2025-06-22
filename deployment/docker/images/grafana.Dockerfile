FROM grafana/grafana:10.1.0

COPY configs/grafana/provisioning /etc/grafana/provisioning
COPY configs/grafana/dashboards /var/lib/grafana/dashboards
