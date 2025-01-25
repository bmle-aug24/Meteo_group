from flask import Flask, jsonify, request
from datetime import timedelta
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users_db = {
    "danieldatascientest": {
        "username": "danieldatascientest",
        "name": "Daniel Datascientest",
        "email": "daniel@datascientest.com",
        "hashed_password": pwd_context.hash('datascientest'),
        "resource": "API prediction",
        "role": ["user"]
    },
    "johndatascientest": {
        "username": "johndatascientest",
        "name": "John Datascientest",
        "email": "john@datascientest.com",
        "hashed_password": pwd_context.hash('secret'),
        "resource": "Entrainement Service",
        "role": ["admin"]
    }
}

api = Flask(import_name="my_api")
api.config["JWT_SECRET_KEY"] = "96a0c910f342e9772c403c7db9de6a21036d12bb51cc3de2ffabdf143419eeb3"
api.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
jwt = JWTManager(api)

def check_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(database, username):
    return database.get(username)

@api.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = get_user(users_db, username)
    if not user or not check_password(password, user['hashed_password']):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@api.route("/resource", methods=["GET"])
@jwt_required()
def get_resource():
    current_username = get_jwt_identity()
    user = get_user(users_db, current_username)

    if "admin" in user["role"]:
        return jsonify({
            "message": "Bienvenue admin!",
            "resource": "Ressource spéciale pour les administrateurs",
            "owner": current_username
        }), 200

    elif "user" in user["role"]:
        return jsonify({
            "message": "Bienvenue utilisateur!",
            "resource": user["resource"],
            "owner": current_username
        }), 200

    return jsonify({"message": "Accès refusé"}), 403

if __name__ == "__main__":
    api.run()
api.run(host="0.0.0.0", port=5000, debug=True)
