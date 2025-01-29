import pandas as pd
from scipy.stats import ks_2samp
import os

# Chemins des fichiers (adaptés pour Docker)
train_data_path = "/app/data/processed/X_train.csv"
log_data_path = "/app/data/production_logs/requests_log.csv"
output_path = "/app/data/monitoring/drift_report.csv"

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

# Calculer la dérive (Kolmogorov-Smirnov test)
drift_results = []
for column in common_columns:
    stat, p_value = ks_2samp(X_train[column], requests_log[column])
    drift_results.append({"feature": column, "statistic": stat, "p_value": p_value})

# Créer un DataFrame pour le rapport
drift_report = pd.DataFrame(drift_results)

# Enregistrer le rapport
os.makedirs(os.path.dirname(output_path), exist_ok=True)
drift_report.to_csv(output_path, index=False)

print(f"Drift detection report saved to {output_path}")
