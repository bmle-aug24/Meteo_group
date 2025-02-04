#!/bin/bash

if test ! -f "/app/.initialized"; then
    echo "Running initialization command..." &&
    apt update && apt install -y git &&
    pip install dvc &&
    cd /app/repo &&
    ls -a &&
    git status &&
    dvc pull data/raw --force &&
    echo 'Pull completed'  # Récupère les fichiers versionnés depuis DagsHub

    touch /app/.initialized
    echo "Initialization complete."
    exit 0
fi
echo "Skipping initialization command..."

if test "$#" -gt 0 ; then
    echo "Executing provided command: $@"
    exec "$@"
    exit 0
fi
#tail -f /dev/null

