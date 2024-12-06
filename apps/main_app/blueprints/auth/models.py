import json
from base64 import b64encode
from typing import Any, Optional, Tuple

import requests
from flask import session

auth_url = "http://127.0.0.1:5001"



def process_api_response(
        method: str, url: str, **kwargs: dict[str, Any]
) -> Tuple[Optional[dict[str, str]], Optional[str]]:
    """
    Helper function to process API responses.

    Args:
        method (str): HTTP method ('get' or 'post').
        url (str): API endpoint URL.
        kwargs: Additional arguments for the request (e.g., headers, json).

    Returns:
        Tuple[Optional[dict], Optional[str]]:
            - Parsed JSON response if successful, or None if an error occurred.
            - Error message if the request failed, or None if successful.
    """
    try:
        response = requests.request(method, url, **kwargs)
        if response.status_code != 200:
            return None, "Try again later"
        result = json.loads(response.text)
        if result.get("status") != 200:
            return None, result.get("message", "Unknown error")
        return result, None
    except requests.RequestException:
        return None, "An error occurred. Please try again later."


def authenticate_user(email: str, password: str) -> bool:
    """
    Authenticate a user by sending credentials to the authentication API.

    This function encodes the user's email and password in Base64 format,
    sends it to the authentication API, and processes the response.
    If authentication is successful, user data is added to the session.

    Args:
        email (str): The user's email address.
        password (str): The user's password.

    Returns:
        bool: True if the user is authenticated successfully.

    Raises:
        ValueError: If the API response indicates an error.
    """
    # Constructing the Authorization header with Base64 encoding.
    auth_header = (
            "Basic "
            + b64encode(f"{email}:{password}".encode()).decode()
    )

    # Sending a request to the authentication API.
    result, error = process_api_response(
        method="get",
        url=f"{auth_url}/find_user",
        headers={"Authorization": auth_header},
    )

    # Handling the API response.
    if not result:
        raise ValueError(error)

    # Storing user data in the session manager.
    SessionManager.add_user_data(result["user_id"], result["role"])

    return True

class SessionManager:
    """
    Manages user session data for login and authorization processes.

    This class provides utilities to handle user session data,
    including setting, clearing, and verifying user authorization status.
    """

    @classmethod
    def add_user_data(cls, user_id: str, role: str) -> None:
        """
        Adds user-specific data to the session upon successful login.

        Args:
            user_id (str): Unique identifier of the user, typically their email or ID.
            role (str): The role or permissions level of the user (e.g., "admin", "user").

        Raises:
            KeyError: If the session cannot be updated (rare edge case).
        """
        session["user_id"] = user_id
        session["role"] = role

    @classmethod
    def clear_user_data(cls) -> None:
        """
        Removes user-specific data from the session.

        This method ensures that user-related keys such as "user_id"
        and "role" are safely removed from the session.
        """
        session.pop("user_id", None)
        session.pop("role", None)

    @classmethod
    def clear_session(cls) -> None:
        """
        Clears all session data.

        This method is a complete reset of the session and removes all keys.
        Useful for a full logout or session invalidation process.
        """
        session.clear()

    @classmethod
    def is_authorized(cls) -> bool:
        """
        Checks whether a user is currently authorized.

        Returns:
            bool: True if the session contains a "user_id", indicating
                  an active login. False otherwise.
        """
        return "user_id" in session
