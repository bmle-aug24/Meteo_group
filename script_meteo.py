import pandas as pd
from ingest_data import get_day_data  # Importation de la fonction pour récupérer les données via l'API

# Chemin du fichier CSV contenant les données brutes
raw_data_file_path = "données/brutes/meteoAUS.csv"  

# Charger les données brutes depuis le fichier CSV
df = pd.read_csv(raw_data_file_path)

# Fonction pour formater et ajouter de nouvelles données au DataFrame
def format_and_add_new_data(df, raw_data):
    """
    Formate les nouvelles données brutes et les ajoute directement au DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame existant.
        raw_data (dict): Données brutes sous forme de dictionnaire.
    
    Returns:
        pd.DataFrame: DataFrame mis à jour avec la nouvelle ligne.
    """
    new_row_df = pd.DataFrame([raw_data])  # Convertir le dictionnaire en DataFrame avec une seule ligne
    
    # Concaténer le DataFrame existant avec le nouveau
    updated_df = pd.concat([df, new_row_df], ignore_index=True)
    
    return updated_df

# Fonction pour mettre à jour la colonne RainTomorrow
def update_rain_tomorrow(df, new_data):
    """
    Met à jour la colonne RainTomorrow pour une date donnée dans le DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame existant.
        new_data (dict): Données brutes avec la clé "Date" et "RainTomorrow".
    
    Returns:
        pd.DataFrame: DataFrame mis à jour.
    """
    # Vérifier si la date existe dans le DataFrame
    mask = df["Date"] == new_data["Date"]
    if mask.any():
        # Mettre à jour la colonne RainTomorrow pour cette date
        df.loc[mask, "RainTomorrow"] = new_data["RainTomorrow"]
        print(f"RainTomorrow mis à jour pour la date {new_data['Date']}.")
    else:
        print(f"La date {new_data['Date']} n'existe pas dans le DataFrame.")
    
    return df

# Sauvegarder le DataFrame mis à jour
def save_dataframe(df, file_path):
    """
    Sauvegarde le DataFrame dans un fichier CSV.
    
    Args:
        df (pd.DataFrame): DataFrame à sauvegarder.
        file_path (str): Chemin du fichier CSV.
    """
    df.to_csv(file_path, index=False)
    print(f"Fichier {file_path} mis à jour avec succès.")

# TEST DES FONCTIONS
def main():
    # Récupérer les données via l'API
    data = get_day_data()

    raw_data = data[0]['Location']  # Exemple d'accès à une location spécifique, ajuster si nécessaire

    # Ajout des nouvelles données au DataFrame
    print("Ajout des nouvelles données au DataFrame...")
    updated_df = format_and_add_new_data(df, raw_data)
    print("Données mises à jour :")
    print(updated_df.tail())  # Afficher les dernières lignes pour vérifier

    # Exemple de mise à jour de la colonne RainTomorrow
    new_rain_data = {"Date": "2025-01-08", "RainTomorrow": "No"}
    print("\nMise à jour de RainTomorrow...")
    updated_df = update_rain_tomorrow(updated_df, new_rain_data)

    # Sauvegarder les modifications
    save_dataframe(updated_df, raw_data_file_path)

if __name__ == "__main__":
    main()

