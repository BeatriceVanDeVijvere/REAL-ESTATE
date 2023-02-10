from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.docker_operator import DockerOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import os

default_args = {
    'owner'                 : 'airflow',
    'description'           : 'Use of the Operators',
    'depend_on_past'        : False,
    'start_date'            : datetime(2023, 2, 9),
    'email_on_failure'      : 'retdeer48@gmail.com',
    'email_on_retry'        : 'retdeer48@gmail.com',
    'retries'               : 1,
    'retry_delay'           : timedelta(minutes=5),
    'schedule_interval'     : '0 0 * * *'
}
with DAG(
        'web_scraping_dag',
        default_args=default_args,
        schedule_interval="5 * * * *",
        catchup=False
) as dag:
    start_dag =DummyOperator(
        task_id='start_dag'
        )

    t12 = DockerOperator(
    task_id='web_scraping',
    image='airflow_scraper:latest',
    container_name ='task___web_scraping',
    api_version='auto',
    auto_remove=True,
    command="/bin/sleep 30",
    docker_url="unix://var/run/docker.sock",
    network_mode="bridge",
    environment={

    }
    )
    t2 =PythonOperator(
    task_id=' scraping-sitemap',
    bash_command='echo "links"'
    )
    t3 =PythonOperator(
    task_id=' scraping-properties-new',
    bash_command='echo "links"'
    )
    end_dag = DummyOperator(
        task_id='end_dag'
    )
start_dag >> t2 >> t3 >> end_dag
