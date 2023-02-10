FROM python:3.9

USER root

RUN mkdir /app

WORKDIR /app

RUN apt update &&  apt upgrade -y\
    apt install -y python3 python3-pip\
    pip3 install --upgrade -r requirements.txt\
    apt install --no-install-recommends lsb-release && \
    tar -xvf archive.tar.gz &&\
    rm -rf /var/lib/apt/lists/* && \
    rm -rf archive.tar.gz \
    apt install pip -y \

COPY scraper/* /app
COPY  requirements.txt .

ENV AIRFLOW_HOME /app/airflow
ENV AIRFLOW_CONFIG /app/airflow/airflow.cfg

CMD ["python3","./scraper.py"]
EXPOSE 3000





