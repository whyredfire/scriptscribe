from datetime import datetime, timedelta, timezone
from flask import Blueprint, jsonify, make_response, request

from config import collection
from src.utils.auth import (
    check_user,
    gen_token,
    salty_pass,
    validate_creds,
    validate_token,
)

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/api/token", methods=["GET"])
def check_token():
    token = request.cookies.get("token")
    decoded = validate_token(token)
    if not decoded["valid"]:
        return jsonify({"message": "Not logged in!"}), 500
    print(decoded)
    username = decoded["payload"]["username"]
    print(username)

    return jsonify({"message": "Logged in!", "username": username}), 200


@auth_bp.route("/api/login", methods=["POST"])
def auth():
    def user_auth(username, password):
        users = list(collection.find())
        for user in users:
            if user.get("username") == username and user.get("password") == salty_pass(
                username, password
            ):
                return True
        return False

    data = request.get_json()
    username = data["username"]
    password = data["password"]

    response = validate_creds(username, password)
    if response:
        return response

    if not check_user(username):
        return jsonify({"message": "user does not exist"}), 401

    if user_auth(username, password):
        token = gen_token(username)
        response = make_response(jsonify({"message": "logged in"}))
        expires = datetime.now(timezone.utc) + timedelta(days=7)
        response.set_cookie("token", token, expires=expires)
        return response, 200

    return jsonify({"message": "incorrect password"}), 401


@auth_bp.route("/api/signup", methods=["POST"])
def signup():
    def add_user(username, hashed_pass):
        new_user = {"username": username, "password": hashed_pass}
        inserted_id = collection.insert_one(new_user).inserted_id
        return inserted_id

    data = request.get_json()
    username = data["username"]
    password = data["password"]

    response = validate_creds(username, password)
    if response:
        return response

    if check_user(username):
        return jsonify({"message": "username already taken"}), 409

    hashed_pass = salty_pass(username, password)

    if add_user(username, hashed_pass):
        return jsonify({"message": "signed up"}), 201

    return jsonify({"message": "something went wrong"}), 500
