FROM --platform=linux/amd64 python:3.11-buster

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
ENV DJANGO_SETTINGS_MODULE 'config.settings'

RUN  apt-get update && apt-get install -y \
     gettext \
     && rm -rf /var/lib/apt/lists/* \
     && mkdir -p /opt/app/static/ \
     && mkdir -p /opt/app/media/ \
     && pip install --upgrade pip

COPY run_uwsgi.sh run_uwsgi.sh
COPY requirements.txt requirements.txt

RUN  pip install -r requirements.txt --no-cache-dir

COPY uwsgi/uwsgi.ini uwsgi.ini
COPY . .

RUN chmod +x run_uwsgi.sh

EXPOSE 8000

ENTRYPOINT ["/opt/app/run_uwsgi.sh"]