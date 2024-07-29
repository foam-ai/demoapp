FROM grafana/promtail:latest
COPY config.yaml /etc/promtail/config.yaml
ENTRYPOINT ["promtail", "-config.file=/etc/promtail/config.yaml"]
