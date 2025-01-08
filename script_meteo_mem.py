import pandas as pd

def load_csv():
    """Simule le chargement d'un fichier CSV en retournant un DataFrame vide avec les bonnes colonnes."""
    return pd.DataFrame(columns=["Date", "Température", "Météo", "Ville"])

def format_new_data(raw_data):
    """Formate les nouvelles données en une seule ligne compatible avec le DataFrame."""
    return [raw_data.get("Date"), raw_data.get("Température"), raw_data.get("Météo"), raw_data.get("Ville")]

def add_new_data(existing_df, new_data):
    """Ajoute une nouvelle ligne de données au DataFrame existant."""
    new_row_df = pd.DataFrame([new_data], columns=existing_df.columns)
    return pd.concat([existing_df, new_row_df], ignore_index=True)

def save_csv(updated_df):
    """Simule la sauvegarde d'un DataFrame sans fichier réel."""
    print(f"Données sauvegardées (simulées) :")
    print(updated_df)

def main():
    # Simuler le chargement des données existantes (DataFrame vide ici)
    existing_df = load_csv()
    print("Données existantes :")
    print(existing_df)

    # Exemple de nouvelles données brutes (dictionnaire)
    raw_data = {"Date": "2025-01-07", "Température": 25.5, "Météo": "Clear", "Ville": "Sydney"}
    
    # Formater les nouvelles données en une seule ligne
    new_data = format_new_data(raw_data)
    print("Nouvelle ligne formatée :", new_data)

    # Ajouter la nouvelle ligne
    updated_df = add_new_data(existing_df, new_data)
    print("Données mises à jour :")
    print(updated_df)

    # Simuler la sauvegarde des données mises à jour
    save_csv(updated_df)

if __name__ == "__main__":
    main()

