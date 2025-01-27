import streamlit as st

st.set_page_config(page_title="Meteo_group_app", page_icon=":sunny:",
                   layout="wide")

users = {"admin":{"username":"admin","password":"admin", "role":"admin"},
         "user":{"username":"user","password":"user", "role":"user"}}

def creds_entered():
    #Normally this function will check with the API
    #Implementing the logic here for now
    user = st.session_state["user"]
    passsword = st.session_state["password"]

    #All the logic to be changed when API is ready
    if user in users:
        if passsword == users[user]["password"]:
            st.session_state["role"] = users[user]["role"]
            st.session_state["auth"] = True #Here normally it will check with the API
        else:
            st.warning("Incorrect password")
    else:
        st.session_state["auth"] = False
        if not st.session_state["user"]:
            st.warning("Please enter your username")
        else:
            st.warning("User not found")

def user_form():
    _, center, __ = st.columns([1, 1, 1])
    with center:
        st.text_input(label="User", key="user")
        st.text_input(label="Password", key="password", type="password")
        st.button(label="Login", on_click=creds_entered)

def login():
    if "auth" not in st.session_state:
        user_form()
        return None
    else:
        if st.session_state["auth"]:
            st.success("Access granted", icon="✅")
            return st.session_state["role"]
        else:
            user_form()
            return None
        
def logout():
    st.session_state["auth"] = False

role = login()
if role:
    col1, col2 = st.columns([10, 1])
    with col2:
        st.write(f"**User**: {st.session_state['user']}")
        st.write(f"**Role**: {st.session_state['role']}")
        st.button(label="Logout", on_click=logout) 
    
    st.title("**Prévisions météo en Australie**")
    
    user_only = (role == "user")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("User tools")
        st.button(label="Check API", on_click=print, args=["It will check the API"])
        st.button(label="Predict", on_click=print, args=["It will predict the weather"])
        st.button(label="Predict proba", on_click=print, args=["It will predict the probability of rain"])
    with col2:
        st.subheader("Admin tools")
        st.page_link("http://localhost:8080", label = "Airflow", disabled = user_only)
        st.page_link("http://localhost:8100", label = "MLFlow", disabled = user_only)
        st.page_link("http://localhost:8000/docs", label = "API", disabled = user_only)
        st.page_link("http://localhost:3000", label = "Grafana", disabled = user_only)
        st.page_link("http://localhost:9090", label = "Prometheus", disabled = user_only)
        st.button(label="Start ingestion", on_click=print, args=["It will lauch the ingestion DAG"], disabled = user_only)
        st.button(label="Start training", on_click=print, args=["It will lauch the training DAG"], disabled = user_only)


