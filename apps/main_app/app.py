import json
import logging
from functools import reduce
from typing import Dict, Set

from blueprints.auth import auth_app
from blueprints.query import query_app
from blueprints.renter import renter_app
from blueprints.renter.models import Billboard
from blueprints.report import report_app
from flask import Flask, render_template, request, session

from apps.common.wrappers import login_required, role_required

# Initialize the Flask application
app = Flask(__name__)

# Register blueprints for modular organization
app.register_blueprint(auth_app, url_prefix="/auth")
app.register_blueprint(renter_app, url_prefix="/rent")
app.register_blueprint(query_app, url_prefix="/query")
app.register_blueprint(report_app, url_prefix="/report")

# Secret key for session management
app.secret_key = """b!e.*(mi]cQkOR1Wh^oRmzkM#PcL.A"[;cfel/)#NF%CAi+?c<;/:sV@*Tua]V&"""

# Load configuration from JSON files
with open("data/db_config.json", "r") as db_config_file:
    app.config["db_config"] = json.load(db_config_file)

with open("data/permissions.json", "r") as permissions_file:
    app.config["permissions"] = {
        key: set(value) for key, value in json.load(permissions_file).items()
    }

# Apply role-based wrappers to endpoints
role_req_endpoints = reduce(lambda x, y: x | y, app.config["permissions"].values())
for endpoint, func in app.view_functions.items():
    if endpoint.split(".")[-1] in role_req_endpoints:
        app.view_functions[endpoint] = login_required(role_required(func))

# Set up logging configuration
logging.basicConfig(
    level=logging.ERROR,
    filename="log/app.log",
    filemode="w",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Load role definitions from a JSON file
with open("data/roles.json", "r") as roles_file:
    roles: Dict[str, Set[str]] = json.load(roles_file)


@app.route("/", methods=["GET"])
@login_required
def handle_index() -> str:
    """
    Render the main index page.

    Returns:
        str: Rendered HTML content for the index page.
    """
    # Log the accessed endpoint for debugging
    print(request.endpoint)

    # Render the inner index for authorized roles
    if "role" in session and session["role"] in roles["inner"]:
        return render_template("inner_index.html", role=session["role"])

    # Fetch random billboards for the outer index page
    billboards = Billboard.get_random_billboards(6)
    return render_template(
        "outer_index.html",
        billboards=billboards,
        is_auth="user_id" in session,
    )


if __name__ == "__main__":
    # Run the Flask development server
    app.run()
