FROM python:3.11.8

# Créer le dossier mlflow
RUN mkdir -p /app/mlruns

# Copier tous les fichiers nécessaires
COPY . /app

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Lancer le serveur MLflow
CMD ["mlflow", "server", "--host", "0.0.0.0", "--port", "8100"]
