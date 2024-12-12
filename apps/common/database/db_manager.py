import logging
from types import TracebackType
from typing import Any, Optional, Type

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

        Returns:
            pymysql.cursors.Cursor or None
        """
        try:
            self.connector = connect(
                host=self.db_config['host'],
                user=self.db_config['user'],
                password=self.db_config['password'],
                database=self.db_config['database']
            )
            # if self.connector is None:
            #     raise OperationalError("Couldn't establish a database connection.")
            self.cursor = self.connector.cursor()
            return self.cursor
        except OperationalError as e:
            logger.error(f"Error code: {e.args[0]}, Error description: {e.args[1]}")
            return None

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> Optional[bool]:
        """
        Exit method to close the cursor and connection and handle exceptions.

        If an exception occurred, the transaction is rolled back; otherwise, it's committed.
        """
        if self.cursor and self.connector:
            if exc_type:
                self.connector.rollback()
            else:
                self.connector.commit()
            self.cursor.close()
            self.connector.close()

        # if exc_type:
        #     raise OperationalError(exc_type, exc, traceback)

        return True
