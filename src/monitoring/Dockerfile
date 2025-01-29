# Utiliser une image de base Python
FROM python:3.11

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le script de drift detection et les fichiers nécessaires
COPY drift_detection.py /app/
COPY requirements.txt /app/

# Installer les dépendances nécessaires
RUN pip install --no-cache-dir -r requirements.txt

# Commande par défaut pour exécuter le script
CMD ["python", "drift_detection.py"]
