from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from config import Config

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    auth_key = request.json.get("api_key")
    if auth_key == Config.API_KEY:
        access_token = create_access_token(identity="user")
        return jsonify(access_token=access_token)
    return jsonify({"message": "Invalid API Key"}), 401
