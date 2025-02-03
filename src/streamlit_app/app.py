import streamlit as st
import requests
import base64
import os

# ---------------------
# 1) Configuration de base Streamlit
# ---------------------
st.set_page_config(
    page_title="Meteo_group_app",
    page_icon=":sunny:",
    layout="wide"
)

# ---------------------
# 2) Variables globales & Gateway
# ---------------------
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
    "RainToday": 0
}

# ---------------------
# 3) Gestion de session (authentification)
# ---------------------
if "is_authenticated" not in st.session_state:
    st.session_state["is_authenticated"] = False
    st.session_state["username"] = None
    st.session_state["access_token"] = None
    st.session_state["permissions"] = []

# ---------------------
# 4) Fonctions utilitaires
# ---------------------
def get_image_base64(image_path: str) -> str:
    """
    Encode une image en base64 pour l'afficher directement via HTML/CSS.
    """
    try:
        with open(image_path, "rb") as f:
            data = f.read()
        encoded = base64.b64encode(data).decode()
        # Détecter l'extension
        ext = os.path.splitext(image_path)[1].lower()
        mime = "image/png" if ext == ".png" else "image/jpeg"
        return f"data:{mime};base64,{encoded}"
    except Exception as e:
        st.error(f"⚠️ Erreur lors de l'encodage de l'image: {e}")
        return ""

