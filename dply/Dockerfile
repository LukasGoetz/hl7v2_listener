FROM python:3.9.0-slim

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
