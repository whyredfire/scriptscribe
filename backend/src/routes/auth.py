from config import collection
from flask import Blueprint, jsonify, make_response, request
from src.utils.auth import check_user, gen_token, salty_pass, validate_creds

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/api/login', methods=['POST'])
def auth():
    def user_auth(username, password):
        users = list(collection.find())
        for user in users:
            if user.get('username') == username and user.get('password') == salty_pass(username, password):
                return True
        return False

    data = request.get_json()
    username = data['username']
    password = data['password']

    response = validate_creds(username, password)
    if response:
        return response

    if not check_user(username):
        return jsonify({
            'message': 'user does not exist',
            'isSuccessful': False
        }), 401

    if user_auth(username, password):
        token = gen_token(username)
        response = make_response(jsonify({
            'message': 'logged in',
            'isSuccessful': True
        }))
        response.set_cookie('token', token)
        return response, 200
    else:
        return jsonify({
            'message': 'incorrect password',
            'isSuccessful': False
        }), 401


@auth_bp.route('/api/signup', methods=['POST'])
def signup():
    def add_user(username, hashed_pass):
        new_user = {
            'username': username,
            'password': hashed_pass
        }
        inserted_id = collection.insert_one(new_user).inserted_id
        return inserted_id

    data = request.get_json()
    username = data['username']
    password = data['password']

    response = validate_creds(username, password)
    if response:
        return response

    if check_user(username):
        return jsonify({
            'message': 'username already taken',
            'isSuccessful': False
        }), 409

    hashed_pass = salty_pass(username, password)

    if (add_user(username, hashed_pass)):
        return jsonify({
            'message': 'signed up',
            'isSuccessful': True
        }), 201
