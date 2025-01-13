import pandas as pd
import xgboost as xgb
from xgboost import XGBClassifier
import yaml
import mlflow
import mlflow.xgboost
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
import os
import json


def load_config(yaml_path):
    """
    Charger la configuration depuis un fichier YAML.
    """
    with open(yaml_path, "r") as file:
        return yaml.safe_load(file)


def validate_data(X, y):
    """
    Vérifie qu'il n'y a pas de NaN ou de valeurs inattendues dans les données.
    """
    if X.isnull().sum().sum() > 0:
        raise ValueError("Des NaN sont présents dans les caractéristiques (X).")
    if y.isnull().sum() > 0:
        raise ValueError("Des NaN sont présents dans la cible (y).")
    print(f"Données valides : {len(X)} lignes et {len(y)} cibles.")


def train_and_evaluate(X_train, y_train, X_test, y_test, config):
    """
    Entraîner et évaluer un modèle XGBoost avec suivi via MLflow.
    """
    # Configurez MLflow
    mlflow.set_tracking_uri(config["mlflow"]["tracking_uri"])
    mlflow.set_experiment(config["mlflow"]["experiment_name"])

    with mlflow.start_run():
        # Définir les paramètres XGBoost
        params = config["model"]["xgboost"]
        model = xgb.XGBClassifier(**params)
        model.fit(X_train, y_train)

        # Prédictions
        y_pred = model.predict(X_test)

        # Calculer les métriques
        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred, zero_division=0),
            "recall": recall_score(y_test, y_pred, zero_division=0),
            "f1_score": f1_score(y_test, y_pred, zero_division=0),
        }

        # Enregistrer les métriques dans MLflow et un fichier
        mlflow.log_params(params)
        mlflow.log_metrics(metrics)

        metrics_path = config["output"]["metrics_path"]
        os.makedirs(os.path.dirname(metrics_path), exist_ok=True)
        with open(metrics_path, "w") as f:
            json.dump(metrics, f)

        # Sauvegarder le modèle
        model_path = config["output"]["model_path"]
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        model.save_model(model_path)

        # Enregistrer le modèle dans MLflow avec un exemple d'entrée
        input_example = X_test.iloc[0:1]
        mlflow.xgboost.log_model(model, "xgboost_model", input_example=input_example)

        print(f"Metrics logged in MLflow: {metrics}")


if __name__ == "__main__":
    # Charger la configuration
    config_path = "config/config.yaml"
    config = load_config(config_path)

    # Charger les données traitées
    X_train = pd.read_csv(config["data"]["processed_dir"] + "X_train.csv")
    X_test = pd.read_csv(config["data"]["processed_dir"] + "X_test.csv")
    y_train = pd.read_csv(config["data"]["processed_dir"] + "y_train.csv").squeeze()
    y_test = pd.read_csv(config["data"]["processed_dir"] + "y_test.csv").squeeze()

    # Valider les données
    validate_data(X_train, y_train)
    validate_data(X_test, y_test)

    # Entraîner et évaluer le modèle
    train_and_evaluate(X_train, y_train, X_test, y_test, config)