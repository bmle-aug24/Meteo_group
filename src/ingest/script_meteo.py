import pandas as pd
from datetime import timedelta
from ingest_data import get_day_data  # Importation de la fonction pour récupérer les données via l'API


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
    
    #Sorting and removing duplicates
    updated_df  = updated_df.drop_duplicates(subset=['Date', 'Location'], keep='last') #SVE: Drop duplicates
    updated_df = updated_df.sort_values(by=['Location', 'Date']) #SVE: Sort by date
    updated_df = updated_df.reset_index(drop=True) #SVE: Reset index
    updated_df = updated_df.drop_duplicates(keep='last') #SVE: Drop duplicates
    
    return updated_df

# Fonction pour mettre à jour la colonne RainTomorrow
def update_rain_tomorrow(df):#, new_data):
    """
    Met à jour la colonne RainTomorrow pour une date donnée dans le DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame existant.
        new_data (dict): Données brutes avec la clé "Date" et "RainTomorrow".
    
    Returns:
        pd.DataFrame: DataFrame mis à jour.
    """
    # Vérifier si la date existe dans le DataFrame
    #mask = df["Date"] == new_data["Date"]
    #if mask.any():
    #    # Mettre à jour la colonne RainTomorrow pour cette date
    #    df.loc[mask, "RainTomorrow"] = new_data["RainTomorrow"]
    #    print(f"RainTomorrow mis à jour pour la date {new_data['Date']}.")
    #else:
    #    print(f"La date {new_data['Date']} n'existe pas dans le DataFrame.")
    df['Date'] = pd.to_datetime(df['Date'])
    for location in df['Location'].unique():
        df_temp = df[df['Location'] == location].sort_values(by='Date')
        last_date = df_temp.tail(1)['Date']
        rain_today = df_temp.tail(1)['RainToday']
        last_date_minus_1 = last_date - timedelta(days=1)
        if df[(df['Date'] == last_date_minus_1.values[0]) & (df['Location'] == location)].shape[0] > 0:
            df.loc[(df['Date'] == last_date_minus_1.values[0]) & (df['Location'] == location)]['RainTomorrow'] = rain_today

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
    # Chemin du fichier CSV contenant les données brutes
    raw_data_file_path = "data/raw/weatherAUS.csv"  #SVE: Modify to the correct path

    # Charger les données brutes depuis le fichier CSV
    df = pd.read_csv(raw_data_file_path)
    
    # Récupérer les données via l'API
    data = get_day_data()

    #raw_data = data[0]['Location']  # Exemple d'accès à une location spécifique, ajuster si nécessaire SVE: Biensur il faut le modifier

    # Ajout des nouvelles données au DataFrame
    print("Ajout des nouvelles données au DataFrame...")
    for data_location in data:
        #print(data_location)
        if data_location is not None:
            df = format_and_add_new_data(df, data_location) #SVE: Changed to the same df, if not, it will not collect the data of all the locations, only the last
    
    print("Données mises à jour :")
    print(df.tail())  # Afficher les dernières lignes pour vérifier

    # Exemple de mise à jour de la colonne RainTomorrow
    #new_rain_data = {"Date": "2025-01-08", "RainTomorrow": "No"} #SVE: Useless
    print("\nMise à jour de RainTomorrow...")
    df = update_rain_tomorrow(df)#, new_rain_data)

    # Sauvegarder les modifications
    #save_dataframe(df, raw_data_file_path)
    save_dataframe(df, "data/raw/weatherAUS_Test.csv")

if __name__ == "__main__":
    main()

