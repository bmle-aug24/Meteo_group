import streamlit as st
import requests

st.set_page_config(page_title="Meteo_group_app", page_icon=":sunny:",
                   layout="wide")

# Configuration de l'URL de l'API Gateway
API_GATEWAY_URL = "http://gateway:8001"
INPUT_SHAPE = {
  "Date": 0,
  "Location": 0,
  "MinTemp": 0,
  "MaxTemp": 0,
  "Rainfall": 0,
  "Evaporation": 0,
  "Sunshine": 0,
  "WindGustDir": 0,
  "WindGustSpeed": 0,
  "WindDir9am": 0,
  "WindDir3pm": 0,
  "WindSpeed9am": 0,
  "WindSpeed3pm": 0,
  "Humidity9am": 0,
  "Humidity3pm": 0,
  "Pressure9am": 0,
  "Pressure3pm": 0,
  "Cloud9am": 0,
  "Cloud3pm": 0,
  "Temp9am": 0,
  "Temp3pm": 0,
  "RainToday":0}

# Variables de session pour stocker l'état de l'utilisateur
if "is_authenticated" not in st.session_state:
    st.session_state["is_authenticated"] = False
    st.session_state["username"] = None
    st.session_state["access_token"] = None
    st.session_state["permissions"] = []

# Fonction pour authentifier l'utilisateur
def authenticate_user(username, password):
    response = requests.post(f"{API_GATEWAY_URL}/login", json={"username": username, "password": password})
    if response.status_code == 200:
        token = response.json()["access_token"]
        return token
    else:
        st.error("Nom d'utilisateur incorrect.")
        return None

# Fonction pour vérifier les permissions
def get_permissions_from_token(token):
    from jose import jwt
    SECRET_KEY = "96a0c910f342e9772c403c7db9de6a21036d12bb51cc3de2ffabdf143419eeb3"
    ALGORITHM = "HS256"
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("permissions", [])
    except Exception as e:
        st.error("Erreur lors du décodage du token.")
        return []

# Fonction pour appeler l'API de prédiction
def call_prediction_api(token, input_data, pred_type='predict'):
    print(pred_type)
    response = requests.post(f"{API_GATEWAY_URL}/predict", 
                             headers={"Authorization": f"Bearer {token}"},
                             json={**input_data, 'pred_type':pred_type})
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Erreur lors de l'appel à l'API de prédiction.")
        st.error(response.status_code)
        st.error(response.json())
        return None

# Fonction pour appeler l'API d'ingestion
def call_ingestion_api(token):
    response = requests.post(f"{API_GATEWAY_URL}/ingest", headers={"Authorization": f"Bearer {token}"})
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Fonction pour appeler l'API d'entraînement
def call_training_api(token):
    response = requests.post(f"{API_GATEWAY_URL}/train", headers={"Authorization": f"Bearer {token}"})
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Erreur lors de l'appel à l'API d'entraînement.")
        return None

# Interface utilisateur Streamlit
st.title("Méteo en Australie")
st.sidebar.title("Authentification")

# Formulaire de connexion
if not st.session_state["is_authenticated"]:
    with st.sidebar.form("login_form"):
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        submitted = st.form_submit_button("Se connecter")

    if submitted:
        token = authenticate_user(username, password)
        if token:
            st.session_state["is_authenticated"] = True
            st.session_state["username"] = username
            st.session_state["access_token"] = token
            st.session_state["permissions"] = get_permissions_from_token(token)
            st.sidebar.success(f"Bienvenue, {username} !", icon="✅")
        else:
            st.sidebar.error("Échec de la connexion.")
else:
    st.sidebar.success(f"Connecté en tant que {st.session_state['username']}", icon="✅")
    if st.sidebar.button("Se déconnecter"):
        st.session_state["is_authenticated"] = False
        st.session_state["username"] = None
        st.session_state["access_token"] = None
        st.session_state["permissions"] = []

# Section principale
if st.session_state["is_authenticated"]:
    colU, colA = st.columns([2,1])
    with colU:
        if "predict" in st.session_state["permissions"]:
            st.subheader("Outils Utilisateur")
            input_data = {}
            pred_type = st.radio("Sélectionner le type de prédiction souhaitée", options=["Absolu", "Probabilité"], horizontal=True)
            pred_endpoint = "predict_proba" if pred_type == 'Probabilité' else "predict"
            for key in INPUT_SHAPE:
                col1, col2 = st.columns([1,3], vertical_alignment='center')
                with col1:
                    st.markdown(key)
                with col2:
                    input_data[key] = st.text_input(label=key, value=0, label_visibility='hidden')
            if st.button("Lancer la prédiction"):
                result = call_prediction_api(st.session_state["access_token"], input_data, pred_endpoint)
                st.write("Résultat de la prédiction :", result["prediction"][0])
    with colA:
        if "train" in st.session_state["permissions"]:
            st.subheader("Outils Administrateur")
            col1,col2 = st.columns(2)
            with col1:
                if st.button("Lancer Ingestion"):
                    result = call_ingestion_api(st.session_state["access_token"])
                    with col2:
                        st.write(result['message'])
            col1,col2 = st.columns(2)
            with col1:
                if st.button("Lancer l'entraînement"):
                    result = call_training_api(st.session_state["access_token"])
                    with col2:
                        st.write("Résultat de l'entraînement :", result["message"])
            st.page_link("http://localhost:8080", label = "Airflow")
            st.page_link("http://localhost:8100", label = "MLFlow")
else:
    st.warning("Veuillez vous connecter pour accéder aux fonctionnalités.")

