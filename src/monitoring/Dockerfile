FROM python:3.11

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier tous les fichiers du dossier de monitoring dans /app
COPY . /app

# Installer les dépendances depuis le fichier requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Commande par défaut pour exécuter le script de monitoring
CMD ["python", "drift_monitoring.py"]
