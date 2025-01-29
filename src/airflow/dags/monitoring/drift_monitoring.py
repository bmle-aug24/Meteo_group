import pandas as pd
from scipy.stats import ks_2samp
import os
import seaborn as sns
import matplotlib.pyplot as plt
import json

# Chemins des fichiers
train_data_path = "../../data/processed/X_train.csv"
log_data_path = "../../data/production_logs/requests_log.csv"
output_drift_report_path = "../../data/monitoring/drift_report.csv"
output_visualizations_dir = "../../data/monitoring/visualizations/"
output_drift_summary_path = "../../data/monitoring/drift_summary.json"

# Vérifier si les fichiers existent
if not os.path.exists(train_data_path):
    raise FileNotFoundError(f"Training data not found at {train_data_path}")

if not os.path.exists(log_data_path):
    raise FileNotFoundError(f"Log data not found at {log_data_path}")

# Charger les données
X_train = pd.read_csv(train_data_path)
requests_log = pd.read_csv(log_data_path)

# Aligner les colonnes
common_columns = list(set(X_train.columns).intersection(set(requests_log.columns)))
X_train = X_train[common_columns]
requests_log = requests_log[common_columns]

# Colonnes dérivantes à surveiller
drift_columns = ["Humidity3pm", "MaxTemp", "Humidity9am", "WindSpeed9am", "Temp3pm"]

# Calculer la dérive (Kolmogorov-Smirnov test)
drift_results = []
significant_drift_columns = []
for column in common_columns:
    stat, p_value = ks_2samp(X_train[column], requests_log[column])
    drift_results.append({"feature": column, "statistic": stat, "p_value": p_value})
    if p_value < 0.05:
        significant_drift_columns.append(column)

# Créer un DataFrame pour le rapport
drift_report = pd.DataFrame(drift_results)

# Enregistrer le rapport
os.makedirs(os.path.dirname(output_drift_report_path), exist_ok=True)
drift_report.to_csv(output_drift_report_path, index=False)

# Calculer les statistiques descriptives
stats_train = X_train.describe()
stats_requests = requests_log.describe()

# Comparer les moyennes et détecter les dérives
drift_summary = {}
for col in drift_columns:
    if col in X_train.columns and col in requests_log.columns:
        train_mean = stats_train.loc["mean", col]
        requests_mean = stats_requests.loc["mean", col]
        difference = abs(train_mean - requests_mean)
        threshold = 0.1 * train_mean
        drift_detected = difference > threshold

        drift_summary[col] = {
            "train_mean": float(train_mean),
            "requests_mean": float(requests_mean),
            "difference": float(difference),
            "drift_detected": bool(drift_detected),  # Convertir explicitement en booléen JSON compatible
        }

# Sauvegarder le résumé de la dérive dans un fichier JSON
with open(output_drift_summary_path, "w") as f:
    json.dump(drift_summary, f, indent=4)

# Générer des visualisations pour les colonnes avec dérive
os.makedirs(output_visualizations_dir, exist_ok=True)
for column in significant_drift_columns:
    plt.figure(figsize=(8, 5))
    sns.kdeplot(X_train[column], label="Train", fill=True, color="blue", alpha=0.4)
    sns.kdeplot(requests_log[column], label="Requests Log", fill=True, color="orange", alpha=0.4)
    plt.title(f"Distribution of {column}")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_visualizations_dir, f"{column}_distribution.png"))
    plt.close()

# Messages de confirmation
print(f"Drift detection report saved to {output_drift_report_path}")
print(f"Drift summary saved to {output_drift_summary_path}")
print(f"Visualizations saved to {output_visualizations_dir}")
