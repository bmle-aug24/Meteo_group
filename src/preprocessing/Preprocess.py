# preprocess.py

import pandas as pd
import yaml
from sklearn.model_selection import train_test_split
import os
import subprocess

def load_config(yaml_path):
    """
    Je crée cette fonction pour charger la configuration depuis un fichier YAML.
    Elle lit simplement le fichier et renvoie un dictionnaire Python.
    """
    with open(yaml_path, "r") as file:
        return yaml.safe_load(file)

def remove_nan_target(df, target_column):
    """
    Ici, je supprime les lignes où la colonne cible contient des valeurs manquantes (NaN).
    J'affiche également le nombre de lignes supprimées, pour info.
    """
    cleaned_data = df.dropna(subset=[target_column])
    print(f"Lignes supprimées (NaN dans la cible) : {len(df) - len(cleaned_data)}")
    return cleaned_data

def preprocess_data(df, target_column):
    """
    Cette fonction réalise le prétraitement des données :
    1) Supprimer les NaN dans la colonne cible (target_column).
    2) Remplir les NaN dans les colonnes numériques par la moyenne.
    3) Remplir les NaN dans les colonnes catégoriques par 'Inconnu'.
    4) Encoder les colonnes catégoriques en codes numériques (int).
    5) Convertir la colonne 'Date' en format ordinal si elle existe.
    
    J'ai décidé ici d'adopter l'approche de remplissage (imputation) des valeurs manquantes
    plutôt que de les supprimer, afin de conserver un maximum de données.
    """
    # 1) Supprimer NaN dans la cible
    df = remove_nan_target(df, target_column)

    # IMPORTANT : on force la copie pour éviter les SettingWithCopyWarning
    df = df.copy()

    # 2) Remplir les NaN numériques par la moyenne
    numerical_columns = df.select_dtypes(include=["float", "int"]).columns
    df.loc[:, numerical_columns] = df.loc[:, numerical_columns].fillna(df.loc[:, numerical_columns].mean())

    # 3) Remplir les NaN catégoriques par "Inconnu"
    categorical_columns = df.select_dtypes(include=["object"]).columns
    df.loc[:, categorical_columns] = df.loc[:, categorical_columns].fillna("Inconnu")

    # 4) Encoder les colonnes catégoriques en codes (par exemple, "Yes" -> 0, "No" -> 1, etc.)
    for col in categorical_columns:
        df.loc[:, col] = df.loc[:, col].astype("category").cat.codes
        df.loc[:, col] = df.loc[:, col].astype("int64")  # je force l'encodage en int64

    # 5) Conversion de la colonne Date en ordinal si elle existe (pour des modèles qui n'acceptent pas le format date)
    if "Date" in df.columns:
        df.loc[:, "Date"] = pd.to_datetime(df.loc[:, "Date"], errors="coerce")  # Conversion en datetime
        df.loc[:, "Date"] = df.loc[:, "Date"].apply(lambda x: x.toordinal() if pd.notnull(x) else pd.NA)
        df.loc[:, "Date"] = df.loc[:, "Date"].astype("Int64")  # gérer les NaN avec un type 'Int64'

    return df

def save_processed_data(X_train, X_test, y_train, y_test, config):
    """
    Cette fonction sauvegarde les ensembles de données (X_train, X_test, y_train, y_test) en CSV
    dans le dossier défini dans la config (processed_dir).
    
    J'ajoute ensuite ces fichiers à DVC pour le suivi de versions des données.
    """
    processed_dir = config["data"]["processed_dir"]
    os.makedirs(processed_dir, exist_ok=True)

    # Sauvegarde en CSV
    X_train.to_csv(os.path.join(processed_dir, "X_train.csv"), index=False)
    X_test.to_csv(os.path.join(processed_dir, "X_test.csv"), index=False)
    y_train.to_csv(os.path.join(processed_dir, "y_train.csv"), index=False)
    y_test.to_csv(os.path.join(processed_dir, "y_test.csv"), index=False)

    # Optionnel : Ajouter ces CSV à DVC pour la traçabilité des données
    """
    for file in os.listdir(processed_dir):
        if file.endswith(".csv"):
            subprocess.run(["dvc", "add", os.path.join(processed_dir, file)])
    """
if __name__ == "__main__":
    # 1) Je charge la config (config.yaml)
    config = load_config("config/config.yaml")

    # 2) Je récupère le chemin du CSV brut et la colonne cible
    raw_data_path = config["data"]["raw_data_path"]
    target_column = config["model"]["target_column"]

    # 3) Lecture du CSV brut dans un DataFrame
    df = pd.read_csv(raw_data_path)

    # 4) J'effectue le prétraitement tel que défini ci-dessus
    df = preprocess_data(df, target_column)

    # 5) Je sépare X et y (caractéristiques et cible)
    X = df.drop(columns=[target_column])
    y = df[target_column]

    # 6) Je fais le split train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=config["model"]["test_size"],
        random_state=config["model"]["random_state"]
    )

    # 7) Je sauvegarde ces DataFrames dans des CSV (X_train.csv, X_test.csv, y_train.csv, y_test.csv)
    save_processed_data(X_train, X_test, y_train, y_test, config)

    print("Préprocessing terminé. Les données train/test sont sauvegardées.")
