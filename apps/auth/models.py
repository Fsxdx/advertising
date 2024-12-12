from __future__ import annotations

import logging
from base64 import b64decode
from typing import Optional, Union

from flask import Request, current_app
from pymysql import ProgrammingError
from werkzeug.security import check_password_hash

from apps.auth.exceptions import UserNotFoundError
from apps.common.database.base_model import BaseModel
from apps.common.database.sql_provider import SQLProvider
from apps.common.meta import MetaSQL


def is_auth_request_valid(api_request: Request) -> bool:
    """
    Validates the presence and format of the Authorization header in the request.

    Args:
        api_request (Request): The incoming Flask request object.

    Returns:
        bool: True if the Authorization header is present and seems valid, False otherwise.
    """
    auth_header: str = api_request.headers.get("Authorization", "")
    if not auth_header or not auth_header.lower().startswith("basic "):
        return False
    return True


def decode_basic_authorization(api_request: Request) -> tuple[str, str]:
    """
    Decodes the Basic Authorization header and extracts the username and password.

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
        token = auth_header.split(" ", 1)[1]
        login_and_password = (
            b64decode(token.encode("ascii")).decode("ascii").split(":", 1)
        )
        if len(login_and_password) != 2:
            raise ValueError("Invalid Basic Authorization header format.")
        login, password = login_and_password
        return login, password
    except (IndexError, ValueError, UnicodeDecodeError) as error:
        raise ValueError(f"Failed to decode Basic Authorization header: {error}")


class User(BaseModel, metaclass=MetaSQL):
    """
    Represents a user and provides methods to interact with user-related database operations.

    Attributes:
        user_id (int): Unique identifier for the user.
        role (str): Role assigned to the user.
        email (str): User's email address.
        password (str): Hashed password of the user.
    """
    sql_provider: SQLProvider

    def __init__(self, user_id: int, role: str, email: str, password: str):
        self.user_id = user_id
        self.role = role
        self.email = email
        self.password = password

    @classmethod
    def get_by_id(cls, user_id: int) -> Optional[User]:
        """
        Fetches a user by their unique user_id.

        Args:
            user_id (int): The unique ID of the user to retrieve.

        Returns:
            Optional[User]: A `User` object if found, otherwise raises `UserNotFoundError`.

        Raises:
            UserNotFoundError: If no user with the provided user_id exists.
        """
        result = cls.fetch_one(
            cls.sql_provider.get("get_user_by_id.sql", user_id=user_id),
            current_app.config["db_config"],
        )
        if result:
            return User(*result)  # type: ignore
        raise UserNotFoundError("Could not find user by user_id.")

    @classmethod
    def get_by_email(cls, email: str) -> Optional[User]:
        """
        Fetches a user by their email address.

        Args:
            email (str): The email address of the user to retrieve.

        Returns:
            Optional[User]: A `User` object if found, otherwise raises `UserNotFoundError`.

        Raises:
            UserNotFoundError: If no user with the provided email exists.
        """
        result = cls.fetch_one(
            cls.sql_provider.get("get_user_by_email.sql", email=email),
            current_app.config["db_config"],
        )
        if result:
            return User(*result)  # type: ignore
        raise UserNotFoundError("Could not find user by email.")

    @classmethod
    def create_renter(cls, role: str, email: str, password: str, **kwargs: str) -> bool:
        """
        Creates a new renter user in the database.

        Args:
            role (str): Role of the user (currently supported only renter).
            email (str): Email address of the user.
            password (str): Hashed password for the user.
            **kwargs: Additional user-specific attributes to be stored.

        Returns:
            bool: True if the user is successfully created, False otherwise.

        Raises:
            NotImplementedError: If the role is not 'renter'.
        """
        if role != "renter":
            raise NotImplementedError("Other roles except renter are have not been implemented yet.")
        try:
            with cls.transaction(current_app.config["db_config"]) as cursor:
                user_id = cls.insert(
                    cls.sql_provider.get(
                        "add_user.sql",
                        role=role,
                        email=email,
                        password=password,
                        cursor=cursor,
                    ),
                    current_app.config["db_config"],
                    cursor=cursor,
                )

                cls.insert(
                    cls.sql_provider.get(f"add_{role}.sql", user_id=user_id, **kwargs),
                    current_app.config["db_config"],
                    cursor=cursor,
                )
            return True
        except ProgrammingError as error:
            current_app.logger.error(f"Database error during renter creation: {error}")
            return False

    def check_password(self, password_hash: str) -> bool:
        """
        Checks whether the provided password hash matches the user's stored hashed password.

        Args:
            password_hash (str): The plain text password to verify.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return check_password_hash(self.password, password_hash)


class AuthManager(BaseModel, metaclass=MetaSQL):
    """Handles authentication-related operations such as user retrieval and registration."""

    @classmethod
    def get_user(cls, request: Request) -> dict[str, Union[int, str]]:
        """
        Authenticates a user based on request data.

        Args:
            request (Request): The HTTP request containing authentication headers.

        Returns:
            dict[str, Union[int, str]]: A dictionary containing status and message, and optionally user details.
        """
        if not is_auth_request_valid(request):
            return {"status": 400, "message": "Bad Request"}

        try:
            email, password = decode_basic_authorization(request)
            user: Optional[User] = User.get_by_email(email)

            if user and user.check_password(password):
                return {
                    "status": 200,
                    "message": "OK",
                    "user_id": user.user_id,
                    "role": user.role,
                }
            return {"status": 401, "message": "Unauthorized"}
        except ValueError as error:
            logging.error("Error while decoding: %s", error)
            return {"status": 400, "message": "Invalid token value"}
        except UserNotFoundError as error:
            logging.warning("User not found: %s", error)
            return {"status": 404, "message": "User not found"}
        except ProgrammingError as error:
            logging.error("Database error in find_user_handler: %s", error)
            return {"status": 500, "message": "Internal Server Error"}

    @classmethod
    def register_user(cls, request: Request) -> dict[str, Union[int, str]]:
        """
        Registers a new user based on request data.

        Args:
            request (Request): The HTTP request containing user data in JSON format.

        Returns:
            dict[str, Union[int, str]]: A dictionary containing the status and message of the operation.
        """
        data: dict[str, str] = request.get_json(silent=True) or {}

        required_fields = {
            "email",
            "password",
            "first_name",
            "last_name",
            "phone_number",
            "renter_address",
            "business_sphere",
        }

        missing_fields = required_fields - data.keys()
        if missing_fields:
            return {
                "status": 400,
                "message": f"Missing required fields: {', '.join(missing_fields)}",
            }
        try:
            User.get_by_email(data["email"])
            return {"status": 409, "message": "User with the same email already exists"}
        except UserNotFoundError:
            try:
                created = User.create_renter(
                    role="renter",
                    email=data["email"],
                    password=data["password"],
                    first_name=data["first_name"],
                    last_name=data["last_name"],
                    phone_number=data["phone_number"],
                    renter_address=data["renter_address"],
                    business_sphere=data["business_sphere"],
                )
                if created:
                    return {"status": 201, "message": "User created successfully"}
                else:
                    return {"status": 500, "message": "Failed to create user"}
            except Exception as error:
                logging.error("Error during user creation: %s", error)
                return {"status": 500, "message": "Internal Server Error"}
