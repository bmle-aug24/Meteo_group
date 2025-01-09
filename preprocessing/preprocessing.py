##############################################################################################
##
##        Import des librairies
##
##############################################################################################
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def insert_image_placeholder(nom_image):
    """
    Placeholder pour insérer une image, à personnaliser si nécessaire
    """
    return f"Image insérée : {nom_image}"


def graph_hisplot(df, list_col, list_label):
    """
    Tracé des histogrammes de distribution d'une liste de variables
    """
    i = 1
    fig = plt.figure(figsize=(20, 10))

    for col, label in zip(list_col, list_label):
        plt.subplot(2, 4, i)
        i += 1
        sns.histplot(x=df[col], kde=True, color='g')
        plt.title(label)
        plt.yticks([])
        plt.ylabel("Densité")
        plt.xlabel("")
    return fig


def graph_boxplot(df, list_col, list_label):
    """
    Tracé des boîtes à moustaches d'une liste de variables
    """
    i = 1
    fig = plt.figure(figsize=(20, 10))

    for col, label in zip(list_col, list_label):
        plt.subplot(2, 4, i)
        i += 1
        sns.boxplot(x=df[col], color='g')
        plt.title(label)
        plt.ylabel("")
        plt.xlabel("")
    return fig


def get_libelle_graph_temp(option):
    """
    Création dynamique du libellé du graphe présentant la température et sa moyenne associée
    """
    ch = "Températures prélevées à {} dans la station {} du {} au {}, climat associé est {}"

    options_mapping = {
        "BadgerysCreek": ("15h00", "01/01/2011", "30/03/2011", "Tempéré"),
        "Canberra": ("9h00", "01/11/2011", "31/01/2012", "Tempéré"),
        "MountGinini": ("15h00", "01/01/2009", "28/02/2009", "Subtropical"),
        "Ballarat": ("9h00", "01/05/2013", "31/07/2013", "Tempéré"),
        "PearceRAAF": ("15h00", "01/09/2014", "30/11/2014", "Tempéré"),
    }

    heure, datedeb, datefin, climat = options_mapping.get(option, ("", "", "", ""))
    return ch.format(heure, option, datedeb, datefin, climat)


def preprocess_data(df_hist, df_villes):
    """
    Fonction principale pour effectuer le préprocessing des données.
    - Lecture des données
    - Ajout des données complémentaires
    """
    df_temperature = pd.read_csv("data/df_exemple_temp.csv")
    df_dir_vent = pd.read_csv("data/df_stat_vent.csv")

    return df_temperature, df_dir_vent


def analyze_temperature(df_temperature, location):
    """
    Analyse des températures pour une localisation donnée
    """
    df_temp = df_temperature.loc[df_temperature["Location"] == location]

    fig = go.Figure(go.Scatter(
        x=df_temp['Date'], y=df_temp['Tempreal'], name="Température réelle"))

    fig = fig.add_trace(go.Scatter(
        x=df_temp['Date'], y=df_temp['Tempmean'], name="Température moyenne"))

    fig.update_layout(
        title=get_libelle_graph_temp(location),
        xaxis_tickformat='%d %B %Y'
    )
    return fig


def analyze_wind(df_dir_vent):
    """
    Analyse des directions des vents
    """
    fig = make_subplots(rows=1, cols=3, specs=[[{'type': 'polar'}] * 3])

    fig.add_trace(go.Scatterpolar(
        name="Direction de la plus grosse rafale de vent",
        r=df_dir_vent["WindGustDir"],
        theta=df_dir_vent["Direction"]), 1, 1)

    fig.add_trace(go.Scatterpolar(
        name="Direction du vent à 9h00",
        r=df_dir_vent["WindDir9am"],
        theta=df_dir_vent["Direction"]), 1, 2)

    fig.add_trace(go.Scatterpolar(
        name="Direction du vent à 15h00",
        r=df_dir_vent["WindDir3pm"],
        theta=df_dir_vent["Direction"]), 1, 3)

    fig.update_traces(fill='toself')

    fig.update_layout(
        polar1=dict(
            radialaxis_angle=90,
            angularaxis=dict(direction="clockwise")
        ),
        polar2=dict(
            radialaxis_angle=90,
            angularaxis=dict(direction="clockwise")
        ),
        polar3=dict(
            radialaxis_angle=90,
            angularaxis=dict(direction="clockwise")
        )
    )
    return fig


def preprocess_wind_data(df_wind):
    """
    Prétraitement des données de vent
    """
    df_wind['WindGustDir'] = df_wind['WindGustDir'].fillna(df_wind['WindDir3pm'])
    df_wind['WindGustSpeed'] = df_wind['WindGustSpeed'].fillna(
        df_wind[['WindSpeed9am', 'WindSpeed3pm']].max(axis=1))
    df_wind = df_wind.drop(columns=['WindDir9am', 'WindSpeed9am', 'WindSpeed3pm'])
    return df_wind
