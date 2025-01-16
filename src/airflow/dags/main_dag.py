from airflow import DAG
from airflow.utils.dates import days_ago 
from airflow.operators.docker_operator import DockerOperator 
from docker.types import Mount 

with DAG(
    dag_id='Ingestion',
    description='Data collection and save in csv file',
    tags=['project', 'docker'],
    schedule_interval = '@daily',
    default_args={
        'owner': 'admin',
        'start_date': days_ago(0, minute=1),
    },
    catchup=False
) as dag:

    ingestion_task = DockerOperator(
        task_id='ingestion',
        image='ingestion',
        auto_remove=True,
        mounts=[Mount(source="meteo_group_data_raw", target="/app/data/raw", type="volume")]
    )