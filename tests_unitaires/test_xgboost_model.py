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
    # Charger la configuration du modèle
    model_config = config["model"]["xgboost"]
    
    # Créer et entraîner le modèle XGBoost
    model = xgb.XGBClassifier(
        n_estimators=model_config["n_estimators"],
        max_depth=model_config["max_depth"]
    )
    
    model.fit(X_train, y_train)

    # Prédictions sur le jeu de test
    y_pred = model.predict(X_test)

    # Calculer les métriques
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    # Sauvegarder les résultats
    metrics = {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1
    }

    # Sauvegarder les métriques dans un fichier JSON
    with open(config["output"]["metrics_path"], "w") as f:
        json.dump(metrics, f)

    # Enregistrer le modèle avec MLflow
    mlflow.start_run()
    mlflow.log_params(model.get_params())
    mlflow.log_metrics(metrics)
    mlflow.xgboost.log_model(model, "model")
    mlflow.end_run()

    # Sauvegarder le modèle localement à l'emplacement attendu par DVC
    model_dir = 'model'
    os.makedirs(model_dir, exist_ok=True)  # Créer le répertoire si nécessaire
    model.save_model(os.path.join(model_dir, 'xgboost_model.json'))  # Sauvegarder à l'emplacement exact attendu par DVC

    print("Modèle entraîné et évalué. Métriques enregistrées.")

