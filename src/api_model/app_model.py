from fastapi import FastAPI, HTTPException
import mlflow
import pandas as pd

from input_classes import InputData, ModelData

api = FastAPI(title="Model API")
mlflow.set_tracking_uri("http://meteo_group-mlflow-1:8100")

print("Loading model...")
model = mlflow.xgboost.load_model("models:/model@model_last", dst_path="model/")

@api.get('/check')
def verify_status():
    """Check that prediction API is online."""
    return {"message": "API is online."}

@api.post('/predict')
async def predict(input_data: InputData):
    global model
    try:
        X = pd.DataFrame.from_dict([input_data.dict()])
        prediction = model.predict(X)

        return {"prediction": prediction.tolist()}
    except HTTPException:
        raise HTTPException(status_code=400, detail="Invalid input data.")

@api.post('/predict_proba')
async def predict_proba(input_data: InputData):
    global model
    try:
        X = pd.DataFrame.from_dict([input_data.dict()])
        prediction = model.predict_proba(X)
        return {"prediction": prediction[:,1].tolist()}
    except HTTPException:
        raise HTTPException(status_code=400, detail="Invalid input data.")

@api.post('/reload')
async def reload_model(model_data: ModelData):
    global model

    if model_data.version and model_data.alias:
        raise HTTPException(status_code=400, detail="Only one of version or alias can be provided.")

    if not model_data.version and not model_data.alias:
        print("No version or alias provided. Using last version.")
        model_data.alias = "model_last"

    try:
        if model_data.alias:
            model = mlflow.xgboost.load_model(f"models:/{model_data.model_name}@{model_data.alias}",
                                             dst_path="model")
        else:
            model = mlflow.xgboost.load_model(f"models:/{model_data.model_name}/{model_data.version}",
                                             dst_path="model")
        return {"message": "Model : '{model_data}' reloaded."}
    except mlflow.exceptions.RestException:
        raise HTTPException(status_code=404, detail=f"Model: '{model_data}' not found.")