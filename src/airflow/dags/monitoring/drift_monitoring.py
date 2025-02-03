import pandas as pd
from scipy.stats import ks_2samp
import os
import mlflow
import json
import seaborn as sns
import matplotlib.pyplot as plt

# Chemins des fichiers
train_data_path = "/app/data/processed/X_train.csv"
log_data_path = "/app/data/production_logs/requests_log.csv"
csv_output_path = "/app/data/monitoring/drift_report.csv"
json_output_path = "/app/data/monitoring/drift_summary.json"
output_visualizations_dir = "/app/data/monitoring/visualizations/"

# Vérification de l'existence des fichiers
if not os.path.exists(train_data_path):
    raise FileNotFoundError(f"Training data not found at {train_data_path}")
if not os.path.exists(log_data_path):
    raise FileNotFoundError(f"Log data not found at {log_data_path}")

# Charger les données
X_train = pd.read_csv(train_data_path)
requests_log = pd.read_csv(log_data_path)

# Identifier les colonnes communes
common_columns = list(set(X_train.columns) & set(requests_log.columns))
if not common_columns:
    raise ValueError("Aucune colonne commune entre les données d'entraînement et les logs de production.")

# Sélectionner uniquement les colonnes communes
X_train = X_train[common_columns]
requests_log = requests_log[common_columns]

# Calcul de la dérive pour chaque colonne avec le test KS
drift_results = []
ALERT_THRESHOLD = 0.05  # seuil pour alerter sur la p-value
for column in common_columns:
    stat, p_value = ks_2samp(X_train[column].dropna(), requests_log[column].dropna())
    drift_detected = p_value < ALERT_THRESHOLD
    drift_results.append({
        "feature": column,
        "statistic": stat,
        "p_value": p_value,
        "drift_detected": drift_detected
    })

# Créer un DataFrame pour le rapport KS et l'enregistrer en CSV
drift_report = pd.DataFrame(drift_results)
os.makedirs(os.path.dirname(csv_output_path), exist_ok=True)
drift_report.to_csv(csv_output_path, index=False)

# Analyse supplémentaire sur des colonnes ciblées pour la dérive descriptive
drift_columns = ["Humidity3pm", "MaxTemp", "Humidity9am", "WindSpeed9am", "Temp3pm"]
drift_summary = {}
stats_train = X_train.describe()
stats_requests = requests_log.describe()

for col in drift_columns:
    if col in X_train.columns and col in requests_log.columns:
        train_mean = stats_train.loc["mean", col]
        requests_mean = stats_requests.loc["mean", col]
        difference = abs(train_mean - requests_mean)
        threshold = 0.1 * train_mean  # seuil à 10% de la moyenne d'entraînement
        drift_detected = difference > threshold
        drift_summary[col] = {
            "train_mean": float(train_mean),
            "requests_mean": float(requests_mean),
            "difference": float(difference),
            "drift_detected": bool(drift_detected)  # Conversion en booléen Python
        }

# Enregistrer le résumé sous format JSON
os.makedirs(os.path.dirname(json_output_path), exist_ok=True)
with open(json_output_path, "w") as f_json:
    json.dump(drift_summary, f_json, indent=4)

# Générer des visualisations pour les colonnes où la dérive est significative
os.makedirs(output_visualizations_dir, exist_ok=True)
significant_drift_columns = [col for col, stats in drift_summary.items() if stats["drift_detected"]]

for col in significant_drift_columns:
    plt.figure(figsize=(8, 5))
    sns.kdeplot(X_train[col].dropna(), label="Train", fill=True, color="blue", alpha=0.4)
    sns.kdeplot(requests_log[col].dropna(), label="Requests Log", fill=True, color="orange", alpha=0.4)
    plt.title(f"Distribution of {col}")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_visualizations_dir, f"{col}_distribution.png"))
    plt.close()

# Enregistrement des métriques dans MLflow
mlflow.set_tracking_uri("http://mlflow:8100")
with mlflow.start_run(run_name="Feature Drift Detection"):
    for _, row in drift_report.iterrows():
        mlflow.log_metric(f"drift_{row['feature']}", row["statistic"])
        mlflow.log_metric(f"p_value_{row['feature']}", row["p_value"])

# Affichage du résultat
alert_features = [row["feature"] for row in drift_results if row["drift_detected"]]
if alert_features:
    print(f"🚨 ALERTE ! Dérive détectée sur : {alert_features}")
else:
    print("✅ Aucune dérive significative détectée.")
print(f"Drift detection report saved to {csv_output_path} and summary to {json_output_path}")
print(f"Visualizations saved to {output_visualizations_dir}")
