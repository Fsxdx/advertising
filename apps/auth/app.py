from __future__ import annotations

import json
import logging
from os import environ
from typing import TYPE_CHECKING

from apps.auth.models import AuthManager
from flask import Flask, jsonify, request

if TYPE_CHECKING:
    from werkzeug.wrappers import Response
app = Flask(__name__)
app.secret_key = environ['SECRET_KEY']

# Load the database configuration from a JSON file
try:
    with open("apps/auth/data/db_config.json", "r", encoding="utf-8") as db_config_file:
        app.config["db_config"] = json.load(db_config_file)
    app.config['db_config']['host'] = environ['DB_HOST']
except FileNotFoundError as error:
    logging.error("Database configuration file not found: %s", error)
    raise RuntimeError("Database configuration file is missing") from error
except json.JSONDecodeError as error:
    logging.error("Error decoding database configuration file: %s", error)
    raise ValueError("Invalid JSON in database configuration file") from error

# Set up logging configuration
logging.basicConfig(
    level=logging.ERROR,
    filename="apps/auth/log/app.log",
    filemode="w",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@app.route("/find_user", methods=["GET"])
def find_user_handler() -> tuple[Response, int]:
    """
    Handle the `/find_user` endpoint to authenticate a user based on Basic Authentication.

    This endpoint validates the request using Basic Authentication headers.
    If the credentials are valid, the user's details are returned.

    Returns:
        tuple[Response, int]: JSON response with user data or error message, and HTTP status code.
    """
    return jsonify(AuthManager.get_user(request)), 200


@app.route("/register_renter", methods=["POST"])
def register_handler() -> tuple[Response, int]:
    """
    Handle the `/register_renter` endpoint to register a new renter.

    This endpoint accepts user registration data as a JSON payload and
    creates a new renter if the data is valid and the email is not already taken.

    Returns:
        tuple[Response, int]: JSON response with status and message, and HTTP status code.
    """
    return jsonify(AuthManager.register_user(request)), 200


if __name__ == "__main__":
    app.run()
