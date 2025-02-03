import pandas as pd
import json
from sklearn.metrics import accuracy_score
import xgboost as xgb

# Définir les colonnes dérivantes
drift_columns = ["Humidity3pm", "MaxTemp", "Humidity9am", "WindSpeed9am", "Temp3pm"]

# Charger les données (remplacez les chemins par vos fichiers)
X_train = pd.read_csv("../../../../data/processed/X_train.csv")
X_test = pd.read_csv("../../../../data/processed/X_test.csv")
y_train = pd.read_csv("../../../../data/processed/y_train.csv").squeeze()
y_test = pd.read_csv("../../../../data/processed/y_test.csv").squeeze()

# Exclure les colonnes dérivantes
X_train_no_drift = X_train.drop(columns=drift_columns)
X_test_no_drift = X_test.drop(columns=drift_columns)

# Entraîner le modèle sans colonnes dérivantes
model_no_drift = xgb.XGBClassifier(n_estimators=10, max_depth=3, random_state=42)
model_no_drift.fit(X_train_no_drift, y_train)
y_pred_no_drift = model_no_drift.predict(X_test_no_drift)
accuracy_no_drift = accuracy_score(y_test, y_pred_no_drift)

# Entraîner le modèle avec toutes les colonnes
model_with_drift = xgb.XGBClassifier(n_estimators=10, max_depth=3, random_state=42)
model_with_drift.fit(X_train, y_train)
y_pred_with_drift = model_with_drift.predict(X_test)
accuracy_with_drift = accuracy_score(y_test, y_pred_with_drift)

# Comparer les précisions
results = {
    "accuracy_no_drift": accuracy_no_drift,
    "accuracy_with_drift": accuracy_with_drift
}

# Sauvegarder les résultats
with open("../../../../data/monitoring/model_comparison.json", "w") as f:
    json.dump(results, f, indent=4)

print(f"Précision sans colonnes dérivantes : {accuracy_no_drift}")
print(f"Précision avec toutes les colonnes : {accuracy_with_drift}")
print("Les résultats sont sauvegardés dans model_comparison.json")
