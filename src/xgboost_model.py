import yaml
import xgboost as xgb
import mlflow
import mlflow.xgboost
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import json
import os


def load_config(yaml_path):
    """
    Charger la configuration depuis un fichier YAML.
    """
    if not os.path.exists(yaml_path):
        raise FileNotFoundError(f"Le fichier de configuration {yaml_path} n'existe pas.")
    
    with open(yaml_path, "r") as file:
        return yaml.safe_load(file)


def validate_data(X, y):
    """
    Valider les données avant l'entraînement du modèle.
    """
    assert X is not None and y is not None, "Les données d'entrée ou la cible sont manquantes."
    assert X.shape[0] == y.shape[0], "Le nombre de lignes de X et y ne correspond pas."


def train_and_evaluate(X_train, y_train, X_test, y_test, config):
    """
    Entraîner le modèle XGBoost et évaluer ses performances.
    """
    model_config = config["model"]["xgboost"]

    # Configurer MLflow
    mlflow.set_tracking_uri(config["mlflow"]["tracking_uri"])
    mlflow.set_experiment(config["mlflow"]["experiment_name"])

    # Créer une nouvelle expérience si elle n'existe pas déjà
    experiment_name = config["mlflow"]["experiment_name"]
    experiment = mlflow.get_experiment_by_name(experiment_name)

    if experiment is None:
        print(f"Création de l'expérience : {experiment_name}")
        mlflow.create_experiment(experiment_name)

    # Commencer une nouvelle exécution
    with mlflow.start_run():
        # Définir et entraîner le modèle
        params = model_config
        model = xgb.XGBClassifier(**params)
        model.fit(X_train, y_train)

        # Prédictions
        y_pred = model.predict(X_test)

        # Calcul des métriques
        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred, zero_division=0),
            "recall": recall_score(y_test, y_pred, zero_division=0),
            "f1_score": f1_score(y_test, y_pred, zero_division=0),
        }

        # Sauvegarder les métriques
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

        # Enregistrer le modèle dans MLflow
        input_example = X_test.iloc[0:1]  # Exemple d'entrée
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

