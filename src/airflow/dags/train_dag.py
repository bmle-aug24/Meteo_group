from airflow import DAG
from airflow.utils.dates import days_ago            #type: ignore
from airflow.operators.python import PythonOperator #type: ignore
from tools import *           #type: ignore

with DAG(
    dag_id='Train',
    description='Data preprocessing and model training',
    tags=['project', 'docker'],
    schedule_interval = '@weekly',
    default_args={
        'owner': 'admin',
        'start_date': days_ago(0, minute=1),
    },
    catchup=False
) as dag:
    preprocess_task = PythonOperator(task_id='start_preprocess_container',
                                     python_callable=start_existing_container,
                                     op_kwargs={'container_name': 'meteo_group-preprocessing-1'})
    training_task = PythonOperator(task_id='start_training_container',
                                    python_callable=start_existing_container,
                                    op_kwargs={'container_name': 'meteo_group-train_service-1'})
    
    update_model_task = PythonOperator(task_id='update_model',
                                       python_callable=load_model_script,
                                       op_kwargs={'model_name': 'model', 'alias': 'model_last'})
       
    preprocess_task >> training_task >> update_model_task
