import logging
from typing import Any

import pymysql
from pymysql import connect
from pymysql.err import OperationalError

logger = logging.getLogger(__name__)


class DBContextManager:
    """
    A context manager for managing database connections.

    Handles opening and closing the connection and cursor automatically.

    Args:
        db_config (dict): Database configuration.
    """

    def __init__(self, db_config: dict[str, str]):
        self.connector: pymysql.connections.Connection[Any] | None = None
        self.cursor: pymysql.cursors.Cursor | None = None
        self.db_config: dict[str, str] = db_config

    def __enter__(self) -> pymysql.cursors.Cursor | None:
        """
        Establishes a database connection and returns a cursor for executing queries.

        The method attempts to establish a connection to the database using the provided configuration.
        If successful, it returns a database cursor. If an error occurs during the connection process,
        it logs the error message with the error code and description but does not propagate the error.

        Returns
        -------
        pymysql.cursors.Cursor or None
            The cursor object for executing SQL queries if the connection is successful.
            Returns None if the connection fails.

        """
        try:
            self.connector = connect(**self.db_config)
            self.cursor = self.connector.cursor()
            if self.cursor is None:
                raise OperationalError("Couldn't establish a database connection.")
            return self.cursor
        except OperationalError as e:
            logger.error(f"Error code: {e.args[0]}, Error description: {e.args[1]}")
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit method to close the cursor and connection and handle exceptions.

        If an exception occurred, the transaction is rolled back; otherwise, it's committed.
        """
        if self.cursor:
            if exc_type:
                self.connector.rollback()  # Roll back the transaction on error
            else:
                self.connector.commit()  # Commit the transaction on success
            self.cursor.close()
            self.connector.close()

        if exc_type:
            raise OperationalError(exc_type, exc_val, exc_tb)

        return True
