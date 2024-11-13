from __future__ import annotations

import json
from base64 import b64encode
from werkzeug.security import generate_password_hash
import requests
from pymysql import ProgrammingError
from . import auth_app
from flask import render_template, request, redirect
from .exceptions import InvalidCredentialsException, InvalidRegistrationDataException
from .models import SessionManager
from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from werkzeug.wrappers import Response

auth_url = 'http://127.0.0.1:5001'


def process_api_response(method: str, url: str, **kwargs):
    """Helper function to process API responses.

    Args:
        method (str): HTTP method ('get' or 'post').
        url (str): API endpoint URL.
        kwargs: Additional arguments for the request (e.g., headers, json).

    Returns:
        dict: Parsed JSON response if successful, or None if error.
        str | None: Error message if request failed, else None.
    """
    try:
        response = requests.request(method, url, **kwargs)
        if response.status_code != 200:
            return None, "Try again later"
        result = json.loads(response.text)
        if result['status'] != 200:
            return None, result['message']
        return result, None
    except requests.RequestException as e:
        return None, "An error occurred. Please try again later."


@auth_app.route('/', methods=['GET'])
def auth_login_get_handler() -> str:
    """Handles GET requests for the login page.

    Returns:
        str: Rendered HTML of the login page.
    """
    return render_template('auth_index.html')


@auth_app.route('/', methods=['POST'])
def auth_login_post_handler() -> Response:
    """Handles POST requests for user login.

    Returns:
        str | Union[str, Response]: Redirects to the home page upon successful login, or renders the login page with an error.
    """

    if SessionManager.is_authorized():
        redirect('/')

    auth_header = {
        'Authorization': 'Basic ' + b64encode(
            f"{request.form['email']}:{request.form['password']}".encode()).decode()
    }
    result, error = process_api_response(
        method="get",
        url=f"{auth_url}/find_user",
        headers=auth_header
    )

    if error:
        return render_template('auth_index.html', error=error)

    # Данные успешно получены
    SessionManager.add_user_data(result['user_id'], result['role'])
    return redirect('/')


@auth_app.route('/register', methods=['GET'])
def auth_register_get_handler() -> str:
    """Handles GET requests for the registration page.

    Returns:
        str: Rendered HTML of the registration page.
    """
    return render_template('registration.html')


@auth_app.route('/register', methods=['POST'])
def auth_register_post_handler() -> str:
    """Handles POST requests for user registration.

    Returns:
        str: Rendered HTML of the successful registration page or registration page with an error.
    """
    data = {
        'email': request.form['email'],
        'password': generate_password_hash(request.form['password']),
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'phone_number': request.form['phone_number'],
        'renter_address': request.form['renter_address'],
        'business_sphere': request.form['business_sphere']
    }
    result, error = process_api_response(
        method="post",
        url=f"{auth_url}/register_renter",
        json=data
    )

    if error:
        return render_template('registration.html', error=error)
    return render_template('successful_registration.html')


@auth_app.route('/logout', methods=['GET'])
def auth_logout_handler() -> Response:
    """Handles GET requests for logging out the user.

    Returns:
        Response: Redirects to the home page after logging out.
    """
    SessionManager.clear_session()
    return redirect('/')
