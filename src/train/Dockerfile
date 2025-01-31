# Utiliser une image Python de base
FROM python:3.11.8

# Créer le répertoire d'application
RUN mkdir -p /app && mkdir -p /app/config && mkdir -p /app/data
WORKDIR /app

# Copier les fichiers nécessaires pour le microservice `train`
COPY requirements.txt /app/requirements.txt
COPY train.py /app/train.py

# train.py utilise un fichier de configuration,je peux decommenter le suivant:
#COPY config /app/config
#COPY data /app/data

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

RUN dvc init --no-scm && \
    dvc remote add origin https://dagshub.com/bmle-aug24/Meteo_group.dvc && \
    dvc remote modify origin auth basic && \
    dvc remote modify origin user bmle-aug24 && \
    dvc remote modify origin password 80f0fd7d1ab6a2b1e95664936d78045d71c78e17 && \
    dvc pull # Récupération des fichiers versionnés

# Commande pour exécuter le service de training avec gestion DVC
CMD sh -c "
    dvc pull && \
    python train.py && \
    dvc add /app/mlflow/latest_model.pkl && \
    dvc push" # Versionne et pousse le modèle entraîné

# Commande d'exécution
CMD ["python", "train.py"]
