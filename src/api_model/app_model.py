from fastapi import FastAPI, HTTPException, Request
import mlflow
import pandas as pd
from input_classes import InputData, ModelData
from datetime import datetime
import os
import time

# 1) Import du module pour Prometheus
from prometheus_fastapi_instrumentator import Instrumentator

# 2) Création de l'API FastAPI
api = FastAPI(title="Model API")

# 3) Initialisation de Prometheus Instrumentator
instrumentator = Instrumentator().instrument(api)

# 4) Configuration de MLflow
mlflow.set_tracking_uri("http://mlflow:8100")

print("Loading model...")
model = mlflow.xgboost.load_model("models:/model@model_last", dst_path="mlflow/")

# 5) Endpoint pour vérifier si l'API est en ligne
@api.get('/check')
def verify_status():
    return {"message": "API is online."}

# 6) Endpoint pour la prédiction avec monitoring
@api.post('/predict')
async def predict(input_data: InputData, request: Request):
    global model
    start_time = time.time()  # Début de la mesure du temps de réponse
    try:
        # 1) Convertir l'entrée en DataFrame
        X = pd.DataFrame.from_dict([input_data.dict()])
        
        # 2) Faire la prédiction
        prediction = model.predict(X)
        
        # 3) Log des requêtes en production (CSV)
        X['prediction'] = prediction
        X['timestamp'] = datetime.now().isoformat()

        # 4) Sauvegarde des logs de requêtes
        log_file = "data/production_logs/requests_log.csv"
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        write_header = not os.path.exists(log_file)
        X.to_csv(log_file, mode='a', header=write_header, index=False)

        # 5) Log Prometheus : temps de réponse
        duration = time.time() - start_time
        instrumentator.expose(api)
        
        return {"prediction": prediction.tolist()}
        
    except HTTPException:
        raise HTTPException(status_code=400, detail="Invalid input data.")

# 7) Endpoint pour la probabilité de prédiction
@api.post('/predict_proba')
async def predict_proba(input_data: InputData):
    global model
    try:
        X = pd.DataFrame.from_dict([input_data.dict()])
        prediction = model.predict_proba(X)
        return {"prediction": prediction[:,1].tolist()}
    except HTTPException:
        raise HTTPException(status_code=400, detail="Invalid input data.")

# 8) Endpoint pour recharger le modèle
@api.post('/reload')
async def reload_model(model_data: ModelData):
    global model

    if model_data.version and model_data.alias:
        raise HTTPException(status_code=400, detail="Only one of version or alias can be provided.")

    if not model_data.version and not model_data.alias:
        print("No version or alias provided. Using last version.")
        model_data.alias = "model_last"
    
    print("Loading model...")
    try:
        if model_data.alias:
            model = mlflow.xgboost.load_model(f"models:/{model_data.model_name}@{model_data.alias}",
                                             dst_path="mlflow/")
        else:
            model = mlflow.xgboost.load_model(f"models:/{model_data.model_name}/{model_data.version}",
                                             dst_path="mlflow/")
        return {"message": f"Model : '{model_data}' reloaded."}
    except mlflow.exceptions.RestException:
        raise HTTPException(status_code=404, detail=f"Model: '{model_data}' not found.")
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app_model:api", host="0.0.0.0", port=8000, reload=True)
