import hashlib
import time
from functools import wraps
import jwt
from flask import request, jsonify

from config import collection

SECRET = "scriptscribeftw"


def gen_token(username):
    payload = {"username": username, "timestamp": int(time.time())}
    token = jwt.encode(payload, SECRET, algorithm="HS256")
    return token


def validate_token(token):
    try:
        payload = jwt.decode(token, SECRET, algorithms="HS256")
        return {"valid": True, "payload": payload}
    except jwt.ExpiredSignatureError:
        return {"valid": False, "error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"valid": False, "error": "Invalid token"}


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get("token")
        if not token:
            return jsonify({"error": "Token is missing!"}), 401

        decoded = validate_token(token)
        if not decoded.get("valid"):
            return jsonify({"error": "Invalid token!"}), 401

        return f(*args, **kwargs)

    return decorated_function


def validate_creds(username, password):
    if not username:
        return jsonify({"message": "username cannot be empty"}), 400

    return jsonify({"message": "password cannot be empty"}), 400


def check_user(username):
    users = list(collection.find())
    for user in users:
        if user.get("username") == username:
            return True
    return False


def salty_pass(username, password):
    salt = "scriptscribeftw"
    salted_pass = username + salt + password

    hashed_pass = hashlib.md5(salted_pass.encode())
    return hashed_pass.hexdigest()
