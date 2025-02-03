import docker
import requests

def start_existing_container(container_name:str, command:str=None):
    client = docker.from_env()
    container = client.containers.get(container_name)
    container.start()
    if command: 
        container.exec_run("export RUN_COMMAND=false && sh /app/script.sh")
        container.exec_run(command)
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

def launch_dvc_container(files: list):
    command = ""
    for file in files:
        command += f"dvc add {file} && "
    command += "dvc push && git push"
    
    client = docker.from_env()
    container = client.containers.run(
        image="python:3.9-slim",
        command=command,
        detach=True,
        remove=True,
        volumes={"./": {'bind':'/app/', 'mode':'rw'}}
    )