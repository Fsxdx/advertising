import json
import os
from functools import reduce
from flask import Flask, render_template, request, render_template_string, session
from apps.common.wrappers import login_required, role_required
from blueprints.renter.models import Billboard
from blueprints.query import query_app
from blueprints.renter import renter_app
from blueprints.auth import auth_app
from blueprints.report import report_app
import logging

app = Flask(__name__)
app.register_blueprint(auth_app, url_prefix='/auth')
app.register_blueprint(renter_app, url_prefix='/rent')
app.register_blueprint(query_app, url_prefix='/query')
app.register_blueprint(report_app, url_prefix='/report')

app.secret_key = """b!e.*(mi]cQkOR1Wh^oRmzkM#PcL.A"[;cfel/)#NF%CAi+?c<;/:sV@*Tua]V&"""

# Load the configuration from a JSON files
with open('data/db_config.json', 'r') as db_config_file:
    app.config['db_config'] = json.load(db_config_file)

with open('data/permissions.json', 'r') as permissions_file:
    app.config['permissions'] = dict(map(lambda kv: (kv[0], set(kv[1])), json.load(permissions_file).items()))


# Apply wrappers to routes where it is necessary
role_req_endpoints = reduce(lambda x, y: x | y, app.config['permissions'].values())
for endpoint, func in app.view_functions.items():
    if endpoint.split('.')[-1] in role_req_endpoints:
        app.view_functions[endpoint] = login_required(role_required(func))

# Initialize the SQLProvider
# sql_provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

# Set up logging configuration
logging.basicConfig(level=logging.ERROR,
                    filename='log/app.log',
                    filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

with open('data/roles.json', 'r') as roles:
    roles = json.load(roles)


@app.route('/', methods=['GET'])
@login_required
def handle_index():
    print(request.endpoint)
    if "role" in session and session["role"] in roles["inner"]:
        return render_template("inner_index.html",
                               role=session['role'])
    billboards = Billboard.get_random_billboards(6)
    return render_template('outer_index.html',
                           billboards=billboards,
                           is_auth='user_id' in session)


if __name__ == '__main__':
    app.run()
