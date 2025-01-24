import docker
import requests

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