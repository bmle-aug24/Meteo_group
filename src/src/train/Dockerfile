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

# Commande d'exécution
CMD ["python", "train.py"]
