from airflow import DAG
from airflow.utils.dates import days_ago            #type: ignore
from airflow.operators.python import PythonOperator #type: ignore
from tools import *                                 #type: ignore

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
    ingestion_task = PythonOperator(task_id='start_ingestion_container',
                                    python_callable=start_existing_container,
                                    op_kwargs={'container_name': 'meteo_group-ingestion-1'})

    ingestion_task 
