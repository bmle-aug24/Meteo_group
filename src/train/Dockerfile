FROM python:3.11.8

# Créer les dossiers nécessaires
RUN mkdir -p /app/config /app/data

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY . /app

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exécuter le script d'entraînement
CMD ["python", "train.py"]
