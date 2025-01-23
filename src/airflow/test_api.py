import requests
from requests.auth import HTTPBasicAuth

url = "http://localhost:8080/api/v1/dags/Ingestion/dagRuns"

response = requests.post(url, json={}, auth=HTTPBasicAuth('airflow', 'airflow'))

if response.status_code == 200:
    print("DAG triggered successfully.")
else:
    print("Error:", response.text)
