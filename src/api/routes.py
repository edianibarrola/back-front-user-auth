"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
# from flask_cors import CORS
from api.utils import generate_sitemap, APIException
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from argon2 import PasswordHasher

ph = PasswordHasher()
api = Blueprint('api', __name__)

# CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend"
    }

    return jsonify(response_body), 200

@api.route('/register', methods=['POST'])
def register():
    content = request.get_json(silent=True)
    user = User(email = content["email"], password = ph.hash(content["password"]), is_active = True)

    db.session.add(user)
    db.session.commit()

    response_body = {
        "message": "User Created"
    }

    return jsonify(response_body), 204

@api.route('/login', methods=['POST'])
def login():

    content = request.get_json()
    print(content)
    user = User.query.filter(User.email == content["email"]).first()
    if user is None:
        return jsonify({"message": "invalid user"}), 403
    
    try:
        ph.verify(user.password, content["password"])
    except:
        return jsonify({"message": "invalid password"}), 403
        
    access_token = create_access_token(identity=user.id, additional_claims={"email":user.email})
    return jsonify({ "token": access_token, "user_id": user.id })

@api.route('/userinfo', methods=['GET'])
@jwt_required()
def userinfo():
    current_user_id = get_jwt_identity()
    
    user = User.query.filter(User.id == current_user_id).first()
    
    response_body = {
        "message": f"Hello {user.email} "
    }

    return jsonify(response_body), 200


@api.route("/reset", methods=["POST"])
def update_password():
    if request.method == "POST":
        # new_password = request.json.get("password")
        email = request.json.get("email")
        password = request.json.get("password")

        if not email:
            return jsonify({"msg": "Missing email in request."}), 400
        if not password:
            return jsonify({"msg":"Missing pw in request."}),400
        
        user = User.query.filter_by(email=email).first()
        
        # Create and set new password
        # result_str = ''.join(random.choice(string.ascii_letters) for i in range(12))
        # new_password_hashed = generate_password_hash(result_str)
        newpass = password
        password = ph.hash(password)
        user.password = password
        db.session.commit()        

        payload = {
            "msg": "Success. An email will be sent to your account with your temporary password.",
            "pass": newpass
        }

        return jsonify(payload), 200

