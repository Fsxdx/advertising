import json
import os
from flask import Flask, render_template, request, render_template_string, session

from apps.common.wrappers import login_required
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

with open('data/roles.json', 'r') as roles:
    roles = json.load(roles)


@app.route('/', methods=['GET'])
@login_required
def handle_index():
    if "role" in session and session["role"] in roles["inner"]:
        return render_template("inner_index.html", is_auth=True)
    billboards=  Billboard.get_random_billboards(6)
    print(billboards)
    return render_template('outer_index.html',
                           billboards=billboards,
                           is_auth='user_id' in session)


if __name__ == '__main__':
    app.run()
