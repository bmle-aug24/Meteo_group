git checkout ellie    #où est bien sur la branche ellie
git checkout -b ellie #pour être sur la branche
git add .
git commit -m "Mise à jour"
git push origin ellie

environnement virtuel:
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
pip freeze > requirements.txt


git init

dvc init
dvc repro

démarrer mllflow dans un autre terminal:
#!/bin/bash
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns --host 0.0.0.0 --port 5000

