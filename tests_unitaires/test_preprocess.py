import pytest
import pandas as pd
import numpy as np
# from script import (
    # get_libelle_graph_temp,
    # graph_hisplot,
    # graph_boxplot,
    # preprocess_wind_data,
    # analyze_temperature,
# )


@pytest.fixture
def sample_dataframe():
    """
    Fixture pour créer un DataFrame d'exemple pour les tests.
    """
    return pd.DataFrame({
        "Location": ["Canberra", "Canberra", "Ballarat"],
        "Date": ["2021-01-01", "2021-01-02", "2021-01-03"],
        "Tempreal": [25.0, 27.5, 24.0],
        "Tempmean": [24.5, 26.0, 23.0],
        "WindGustDir": ["N", None, "S"],
        "WindDir3pm": ["E", "W", "S"],
        "WindGustSpeed": [40, None, 30],
        "WindSpeed9am": [10, 15, 20],
        "WindSpeed3pm": [25, 20, 15],
    })


def test_get_libelle_graph_temp():
    """
    Teste la fonction get_libelle_graph_temp.
    """
    result = get_libelle_graph_temp("Canberra")
    expected = "Températures prélevées à 9h00 dans la station Canberra du 01/11/2011 au 31/01/2012, climat associé est Tempéré"
    assert result == expected


def test_graph_hisplot(sample_dataframe):
    """
    Teste si la fonction graph_hisplot retourne une figure matplotlib.
    """
    list_col = ["Tempreal", "Tempmean"]
    list_label = ["Température réelle", "Température moyenne"]
    fig = graph_hisplot(sample_dataframe, list_col, list_label)
    assert fig is not None  # Vérifie que la figure est créée
    assert hasattr(fig, "axes")  # Vérifie que la figure contient des axes


def test_graph_boxplot(sample_dataframe):
    """
    Teste si la fonction graph_boxplot retourne une figure matplotlib.
    """
    list_col = ["Tempreal", "Tempmean"]
    list_label = ["Température réelle", "Température moyenne"]
    fig = graph_boxplot(sample_dataframe, list_col, list_label)
    assert fig is not None
    assert hasattr(fig, "axes")


def test_preprocess_wind_data(sample_dataframe):
    """
    Teste la fonction preprocess_wind_data.
    """
    processed_df = preprocess_wind_data(sample_dataframe)
    assert "WindDir9am" not in processed_df.columns  # Vérifie la suppression des colonnes
    assert "WindSpeed9am" not in processed_df.columns
    assert "WindSpeed3pm" not in processed_df.columns
    assert not processed_df["WindGustDir"].isnull().any()  # Vérifie le remplissage des valeurs NA
    assert not processed_df["WindGustSpeed"].isnull().any()


def test_analyze_temperature(sample_dataframe):
    """
    Teste si la fonction analyze_temperature retourne une figure plotly.
    """
    fig = analyze_temperature(sample_dataframe, "Canberra")
    assert fig is not None
    assert isinstance(fig, go.Figure)  # Vérifie que le résultat est une figure Plotly
