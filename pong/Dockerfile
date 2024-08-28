FROM python:latest
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN apt-get update && apt-get install -y postgresql-client

WORKDIR /app
COPY requirements.txt /app/requirements.txt
COPY entrypoint.sh /app/entrypoint.sh
# COPY ./pythpong /app/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN ls -la /app

ENTRYPOINT ["/bin/sh", "-c", "chmod +x /app/entrypoint.sh && /app/entrypoint.sh"]
