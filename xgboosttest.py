import xgboost as xgb
# Initialiser un modèle XGBoost simple
model = xgb.XGBClassifier(n_estimators=10, max_depth=3)
print("XGBClassifier initialized successfully!")
