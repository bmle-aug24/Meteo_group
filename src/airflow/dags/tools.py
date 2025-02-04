import docker
import requests
from datetime import datetime
import subprocess as sp

def start_existing_container(container_name:str):
    client = docker.from_env()
    container = client.containers.get(container_name)
    container.start()      
    container.wait()

def load_model_script(model_name:str="model", alias:str="model_last"):
    url = "http://meteo_group-api_prediction-1:8000/reload"
    data = {"model_name": model_name,
            "alias": alias}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        print(response.text)
    else:
        print("Error:", response.text)

def launch_dvc_push_container(container_name:str, files: list):
    #command = "echo 'command received'"
    command = "apt update && apt install -y git && "
    command += "pip install dvc && "
    command += "cd /app/repo && "
    for file in files:
        command += f"dvc add {file} && git add {file}.dvc && "
    command += "dvc push && "
    command += f"git commit -m 'dvc update {datetime.today().strftime('%Y-%m-%d')}' && "
    command += "git push"
    
    """
    client = docker.from_env()
    container = client.containers.get(container_name)
    container.start()
    #container.exec_run(["/bin/bash", "/app/script.sh", "echo 'Test entry'"], stdout=True, stderr=True)
    container.exec_run(["/bin/bash", "/app/script.sh", command])
    container.wait()
    

    repo_path = "/opt/airflow/repo"
    sp.run(["mkdir", "-p", repo_path], check=True)
    #sp.run(["cd", "/opt/airflow/repo"])
    for file in files:
        sp.run(["dvc", "add", file], check=True,cwd=repo_path)
        sp.run(["git", "add", file+".dvc"], check=True,cwd=repo_path)
    sp.run(["dvc", "push"], check=True,cwd=repo_path)
    sp.run(["git", "commit", "-m", "Update_DVC", datetime.today().strftime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))], check=True,cwd=repo_path)
    sp.run(["git", "push"], check=True,cwd=repo_path)
    """
    repo_path = "/opt/airflow/repo"
    sp.run(["mkdir", "-p", repo_path], check=True)

    client = docker.from_env()
    container = client.containers.run(
        image="python:3.9-slim",
        name="dvc_push",
        command=["/bin/bash", "-c", command],
        detach=True,
        #auto_remove=True,
        mounts={"localhost_volume":  {"bind": "/app/repo", "mode": "rw"}},
        network_mode="bridge"
    )
    container.wait()
