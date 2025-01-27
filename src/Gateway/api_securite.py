from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List
from jose import JWTError, jwt
import requests

# Clé secrète et algorithme pour JWT
SECRET_KEY = "96a0c910f342e9772c403c7db9de6a21036d12bb51cc3de2ffabdf143419eeb3"
ALGORITHM = "HS256"

# Base de données simulée
users_db = {
    "user": {
        "username": "user",
        "roles": ["user"],
        "permissions": ["predict"]
    },
    "admin": {
        "username": "admin",
        "roles": ["admin"],
        "permissions": ["predict", "train"]
    }
}

# Configuration FastAPI
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8000/login")

# Modèle pour les utilisateurs
class User(BaseModel):
    username: str
    roles: List[str]
    permissions: List[str]

# Fonction pour générer un token JWT
def create_token(username: str):
    user = users_db.get(username)
    if not user:
        raise HTTPException(status_code=401, detail="Utilisateur non trouvé")
    payload = {
        "username": username,
        "roles": user["roles"],
        "permissions": user["permissions"]
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

# Fonction pour décoder et vérifier un token JWT
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")

# Endpoint pour la connexion (authentification)
@app.post("/login")
def login(username: str):
    if username not in users_db:
        raise HTTPException(status_code=401, detail="Nom d'utilisateur incorrect")
    token = create_token(username)
    return {"access_token": token}

# Endpoint pour prédiction (accessible à tous les utilisateurs)
@app.get("/predict")
def predict(token: str = Depends(oauth2_scheme)):
    user = decode_token(token)
    if "predict" not in user["permissions"]:
        raise HTTPException(status_code=403, detail="Permission refusée")
    
    # Appel au microservice prédiction
    response = requests.post("http://train_service:8002/train", headers={"Authorization": f"Bearer {token}"})
    return response.json()

# Endpoint pour entraînement (accessible uniquement aux administrateurs)
@app.post("/train")
def train(token: str = Depends(oauth2_scheme)):
    user = decode_token(token)
    if "train" not in user["permissions"]:
        raise HTTPException(status_code=403, detail="Permission refusée")
    
    # Appel au microservice entraînement
    response = requests.get("http://api_prediction:8000/predict", headers={"Authorization": f"Bearer {token}"})
    
    return response.json()

