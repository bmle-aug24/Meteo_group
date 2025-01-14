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


push: 
git rm -r --cached venv  #supprimer le cache
git status               #confimer qu"'il n'y a plus de cachde
git add .gitignore       # confirmer modif
git commit -m "Ajout de venv dans .gitignore et suppression du cache"
git filter-repo --path venv --invert-paths --force  # ,ettoyage objets lourd
git gc --prune=now --aggressive   #check
git push origin ellie --force

git remote -v   #check depot distant
git remote add origin https://github.com/bmle-aug24/Meteo_group.git  #ajouter depot distant
si pas le bon: git remote set-url origin https://github.com/bmle-aug24/Meteo_group.git
git remote -v
git push origin ellie --force


git log --oneline



export PYTHONPATH="$PWD:$PYTHONPATH"
ou
export PYTHONPATH=$PWD/src:$PYTHONPATH
pytest tests_unitaires/test_preprocess.py
pytest tests_unitaires/test_xgboost_model.py