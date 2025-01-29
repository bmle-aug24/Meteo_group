FROM python:3.11

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers nécessaires
COPY . /app

# Installer les dépendances nécessaires
RUN pip install --no-cache-dir -r requirements.txt

# Commande par défaut pour exécuter le script de monitoring
CMD ["python", "drift_detection.py"]
