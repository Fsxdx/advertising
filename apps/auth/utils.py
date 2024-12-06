from base64 import b64decode

from flask import Request


def is_auth_request_valid(api_request: Request) -> bool:
    """Validates the presence and format of the Authorization header in the request.

    Args:
        api_request (Request): The incoming Flask request object.

    Returns:
        bool: True if the Authorization header is present and seems valid, False otherwise.
    """
    auth_header: str = api_request.headers.get("Authorization", "")
    # Check if the header exists and contains more than just "Basic".
    if not auth_header or not auth_header.lower().startswith("basic "):
        return False
    return True


def decode_basic_authorization(api_request: Request) -> tuple[str, str]:
    """Decodes the Basic Authorization header and extracts the username and password.

    Args:
        api_request (Request): The incoming Flask request object.

    Returns:
        tuple[str, str]: A tuple containing the username and password.

    Raises:
        ValueError: If the Authorization header is missing, malformed, or improperly encoded.
    """
    auth_header: str | None = api_request.headers.get("Authorization")
    if not auth_header:
        raise ValueError("Authorization header is missing.")

    try:
        # Extract and decode the token from the Authorization header
        token = auth_header.split(" ", 1)[1]  # Only split once
        login_and_password = (
            b64decode(token.encode("ascii")).decode("ascii").split(":", 1)
        )  # Split once for safety
        if len(login_and_password) != 2:
            raise ValueError("Invalid Basic Authorization header format.")
        login, password = login_and_password
        return login, password
    except (IndexError, ValueError, UnicodeDecodeError) as error:
        raise ValueError(f"Failed to decode Basic Authorization header: {error}")
