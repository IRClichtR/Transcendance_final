FROM  python:3.9

RUN apt-get update && apt-get install -y postgresql-client
ENV   PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt


COPY . /app
RUN chmod +x /app/entrypoint.sh
COPY ./server_ignition.py /app/backend_server
ENTRYPOINT /app/entrypoint.sh
