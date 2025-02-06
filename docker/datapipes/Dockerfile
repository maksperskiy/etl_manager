FROM python:3.12 AS base

ENV TZ="Europe/Minsk"

WORKDIR /opt/app

RUN apt-get update && apt-get install -y \
    openjdk-17-jre-headless \
    && rm -rf /var/lib/apt/lists/*

RUN apt -y update \
    && pip3 install --upgrade pip
RUN pip3 install pyspark>=3.0.0 

FROM base

COPY docker/datapipes/requirements.txt /opt/app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install -r requirements.txt 

COPY src/ /opt/app
# RUN python manage.py collectstatic --noinput

# ENTRYPOINT [ "python", "manage.py", "runserver" ]
