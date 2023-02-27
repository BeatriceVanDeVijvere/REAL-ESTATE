from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.models.BaseOperator import *
from airflow import DummyOperator
from datetime import datetime, timedelta
from get_container_ip import *
from config_of_connection import *


default_args = {
    'owner'                 : 'airflow',
    'description'           : 'Use of the Operators',
    'depend_on_past'        : False,
    'start_date'            : datetime(2022, 1, 1),
    'email_on_failure'      : 'retdeer48@gmail.com',
    'email_on_retry'        : 'retdeer48@gmail.com',
    'retries'               : 1,
    'retry_delay'           : timedelta(minutes=5),
    'schedule_interval'     : '0 0 * * *'
}
with DAG(
        'web_scraping_dag',
        default_args=default_args,
        catchup=False
) as dag:
    start_dag = DummyOperator(
        task_id='start_dag'
        )

    t1_create_image = BashOperator(
        task_id='create_docker_image',
        bash_command='docker build -t postgres .',
        dag=dag
    )

    t2_run_postgres_container = BashOperator(
        task_id='run_postgres_container',
        bash_command='docker run --name postgres -e POSTGRES_PASSWORD=bea -pp  5432: 5432 - d postgres',
        dag=dag,
    )

    t3_get_container_ip_task = PythonOperator(
        task_id='get_container_ip',
        python_callable=get_container_ip,
        dag=dag,
    )
    t4_web_scraping_links = DockerOperator(
        task_id='web_scraping_links',
        image='airflow_scraper',
        container_name='task___web_scraping',
        api_version='auto',
        auto_remove=True,
        command='python /projecten/REAL-ESTATE/web_scraping_links.py',
        docker_url='unix://var/run/docker.sock',
        network_mode='bridge',
        environment = get_conn_params_from_config
     )

    t4_get_links_information = DockerOperator(
        task_id='get_links_information',
        image='airflow_scraper',
        container_name='task___get_links_information',
        api_version='auto',
        auto_remove=True,
        command='python /projecten/REAL-ESTATE/get_links_information.py',
        docker_url='unix://var/run/docker.sock',
        network_mode='bridge'
    )
    end_dag = DummyOperator(
    task_id='end_dag'
    )


start_dag >> t1_create_image >> t2_run_postgres_container >> t3_get_container_ip_task >> t4_get_links_information >> end_dag
