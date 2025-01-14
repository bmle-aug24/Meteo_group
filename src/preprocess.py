import pandas as pd
import yaml
from sklearn.model_selection import train_test_split
import os
import subprocess


def load_config(yaml_path):
    """
    Charger la configuration depuis un fichier YAML.
    """
    with open(yaml_path, "r") as file:
        return yaml.safe_load(file)


def remove_nan_target(df, target_column):
    """
    Supprime les lignes où la colonne cible contient des NaN.
    """
    cleaned_data = df.dropna(subset=[target_column])
    print(f"Lignes supprimées (NaN dans cible) : {len(df) - len(cleaned_data)}")
    return cleaned_data


def preprocess_data(df, target_column):
    """
    Prétraiter les données : gérer les NaN, encoder les colonnes catégoriques, et convertir les dates.
    """
    # Supprimer les lignes où la cible est NaN
    df = remove_nan_target(df, target_column)

    # Gestion des NaN dans les colonnes numériques
    numerical_columns = df.select_dtypes(include=["float", "int"]).columns
    df.loc[:, numerical_columns] = df[numerical_columns].fillna(df[numerical_columns].mean())

    # Gestion des NaN dans les colonnes catégoriques
    categorical_columns = df.select_dtypes(include=["object"]).columns
    df.loc[:, categorical_columns] = df[categorical_columns].fillna("Inconnu")

    # Encodage des colonnes catégoriques
    for col in categorical_columns:
        df.loc[:, col] = df[col].astype("category").cat.codes

        # S'assurer que le type est bien 'int64' après encodage
        df[col] = df[col].astype("int64")

    # Conversion de la colonne Date
    if "Date" in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # Convertir en datetime, erreurs deviennent NaT
        df['Date'] = df['Date'].apply(lambda x: x.toordinal() if pd.notnull(x) else pd.NA)  # Convertir en ordinale
        df['Date'] = df['Date'].astype('Int64')  # Utilisation de 'Int64' pour permettre NaN avec des entiers

    return df


def save_processed_data(X_train, X_test, y_train, y_test, config):
    """
    Sauvegarder les ensembles de données traités et les suivre avec DVC.
    """
    processed_dir = config["data"]["processed_dir"]
    os.makedirs(processed_dir, exist_ok=True)

    X_train.to_csv(os.path.join(processed_dir, "X_train.csv"), index=False)
    X_test.to_csv(os.path.join(processed_dir, "X_test.csv"), index=False)
    y_train.to_csv(os.path.join(processed_dir, "y_train.csv"), index=False)
    y_test.to_csv(os.path.join(processed_dir, "y_test.csv"), index=False)

    # Ajouter les fichiers à DVC pour le suivi
    for file in os.listdir(processed_dir):
        subprocess.run(["dvc", "add", os.path.join(processed_dir, file)])


if __name__ == "__main__":
    # Charger la configuration
    config = load_config("config/config.yaml")

    # Charger les données brutes
    raw_data_path = config["data"]["raw_data_path"]
    target_column = config["model"]["target_column"]
    df = pd.read_csv(raw_data_path)

    # Prétraiter les données
    df = preprocess_data(df, target_column)

    # Séparer les caractéristiques (X) et la cible (y)
    X = df.drop(columns=[target_column])
    y = df[target_column]

    # Diviser en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=config["model"]["test_size"],
        random_state=config["model"]["random_state"]
    )

    # Sauvegarder
    save_processed_data(X_train, X_test, y_train, y_test, config)
