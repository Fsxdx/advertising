import json
import logging
from functools import reduce
from os import environ
from typing import Dict, Set

from apps.common.wrappers import login_required, role_required
from apps.main_app.blueprints.auth import auth_app
from apps.main_app.blueprints.query import query_app
from apps.main_app.blueprints.renter import renter_app
from apps.main_app.blueprints.renter.models import Billboard
from apps.main_app.blueprints.report import report_app
from flask import Flask, render_template, session
from werkzeug.exceptions import Forbidden

app = Flask(__name__)

app.register_blueprint(auth_app, url_prefix="/auth")
app.register_blueprint(renter_app, url_prefix="/rent")
app.register_blueprint(query_app, url_prefix="/query")
app.register_blueprint(report_app, url_prefix="/report")

app.secret_key = environ['SECRET_KEY']

# Load configuration from JSON files
try:
    with open("apps/main_app/data/db_config.json", "r") as db_config_file:
        app.config["db_config"] = json.load(db_config_file)

    for key, value in app.config['db_config'].items():
        value['host'] = environ['DB_HOST']

    with open("apps/main_app/data/permissions.json", "r") as permissions_file:
        app.config["permissions"] = {
            key: set(value) for key, value in json.load(permissions_file).items()
        }
except FileNotFoundError as error:
    logging.error("Database configuration file not found: %s", error)
    raise RuntimeError("Database configuration file is missing") from error
except json.JSONDecodeError as error:
    logging.error("Error decoding database configuration file: %s", error)
    raise ValueError("Invalid JSON in database configuration file") from error

# Apply role-based wrappers to endpoints
role_req_endpoints = reduce(lambda x, y: x | y, app.config["permissions"].values())
for endpoint, func in app.view_functions.items():
    if endpoint.split(".")[-1] in role_req_endpoints:
        app.view_functions[endpoint] = login_required(role_required(func))  # type: ignore

# Set up logging configuration
logging.basicConfig(
    level=logging.ERROR,
    filename="apps/main_app/log/app.log",
    filemode="w",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Load role definitions from a JSON file
with open("apps/main_app/data/roles.json", "r") as roles_file:
    roles: Dict[str, Set[str]] = json.load(roles_file)


@app.route("/", methods=["GET"])
@login_required
def handle_index() -> str:
    """
    Render the main index page.

    Returns:
        str: Rendered HTML content for the index page.
    """
    if "role" in session and session["role"] in roles["inner"]:
        return render_template("inner_index.html", role=session["role"])

    billboards = Billboard.get_random_billboards(6)
    return render_template(
        "outer_index.html",
        billboards=billboards,
        is_auth="user_id" in session,
    )


@app.errorhandler(Forbidden)
def handle_access_forbidden(e: Forbidden) -> tuple[str, int]:
    """
    Handles HTTP 403 Forbidden errors in the Flask application.

    Args:
        e (Forbidden): The exception instance representing the forbidden error.

    Returns:
        tuple[str, int]: A tuple containing the rendered error page as a string
        and the HTTP status code (403).
    """
    return render_template("error.html", description=e.description), 403


if __name__ == "__main__":
    app.run()
