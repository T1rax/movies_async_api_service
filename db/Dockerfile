FROM --platform=linux/amd64 python:3.11-buster

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN  apt-get update && apt-get install -y \
     gettext \
     && rm -rf /var/lib/apt/lists/* \
     && pip install --upgrade pip

COPY run.sh run.sh
COPY requirements.txt requirements.txt

RUN  pip install -r requirements.txt --no-cache-dir

COPY . .

RUN chmod +x run.sh

EXPOSE 8000

ENTRYPOINT ["/opt/app/run.sh"]