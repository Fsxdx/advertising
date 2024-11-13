import os.path
from flask import session, current_app
from werkzeug.security import check_password_hash
from apps.common.database.base_model import BaseModel
from typing import Optional, Union
from apps.common.meta import MetaSQL


class User(BaseModel, metaclass=MetaSQL):
    """Represents a user and provides methods to interact with user-related database operations."""

    def __init__(self, user_id: int, role: str, email: str, password: str):
        """
        Args:
            user_id (int): ID of the user.
            role (str): Role of the user (e.g., 'renter').
            email (str): Email address of the user.
            password (str): Hashed password of the user.
        """

        self.user_id = user_id
        self.role = role
        self.email = email
        self.password = password

    @classmethod
    def get_by_id(cls, user_id: int) -> Optional['User']:
        """Fetches a user by user_id.

        Args:
            user_id (int): user_id of the user to be fetched.

        Returns:
            Optional[User]: A `User` instance if found, or None otherwise.
        """
        result = cls.fetch_one(User.sql_provider.get('get_user_by_id.sql', user_id=user_id),
                               current_app.config['db_config'])
        return User(*result) if result else None

    @classmethod
    def get_by_email(cls, email: str) -> Optional['User']:
        """Fetches a user by their email address.

        Args:
            email (str): Email address of the user to be fetched.

        Returns:
            Optional[User]: A `User` instance if found, or None otherwise.
        """
        result = cls.fetch_one(User.sql_provider.get('get_user_by_email.sql', email=email), current_app.config['db_config'])
        return User(*result) if result else None

    @classmethod
    def create_renter(cls, role: str, email: str, password: str, **kwargs) -> None:
        """Creates a new renter and adds associated user information in the database.

        Args:
            role (str): The role of the user (should be 'renter').
            email (str): Email address of the new renter.
            password (str): Hashed password of the new renter.
            **kwargs: Additional user data to insert into the renter table.
        """
        with User.transaction() as cursor:
            user_id = cls.insert(User.sql_provider.get(
                'add_user.sql',
                role=role,
                email=email,
                password=password,
                cursor=cursor
            ),
                current_app.config['db_config'],
                cursor=cursor)

            cls.insert(User.sql_provider.get(
                f'add_{role}.sql',
                user_id=user_id,
                **kwargs
            ),
                current_app.config['db_config'],
                cursor=cursor)

    def check_password(self, password: str) -> bool:
        """Verifies the user's password.

        Args:
            password (str): Plain text password to check.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return check_password_hash(self.password, password)
