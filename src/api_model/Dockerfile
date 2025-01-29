FROM python:3.11.8

# Créer le dossier de l'application
RUN mkdir -p /app/mlflow

# Copier tous les fichiers du répertoire source
COPY . /app

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Lancer l'API avec uvicorn
CMD ["uvicorn", "app_model:api", "--host", "0.0.0.0", "--port", "8000"]
