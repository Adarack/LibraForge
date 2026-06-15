FROM sandreas/m4b-tool@sha256:3154399019ed6a2d26fd477f71a1367e4c60e605d0188699028ad3444afd3c70

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    SCRIPTS_DIR=/app/scripts \
    REPORTS_DIR=/app/reports \
    PATH=/opt/venv/bin:$PATH

RUN apk add --no-cache ffmpeg python3 py3-pip \
    && python3 -m venv /opt/venv

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app /app/app
COPY scripts /app/scripts
COPY config /app/config
RUN mkdir -p /app/reports

EXPOSE 5056
ENTRYPOINT []
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5056"]
