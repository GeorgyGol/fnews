FROM tiangolo/meinheld-gunicorn-flask:python3.9
MAINTAINER g.golyshev@gmail.com
RUN apt-get update
#RUN apt-get -y install vim nano

WORKDIR ..

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ./app /app

#ENTRYPOINT bash
ENTRYPOINT  gunicorn --conf gunicorn_conf.py --bind 0.0.0.0:5002 main:app


