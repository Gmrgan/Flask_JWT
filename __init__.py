from flask import Flask, render_template, jsonify, request, make_response
from datetime import timedelta
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

app = Flask(__name__)

# Configuration du module JWT
app.config["JWT_SECRET_KEY"] = "Ma_clé_secrete"  # Ma clée privée
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]  # Stockage du JWT dans les cookies
app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token"
jwt = JWTManager(app)

@app.route('/')
def hello_world():
    return render_template('accueil.html')

# Affichage du formulaire de connexion
@app.route("/login", methods=["GET"])
def login_form():
    return render_template('formulaire.html')

# Création d'une route qui vérifie l'utilisateur et retourne un Jeton JWT si ok.
# La fonction create_access_token() est utilisée pour générer un jeton JWT.
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return jsonify({"msg": "Mauvais utilisateur ou mot de passe"}), 401
    
    access_token = create_access_token(identity=username, expires_delta=timedelta(hours=1))
    response = make_response(jsonify({"access_token": access_token}))
    response.set_cookie("access_token", access_token, httponly=True, max_age=3600)
    return response

@app.route("/admin", methods=["POST"])
def admin():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "admin" or password != "admin":
        return jsonify({"msg": "Mauvais utilisateur ou mot de passe"}), 401

    access_token = create_access_token(identity=username, expires_delta=timedelta(hours=1))
    response = make_response(jsonify({"access_token": access_token}))
    response.set_cookie("access_token", access_token, httponly=True, max_age=3600)
    return jsonify(access_token=access_token)

# Route protégée par un jeton valide
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == "__main__":
    app.run(debug=True)
