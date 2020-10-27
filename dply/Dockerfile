FROM python:3.9.0-slim

ENV http_proxy=http://proxy.klima.ads.local:2080/ \
    https_proxy=http://proxy.klima.ads.local:2080/ \
    no_proxy=10.3.0.0/16

WORKDIR /opt/hl7v2_listener
COPY hl7v2_listener/requirements .
RUN pip3 install -r requirements

EXPOSE 8788

COPY hl7v2_listener/app.py .

CMD ["python", "./app.py"]

LABEL org.opencontainers.image.authors="DBMI" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.vendor="DBMI" \
      org.opencontainers.image.title="hl7v2_listener"