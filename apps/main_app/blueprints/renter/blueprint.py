from flask import Blueprint

renter_app = Blueprint(
    "renter", __name__, template_folder="templates", static_folder="static"
)
