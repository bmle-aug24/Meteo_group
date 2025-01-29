import pandas as pd
from scipy.stats import ks_2samp
import os
import mlflow

# 📌 Définition des chemins des fichiers (Docker)
train_data_path = "/app/data/processed/X_train.csv"
log_data_path = "/app/data/production_logs/requests_log.csv"
output_path = "/app/data/monitoring/drift_report.csv"

# 📌 Vérifier si les fichiers existent
if not os.path.exists(train_data_path):
    raise FileNotFoundError(f"Training data not found at {train_data_path}")

if not os.path.exists(log_data_path):
    raise FileNotFoundError(f"Log data not found at {log_data_path}")

# 📌 Charger les données
X_train = pd.read_csv(train_data_path)
requests_log = pd.read_csv(log_data_path)

# 📌 Aligner les colonnes pour éviter les erreurs
common_columns = list(set(X_train.columns) & set(requests_log.columns))
if not common_columns:
    raise ValueError("Aucune colonne commune entre les données d'entraînement et les logs de production.")

X_train = X_train[common_columns]
requests_log = requests_log[common_columns]

# 📌 Calculer la dérive avec Kolmogorov-Smirnov
drift_results = []
for column in common_columns:
    stat, p_value = ks_2samp(X_train[column].dropna(), requests_log[column].dropna())
    drift_results.append({"feature": column, "statistic": stat, "p_value": p_value})

# 📌 Créer un DataFrame pour le rapport
drift_report = pd.DataFrame(drift_results)

# 📌 Enregistrer le rapport dans un fichier CSV
os.makedirs(os.path.dirname(output_path), exist_ok=True)
drift_report.to_csv(output_path, index=False)

# 📌 Définir un seuil pour signaler une dérive
ALERT_THRESHOLD = 0.05  # 📌 Seuil de p-value pour alerter

alert_features = drift_report[drift_report["p_value"] < ALERT_THRESHOLD]["feature"].tolist()

# 📌 Enregistrer les métriques dans MLflow
mlflow.set_tracking_uri("http://mlflow:8100")
with mlflow.start_run(run_name="Feature Drift Detection"):
    for _, row in drift_report.iterrows():
        mlflow.log_metric(f"drift_{row['feature']}", row["statistic"])
        mlflow.log_metric(f"p_value_{row['feature']}", row["p_value"])

# 📌 Afficher les résultats
if alert_features:
    print(f"🚨 ALERTE ! Dérive détectée sur : {alert_features}")
else:
    print("✅ Aucune dérive significative détectée.")

print(f"Drift detection report saved to {output_path}")
