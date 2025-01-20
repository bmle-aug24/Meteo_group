from fastapi import FastAPI#, Header, HTTPException
import mlflow

api = FastAPI(title="MODEL API")
print("Loading model...")

client = mlflow.tracking.MlflowClient()
"""
registered_models = client.get_registered_model
for model in registered_models:
    print(model.name)

mlflow.set_tracking_uri("http://localhost:8100")
print(f"Tracking URI: {mlflow.get_tracking_uri()}")
model_details = client.get_registered_model("Model 1")
print(model_details)
"""
model = mlflow.pyfunc.load_model("models:/'Model 1'@model_last")

@api.get('/check')
def verify_status():
    """Check that prediction API is online."""
    return {"message": "API is online."}

@api.post('/predict')
def predict():
    prediction = None
    return {"prediction": prediction}

@api.post('/reload')
def reload_model(path_to_model: str):
    model = mlflow.xgboost.load_model(path_to_model)
    return {"message": "Model reloaded."}