def set_custom_style():
    """
    Applique le style CSS personnalisé, adapté à un thème 'météo' (jaune/bleu ciel).
    """
    # Exemple : On va chercher un fond local "assets/background.jpg"
    background_path = "assets/background.jpg"
    background_base64 = get_image_base64(background_path)

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&family=Montserrat:wght@600&display=swap');

        /* Le conteneur global de l'app */
        .stApp {{
            font-family: 'Roboto', sans-serif;
            background: 
              linear-gradient(
                120deg, 
                rgba(255, 255, 128, 0.6),  /* jaune pâle transparent */
                rgba(135, 206, 250, 0.6)   /* bleu ciel transparent */
              ),
              url("{background_base64}") no-repeat center center fixed;
            background-size: cover;
        }}

        /* Sidebar style : dégradé vertical jaune -> bleu ciel */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #ffe066, #87cefa);
            color: #000; /* Texte en noir pour contraster */
            border-right: 3px solid #ffd700; /* Bordure dorée */
            padding: 20px;
        }}

        /* Les titres/labels dans la sidebar en plus foncé */
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3, 
        [data-testid="stSidebar"] label {{
            color: #333;
            font-weight: bold;
        }}

        /* Effet hover sur les boutons */
        button:hover {{
            transform: scale(1.03);
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
        }}

        /* Titre principal */
        .title {{
            animation: fadeIn 2s ease-in-out;
            color: #444; /* gris foncé */
            text-align: center;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}

        /* Bloc d'accueil (content-block) */
        .content-block {{
            background-color: rgba(255, 255, 255, 0.8);
            color: #333;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}

        /* Footer - on le met dans un ton bleu doux ou jaune */
        footer {{
            text-align: center;
            margin-top: 50px;
            font-size: 14px;
            color: #333;
            background-color: rgba(255, 255, 255, 0.7);
            padding: 10px;
            border-radius: 10px;
        }}
        footer a {{
            text-decoration: none;
            color: #0066cc;
            margin: 0 5px;
            font-weight: bold;
        }}
        footer a:hover {{
            color: #ff9900;
            text-decoration: underline;
        }}
        footer img {{
            width: 20px;
            vertical-align: middle;
            margin-right: 5px;
        }}

        /* Blocs de résultat (réponse prédiction) */
        .result-block {{
            background-color: rgba(255, 255, 255, 0.7);
            color: #000;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            border: 2px dashed #ccc;
        }}
        .result-success {{
            border: 2px solid #28a745;
        }}
        .result-warning {{
            border: 2px solid #ffc107;
        }}
        .result-error {{
            border: 2px solid #dc3545;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )

def authenticate_user(username, password):
    response = requests.post(
        f"{API_GATEWAY_URL}/login",
        json={"username": username, "password": password}
    )
    if response.status_code == 200:
        token = response.json()["access_token"]
        return token
    else:
        st.error("Nom d'utilisateur ou mot de passe incorrect.")
        return None

def get_permissions_from_token(token):
    """
    Décode le token JWT pour extraire les permissions.
    """
    from jose import jwt
    SECRET_KEY = "96a0c910f342e9772c403c7db9de6a21036d12bb51cc3de2ffabdf143419eeb3"
    ALGORITHM = "HS256"
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("permissions", [])
    except Exception as e:
        st.error("Erreur lors du décodage du token.")
        return []

def call_prediction_api(token, input_data, pred_type='predict'):
    response = requests.post(
        f"{API_GATEWAY_URL}/predict",
        headers={"Authorization": f"Bearer {token}"},
        json={**input_data, 'pred_type': pred_type}
    )
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Erreur lors de l'appel à l'API de prédiction.")
        st.error(response.status_code)
        st.error(response.json())
        return None

def call_ingestion_api(token):
    response = requests.post(
        f"{API_GATEWAY_URL}/ingest",
        headers={"Authorization": f"Bearer {token}"}
    )
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Erreur lors de l'appel à l'API d'ingestion.")
        return None

def call_training_api(token):
    response = requests.post(
        f"{API_GATEWAY_URL}/train",
        headers={"Authorization": f"Bearer {token}"}
    )
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Erreur lors de l'appel à l'API d'entraînement.")
        return None

# ---------------------
# 5) Application Streamlit
# ---------------------

# Appliquer notre style personnalisé (couleurs, fonds, etc.)
set_custom_style()

# Affichage d’un logo local (ex: "assets/logo_meteo.png"), si dispo
logo_path = "assets/logo_meteo.png"
if os.path.exists(logo_path):
    logo_base64 = get_image_base64(logo_path)
    st.markdown(
        f"""
        <div class="title">
            <img src="{logo_base64}" alt="Logo Meteo" style="height: 60px; margin-right: 10px;">
            <h1 style="margin: 0;">Prévision Météo en Australie</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown('<h1 class="title">Prévision Météo en Australie</h1>', unsafe_allow_html=True)

# Barre latérale (authentification)
st.sidebar.title("Authentification")
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

# Partie principale
if st.session_state["is_authenticated"]:
    st.markdown(
        """
        <div class="content-block">
            <h2>Bienvenue dans l’application de prévision météo en Australie !</h2>
            <p>
              Renseignez les différents paramètres pour obtenir une prédiction.<br>
              Selon vos permissions, vous pouvez également lancer l’ingestion et l’entraînement.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    colU, colA = st.columns([2, 1])
    with colU:
        # Outils Utilisateur (prédiction)
        if "predict" in st.session_state["permissions"]:
            st.subheader("Outils Utilisateur")

            pred_type = st.radio(
                "Type de prédiction souhaitée",
                options=["Absolu", "Probabilité"], 
                horizontal=True
            )
            pred_endpoint = "predict_proba" if pred_type == 'Probabilité' else "predict"

            input_data = {}
            for key in INPUT_SHAPE:
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.markdown(f"**{key}**")
                with col2:
                    input_data[key] = st.text_input(label=key, value=0, label_visibility='hidden')

            if st.button("Lancer la prédiction"):
                with st.spinner("Appel à l'API de prédiction..."):
                    result = call_prediction_api(
                        st.session_state["access_token"], 
                        input_data, 
                        pred_endpoint
                    )
                if result:
                    st.markdown(
                        f"""
                        <div class="result-block">
                            <h3>Résultat de la prédiction</h3>
                            <p>
                              <strong>Prévision :</strong> {result["prediction"][0]}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

    with colA:
        # Outils Administrateur (ingestion & entraînement)
        if "train" in st.session_state["permissions"]:
            st.subheader("Outils Administrateur")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Lancer Ingestion"):
                    with st.spinner("Ingestion en cours..."):
                        result = call_ingestion_api(st.session_state["access_token"])
                    with col2:
                        if result:
                            st.write(result['message'])

            col3, col4 = st.columns(2)
            with col3:
                if st.button("Lancer l'entraînement"):
                    with st.spinner("Entraînement en cours..."):
                        result = call_training_api(st.session_state["access_token"])
                    with col4:
                        if result:
                            st.write("**Résultat de l'entraînement**:", result["message"])

            # Liens Airflow & MLflow (exemple)
            st.markdown("---")
            st.markdown("**Liens utiles :**")
            st.markdown("[Airflow (localhost:8080)](http://localhost:8080)")
            st.markdown("[MLFlow (localhost:8100)](http://localhost:8100)")

else:
    st.warning("Veuillez vous connecter pour accéder aux fonctionnalités.")

# Footer
st.markdown(
    """
    <footer>
        &copy; 2025 MLOps Weather Project - Australia  
        Développé par l'équipe Meteo_group  
        <br>
        <a href="https://docs.streamlit.io" target="_blank">
          <img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit" />
          Streamlit
        </a> |
        <a href="https://github.com" target="_blank">
          <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="GitHub" />
          GitHub
        </a>
    </footer>
    """,
    unsafe_allow_html=True
)
