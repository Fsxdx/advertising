from __future__ import annotations

from os import environ
from typing import Union

from flask import redirect, render_template, request
from werkzeug.security import generate_password_hash
from werkzeug.wrappers import Response

from .blueprint import auth_app
from .models import SessionManager, authenticate_user, process_api_response


@auth_app.route("/", methods=["GET"])
def auth_login_get_handler() -> str:
    """
    Handles GET requests for the login page.

    Returns:
        str: Rendered HTML of the login page.
    """
    return render_template("auth_index.html")


@auth_app.route("/", methods=["POST"])
def auth_login_post_handler() -> Union[str, Response]:
    """
    Handles POST requests for user login.

    Returns:
        Union[str, Response]: Redirects to the home page upon successful login,
        or renders the login page with an error.
    """
    if SessionManager.is_authorized():
        return redirect("/")
    try:
        authenticate_user(request.form['email'],
                          request.form['password'])
        return redirect("/")

    except ValueError as e:
        return render_template("auth_index.html", error=e.args[0])


@auth_app.route("/register", methods=["GET"])
def auth_register_get_handler() -> str:
    """
    Handles GET requests for the registration page.

    Returns:
        str: Rendered HTML of the registration page.
    """
    return render_template("registration.html")


@auth_app.route("/register", methods=["POST"])
def auth_register_post_handler() -> str:
    """
    Handles POST requests for user registration.

    Returns:
        str: Rendered HTML of the successful registration page,
        or the registration page with an error.
    """
    data = {
        "email": request.form["email"],
        "password": generate_password_hash(request.form["password"]),
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "phone_number": request.form["phone_number"],
        "renter_address": request.form["renter_address"],
        "business_sphere": request.form["business_sphere"],
    }

    result, error = process_api_response(
        method="post", url=f"{environ['AUTH_URL']}/register_renter", json=data
    )

    if not result:
        return render_template("registration.html", error=error)

    return render_template("successful_registration.html")


@auth_app.route("/logout", methods=["GET"])
def auth_logout_handler() -> Response:
    """
    Handles GET requests for logging out the user.

    Returns:
        Response: Redirects to the home page after logging out.
    """
    SessionManager.clear_session()
    return redirect("/")
