from contextlib import contextmanager
from typing import Any, Generator, Optional, Union

from pymysql import OperationalError, connect
from pymysql.connections import Connection
from pymysql.cursors import Cursor

from .db_manager import DBContextManager


class BaseModel:
    """Base model providing utility methods for interacting with the database."""

    @classmethod
    def execute_query(
        cls, query: str, db_config: dict[str, Any], cursor: Optional[Cursor] = None
    ) -> Cursor:
        """Executes a SQL query.

        Args:
            query (str): The SQL query to execute.
            db_config (dict[str, Any]): Database configuration.
            cursor (Optional[Cursor], optional): Reusable database cursor. Defaults to None.

        Returns:
            Cursor: The cursor after executing the query.

        Raises:
            OperationalError: If the query fails or the cursor cannot be created.
        """
        if cursor:
            cursor.execute(query)
            return cursor
        with DBContextManager(db_config) as context_cursor:
            if context_cursor is None:
                raise OperationalError("Failed to create a database cursor.")
            context_cursor.execute(query)
            return context_cursor

    @classmethod
    def fetch_all(
        cls, query: str, db_config: dict[str, Any], cursor: Optional[Cursor] = None
    ) -> tuple[tuple[str, ...], ...]:
        """Fetches all results from a SQL query.

        Args:
            query (str): SQL query to fetch results.
            db_config (dict[str, Any]): Database configuration.
            cursor (Optional[Cursor], optional): Reusable database cursor. Defaults to None.

        Returns:
            tuple[tuple, ...]: A tuple of rows fetched from the database.
        """
        cursor = cls.execute_query(query, db_config, cursor)
        return cursor.fetchall()

    @classmethod
    def fetch_one(
        cls, query: str, db_config: dict[str, Any], cursor: Optional[Cursor] = None
    ) -> Optional[tuple[str, ...]]:
        """Fetches a single result from a SQL query.

        Args:
            query (str): SQL query to fetch a single result.
            db_config (dict[str, Any]): Database configuration.
            cursor (Optional[Cursor], optional): Reusable database cursor. Defaults to None.

        Returns:
            Optional[tuple]: A single row fetched from the database, or None if no result.
        """
        cursor = cls.execute_query(query, db_config, cursor)
        return cursor.fetchone()

    @classmethod
    def insert(
        cls, query: str, db_config: dict[str, Any], cursor: Optional[Cursor] = None
    ) -> int:
        """Inserts a new record into the database and returns the last inserted ID.

        Args:
            query (str): SQL query to insert a new record.
            db_config (dict[str, Any]): Database configuration.
            cursor (Optional[Cursor], optional): Reusable database cursor. Defaults to None.

        Returns:
            int: The ID of the last inserted row.
        """
        cursor = cls.execute_query(query, db_config, cursor)
        return cursor.lastrowid

    @classmethod
    def call_procedure(
        cls,
        procedure_name: str,
        db_config: dict[str, Any],
        *params: Union[str, int, float],
        cursor: Optional[Cursor] = None,
    ) -> tuple[tuple[str, ...], ...]:
        """Calls a stored procedure in the database.

        Args:
            procedure_name (str): Name of the stored procedure.
            db_config (dict[str, Any]): Database configuration.
            *params (Union[str, int, float]): Parameters to pass to the procedure.
            cursor (Optional[Cursor], optional): Reusable database cursor. Defaults to None.

        Returns:
            tuple[tuple, ...]: Results fetched from the procedure.

        Raises:
            OperationalError: If the procedure execution fails or the cursor cannot be created.
        """
        if cursor:
            cursor.callproc(procedure_name, params)
            return cursor.fetchall()
        with DBContextManager(db_config) as context_cursor:
            if context_cursor is None:
                raise OperationalError("Failed to create a database cursor.")
            context_cursor.callproc(procedure_name, params)
            return context_cursor.fetchall()

    @classmethod
    @contextmanager
    def transaction(cls, db_config: dict[str, Any]) -> Generator[Cursor, None, None]:
        """Manages a database transaction.

        Args:
            db_config (dict[str, Any]): Database configuration.

        Yields:
            Generator[Cursor, None, None]: A cursor for executing queries within the transaction.

        Raises:
            Exception: Rolls back the transaction in case of any error.
        """
        connection: Connection = connect(**db_config)
        cursor: Cursor = connection.cursor()
        try:
            yield cursor
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()
            connection.close()
