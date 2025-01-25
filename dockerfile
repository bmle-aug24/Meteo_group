# Utiliser une image Python comme base
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier requirements.txt et installer les dépendances
COPY ./requirements.txt /app/
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    pip install --no-cache-dir -r /app/requirements.txt dvc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Créer le dossier raw et copier les données brutes
RUN mkdir -p /app/data/raw
COPY ./data/raw/weatherAUS.csv /app/data/raw/weatherAUS.csv

# Copier les scripts et le fichier de configuration
COPY ./src/preprocess/ /app/src/preprocess/
COPY ./src/config.yaml /app/src/config.yaml

# Copier le fichier dvc.yaml et initialiser DVC sans Git
COPY ./dvc.yaml /app/dvc.yaml
RUN dvc init --no-scm

# Définir la commande par défaut pour exécuter le script de preprocessing
CMD ["python", "/app/src/preprocess/preprocess.py"]