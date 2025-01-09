import pytest
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
import xgboost as xgb
# from preprocess import load_data, prepare_data, train_xgboost

# Mock data pour les tests
@pytest.fixture
def mock_data():
    data = {
        "feature1": [1.0, 2.0, 3.0, 4.0, 5.0],
        "feature2": [0.5, 1.5, 2.5, 3.5, 4.5],
        "category": ["A", "B", "A", "B", "A"],
        "RainTomorrow": [0, 1, 0, 1, 0],
    }
    dataset = pd.DataFrame(data)
    return dataset

@pytest.fixture
def prepared_data(mock_data):
    # Mock le chargement des données
    X = mock_data.drop(columns=["RainTomorrow"])
    y = mock_data["RainTomorrow"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Identification des colonnes numériques et catégorielles
    num_features = X_train.select_dtypes(include=["float64", "int64"]).columns
    cat_features = X_train.select_dtypes(include=["object"]).columns

    # Préprocesseur pour normalisation et encodage
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), num_features),
            ("cat", OneHotEncoder(drop="first"), cat_features),
        ]
    )

    return X_train, X_test, y_train, y_test, preprocessor

# Test : Chargement des données
def test_load_data(mock_data, monkeypatch):
    # Mock de la fonction pandas.read_csv
    def mock_read_csv(*args, **kwargs):
        return mock_data

    monkeypatch.setattr(pd, "read_csv", mock_read_csv)

    X_train, X_test, y_train, y_test = load_data()
    assert X_train is not None
    assert y_train is not None
    assert len(X_train) > 0
    assert len(y_train) > 0

# Test : Préparation des données
def test_prepare_data(prepared_data):
    X_train, X_test, y_train, y_test, preprocessor = prepared_data

    assert X_train.shape[0] > 0
    assert X_test.shape[0] > 0
    assert y_train.shape[0] > 0
    assert y_test.shape[0] > 0
    assert isinstance(preprocessor, ColumnTransformer)

# Test : Entraînement avec XGBoost
def test_train_xgboost(prepared_data):
    X_train, X_test, y_train, y_test, preprocessor = prepared_data

    # Entraîner le modèle
    results = train_xgboost(X_train, X_test, y_train, y_test, preprocessor)

    # Vérifications sur les résultats
    assert "Accuracy" in results
    assert results["Accuracy"] > 0
    assert "Recall (1)" in results
    assert "F1 Score" in results
    assert "Precision (1)" in results
