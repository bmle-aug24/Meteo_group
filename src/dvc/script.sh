#!/bin/bash

if [ "$RUN_COMMAND" = "true" ]; then
    echo "Running default command..." &&
    apt update && apt install -y git &&
    pip install dvc &&
    git init &&
    git config --global user.email 'you@example.com' &&
    git config --global user.name 'Your Name' &&
    dvc init -f &&
    git add .dvc &&
    git commit -m 'Initialize DVC' &&
    dvc remote add origin https://dagshub.com/bmle-aug24/Meteo_group.dvc &&
    dvc remote modify origin auth basic &&
    dvc remote modify origin user bmle-aug24 &&
    dvc remote modify origin password 80f0fd7d1ab6a2b1e95664936d78045d71c78e17 &&
    dvc remote default origin &&
    dvc pull data/raw --force &&
    echo 'Pull completed'  # Récupère les fichiers versionnés depuis DagsHub
else
    echo "Skipping default command..."
    tail -f /dev/null
fi
