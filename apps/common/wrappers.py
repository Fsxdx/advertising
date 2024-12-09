from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

from flask import current_app, redirect, request, session, url_for
from werkzeug.exceptions import Forbidden
from werkzeug.wrappers import Response

RetType = TypeVar("RetType")


def login_required(f: Callable[..., RetType]) -> Callable[..., RetType | Response]:
    """Decorator that ensures the user is logged in.

    Redirects to the login page if the user is not authenticated (i.e., no 'role' in the session).

    Args:
        f (Callable[..., RetType]): The view function to wrap.

    Returns:
        Callable[..., RetType]: The wrapped function that checks the user's login status before proceeding.
    """

    @wraps(f)
    def wrap(*args: tuple[str], **kwargs: dict[str, Any]) -> RetType | Response:
        # If 'role' is not in the session, the user is not logged in, so redirect to login page
        if "role" not in session:
            return redirect(url_for("auth.auth_login_get_handler"))
        return f(*args, **kwargs)

    return wrap


def role_required(func: Callable[..., RetType]) -> Callable[..., RetType | str]:
    """Decorator that ensures the user has the required role to access a page.

    Checks if the user's role (from the session) has permission to access the current route
    based on the configured roles in the 'permissions' dictionary.

    Args:
        func (Callable[..., RetType]): The view function to wrap.

    Returns:
        Callable[..., RetType]: The wrapped function that checks the user's role before proceeding.

    Raises:
        Forbidden: If the user is not authorized to access page.
    """

    @wraps(func)
    def wrap(*args: tuple[str], **kwargs: dict[str, Any]) -> RetType | str:
        role = session.get("role")
        endpoint = request.endpoint
        if endpoint is None:
            raise ValueError("Endpoint is not set")

        if role and endpoint.split(".")[-1] in current_app.config["permissions"].get(role, []):
            return func(*args, **kwargs)

        raise Forbidden("You don't have rights to access that page.")

    return wrap
