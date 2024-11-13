from __future__ import annotations
import json
import os
from flask import Flask, render_template, request, render_template_string, session
from pymysql import ProgrammingError
from flask import render_template, request, redirect, jsonify
from apps.auth.models import User
from typing import Union, TYPE_CHECKING

from apps.auth.utils import is_auth_request_valid, decode_basic_authorization

if TYPE_CHECKING:
    from werkzeug.wrappers import Response
from apps.common.database.sql_provider import SQLProvider
import logging

app = Flask(__name__)

app.secret_key = """b!e.*(mi]cQkOR1Wh^oRmzkM#PcL.A"[;cfel/)#NF%CAi+?c<;/:sV@*Tua]V&"""

# Load the database configuration from a JSON file
with open('data/db_config.json', 'r') as db_config_file:
    db_config = json.load(db_config_file)
    app.config['db_config'] = db_config

# Initialize the SQLProvider
# sql_provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

# Set up logging configuration
logging.basicConfig(level=logging.ERROR,
                    filename='log/app.log',
                    filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


@app.route('/find_user', methods=['GET'])
def find_user_handler() -> tuple[Response, int]:
    if not is_auth_request_valid(request):
        return jsonify({"status": 400, "message": "Bad Request"}), 200
    email, password = decode_basic_authorization(request)
    print(email, password)

    try:
        user = User.get_by_email(email)
        if user and user.check_password(password):
            return jsonify({"status": 200, "message": "OK", "user_id": user.user_id, "role": user.role}), 200
        else:
            return jsonify({"status": 404, "message": "Bad Credentials"}), 200

    except ProgrammingError as e:
        print(e)
        return jsonify({"status": 500, "message": "Try again later"}), 200


@app.route('/register_renter', methods=['POST'])
def register_handler() -> tuple[Response, int]:
    data = request.json
    if ('email' not in data or 'password' not in data or 'first_name' not in data or 'last_name' not in data
            or 'phone_number' not in data or 'renter_address' not in data or 'business_sphere' not in data):
        return jsonify({"status": 415, "message": "Bad Request"}), 200

    try:
        if User.get_by_email(data['email']):
            return jsonify({"status": 400, "message": "User with the same name already exists"}), 200
        role = 'renter'
        User.create_renter(role, data['email'], data['password'],
                           first_name=data['first_name'],
                           last_name=data['last_name'],
                           phone_number=data['phone_number'],
                           renter_address=data['renter_address'],
                           business_sphere=data['business_sphere'])
        return jsonify({"status": 200, "message": "OK"}), 200
    except ProgrammingError:
        return jsonify({"status": 500, "message": "Try again later"}), 200


if __name__ == '__main__':
    app.run()
