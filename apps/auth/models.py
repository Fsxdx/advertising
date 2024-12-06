import logging
from typing import Optional, Union

from flask import Request, current_app
from pymysql import ProgrammingError
from werkzeug.security import check_password_hash

from apps.auth.exceptions import UserNotFoundError
from apps.auth.utils import decode_basic_authorization, is_auth_request_valid
from apps.common.database.base_model import BaseModel
from apps.common.meta import MetaSQL


class User(BaseModel, metaclass=MetaSQL):
    """Represents a user and provides methods to interact with user-related database operations."""

    def __init__(self, user_id: int, role: str, email: str, password: str):
        """
        Initializes a User instance.

        Args:
            user_id (int): Unique identifier for the user.
            role (str): Role assigned to the user (e.g., 'renter', 'admin').
            email (str): User's email address.
            password (str): Hashed password of the user.
        """
        self.user_id = user_id
        self.role = role
        self.email = email
        self.password = password

    @classmethod
    def get_by_id(cls, user_id: int) -> Optional["User"]:
        """Fetches a user by their unique user_id.

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
            return User(*result)
        raise UserNotFoundError("Could not find user by user_id.")

    @classmethod
    def get_by_email(cls, email: str) -> Optional["User"]:
        """Fetches a user by their email address.

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
            return User(*result)
        raise UserNotFoundError("Could not find user by email.")

    @classmethod
    def create_renter(cls, role: str, email: str, password: str, **kwargs) -> bool:
        """Creates a new renter user in the database.

        Args:
            role (str): Role of the user (should be 'renter').
            email (str): Email address of the renter.
            password (str): Hashed password for the renter.
            **kwargs: Additional user-specific attributes to be stored.

        Returns:
            bool: True if the renter is successfully created, False otherwise.
        """
        if role != "renter":
            raise ValueError("Role must be 'renter' when creating a renter.")
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

    def check_password(self, password: str) -> bool:
        """Checks whether the provided password matches the user's stored hashed password.

        Args:
            password (str): The plain text password to verify.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return check_password_hash(self.password, password)


class AuthManager(BaseModel, metaclass=MetaSQL):
    @classmethod
    def get_user(cls, request: Request) -> dict[str, Union[int | str]]:
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
    def register_user(cls, request: Request):
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
            # Check if a user with the provided email already exists
            User.get_by_email(data["email"])
            return {"status": 409, "message": "User with the same email already exists"}
        except UserNotFoundError:
            # Proceed with user creation
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
