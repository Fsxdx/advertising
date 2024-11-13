from flask import Blueprint

report_app = Blueprint('report', __name__, template_folder='templates')

from . import routes