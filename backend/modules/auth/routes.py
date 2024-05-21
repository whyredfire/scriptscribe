from flask import Blueprint, jsonify, redirect, request
from pymongo import MongoClient
import hashlib
import os

auth_bp = Blueprint('auth', __name__, static_folder='static',
                    template_folder='templates')

host = os.environ.get('MONGO_HOST', 'localhost')
port = os.environ.get('MONGO_PORT', '27017')
connection_string = f'mongodb://{host}:{port}/'

client = MongoClient(connection_string)
collection = client.scriptscribe.users


def validate_creds(username, password):
    if not username:
        return jsonify({
            'message': 'username cannot be empty',
            'isSuccessful': False
        }), 200
    elif not password:
        return jsonify({
            'message': 'password cannot be empty',
            'isSuccessful': False
        }), 200


def check_user(username):
    users = list(collection.find())
    for user in users:
        if user.get('username') == username:
            return True
    return False


def salty_pass(username, password):
    salt = 'scriptscribeftw'
    salted_pass = username + salt + password

    hashed_pass = hashlib.md5(salted_pass.encode())
    return hashed_pass.hexdigest()


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
        }), 200

    if user_auth(username, password):
        return jsonify({
            'message': 'logged in',
            'isSuccessful': True
        }), 200
    else:
        return jsonify({
            'message': 'incorrect password',
            'isSuccessful': False
        }), 200


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
        }), 200

    hashed_pass = salty_pass(username, password)

    if (add_user(username, hashed_pass)):
        return jsonify({
            'message': 'signed up',
            'isSuccessful': True
        }), 200
