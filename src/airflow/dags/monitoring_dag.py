from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from airflow.utils.dates import days_ago
import subprocess
import os
import json

# Variables globales
DRIFT_SCRIPT_PATH = "/opt/airflow/dags/monitoring/drift_monitoring.py"
MODEL_COMPARISON_SCRIPT_PATH = "/opt/airflow/dags/monitoring/model_comparison.py"
DRIFT_SUMMARY_PATH = "/opt/airflow/data/monitoring/drift_summary.json"

# Tâche 1 : Détection de dérive
def run_drift_monitoring():
    subprocess.run(["python", DRIFT_SCRIPT_PATH], check=True)

# Tâche 2 : Comparaison des modèles
def run_model_comparison():
    subprocess.run(["python", MODEL_COMPARISON_SCRIPT_PATH], check=True)

# Tâche 3 : Vérification des dérives significatives et alerte
def check_drift_and_alert():
    with open(DRIFT_SUMMARY_PATH, "r") as f:
        drift_summary = json.load(f)

    # Vérifie si une dérive est détectée
    drift_detected = any([col["drift_detected"] for col in drift_summary.values()])

    if drift_detected:
        raise ValueError("Dérive détectée dans les données de production !")

# DAG et tâches
default_args = {
    "owner": "airflow",
    "retries": 1,
}

with DAG(
    dag_id="monitoring_dag",
    default_args=default_args,
    description="DAG pour le monitoring de dérive et comparaison des modèles",
    schedule_interval="0 0 * * *",
    start_date=days_ago(1),
    catchup=False,
) as dag:

    # Étape 1 : Détection de dérive
    drift_monitoring_task = PythonOperator(
        task_id="run_drift_monitoring",
        python_callable=run_drift_monitoring,
    )

    # Étape 2 : Comparaison des modèles
    model_comparison_task = PythonOperator(
        task_id="run_model_comparison",
        python_callable=run_model_comparison,
    )

    # Étape 3 : Vérification et alerte
    check_drift_task = PythonOperator(
        task_id="check_drift_and_alert",
        python_callable=check_drift_and_alert,
    )

    # Étape 4 : Envoi d’un email en cas de dérive
    email_alert_task = EmailOperator(
        task_id="send_email_alert",
        to="team@example.com",
        subject="Alerte : Dérive détectée dans les données !",
        html_content="Des dérives ont été détectées dans les données de production. Veuillez vérifier le rapport.",
    )

    # Orchestration des tâches
    drift_monitoring_task >> check_drift_task >> [model_comparison_task, email_alert_task]
