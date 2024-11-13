import json
from collections.abc import Callable
from functools import wraps
from typing import TypeVar
from flask import session, render_template_string, request, redirect, url_for

RetType = TypeVar('RetType')


def login_required(f: Callable[..., RetType]) -> Callable[..., RetType]:
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'role' not in session:
            return redirect(url_for('auth.auth_login_get_handler'))
        return f(*args, **kwargs)

    return wrap


def role_required(func: Callable[..., RetType]) -> Callable[..., RetType]:
    permissions = dict(map(lambda kv: (kv[0], set(kv[1])), json.load(open('data/permissions.json')).items()))

    @wraps(func)
    def wrap(*args, **kwargs):
        role = session.get('role')
        endpoint = request.endpoint

        if endpoint.split('.')[-1] in permissions[role]:
            return func(*args, **kwargs)

        return render_template_string('You do not have rights to access this page')

    return wrap
