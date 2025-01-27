import streamlit as st
import requests

# Configuration de l'URL de l'API Gateway
API_GATEWAY_URL = "http://localhost:8000"

# Variables de session pour stocker l'état de l'utilisateur
if "is_authenticated" not in st.session_state:
    st.session_state["is_authenticated"] = False
    st.session_state["username"] = None
    st.session_state["access_token"] = None
    st.session_state["permissions"] = []

# Fonction pour authentifier l'utilisateur
def authenticate_user(username, password):
    response = requests.post(f"{API_GATEWAY_URL}/login", json={"username": username})
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
def call_prediction_api(token):
    response = requests.get(f"{API_GATEWAY_URL}/predict", headers={"Authorization": f"Bearer {token}"})
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Erreur lors de l'appel à l'API de prédiction.")
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
st.title("Mon Application Streamlit")
st.sidebar.title("Authentification")

# Formulaire de connexion
if not st.session_state["is_authenticated"]:
    with st.sidebar.form("login_form"):
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")  # Simulé ici, non utilisé dans l'API actuelle
        submitted = st.form_submit_button("Se connecter")

    if submitted:
        token = authenticate_user(username, password)
        if token:
            st.session_state["is_authenticated"] = True
            st.session_state["username"] = username
            st.session_state["access_token"] = token
            st.session_state["permissions"] = get_permissions_from_token(token)
            st.sidebar.success(f"Bienvenue, {username} !")
        else:
            st.sidebar.error("Échec de la connexion.")
else:
    st.sidebar.success(f"Connecté en tant que {st.session_state['username']}")
    if st.sidebar.button("Se déconnecter"):
        st.session_state["is_authenticated"] = False
        st.session_state["username"] = None
        st.session_state["access_token"] = None
        st.session_state["permissions"] = []

# Section principale
if st.session_state["is_authenticated"]:
    st.header("Actions disponibles")

    # Affichage des permissions
    st.write("Vos permissions :", st.session_state["permissions"])

    # Fonctionnalité de prédiction
    if "predict" in st.session_state["permissions"]:
        st.subheader("API de prédiction")
        input_data = st.text_input("Entrez les données pour la prédiction (exemple : 1,2,3)")
        if st.button("Lancer la prédiction"):
            if input_data:
                input_list = [float(x) for x in input_data.split(",")]
                result = call_prediction_api(st.session_state["access_token"])
                st.write("Résultat de la prédiction :", result)
            else:
                st.warning("Veuillez entrer des données pour la prédiction.")

    # Fonctionnalité d'entraînement
    if "train" in st.session_state["permissions"]:
        st.subheader("API d'entraînement")
        if st.button("Lancer l'entraînement"):
            result = call_training_api(st.session_state["access_token"])
            st.write("Résultat de l'entraînement :", result)
else:
    st.warning("Veuillez vous connecter pour accéder aux fonctionnalités.")

