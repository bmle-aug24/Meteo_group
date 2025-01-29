from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import subprocess
import os

# Définir le chemin de ton script de monitoring
SCRIPT_PATH = "/opt/airflow/dags/monitoring/drift_monitoring.py"  # Assure-toi que le chemin correspond

# Fonction pour exécuter le script Python
def run_drift_monitoring():
    subprocess.run(["python", SCRIPT_PATH], check=True)

# Définir le DAG
default_args = {
    "owner": "airflow",
    "retries": 1,
}

with DAG(
    dag_id="monitoring_dag",
    default_args=default_args,
    description="DAG pour exécuter le monitoring de dérive",
    schedule_interval="0 0 * * *",  # Exécution quotidienne à minuit
    start_date=days_ago(1),
    catchup=False,
) as dag:

    # Définir une tâche pour exécuter le monitoring
    monitoring_task = PythonOperator(
        task_id="run_drift_monitoring",
        python_callable=run_drift_monitoring,
    )
