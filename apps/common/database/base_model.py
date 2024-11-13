from contextlib import contextmanager
from pymysql import OperationalError, connect
from pymysql.cursors import Cursor
from .db_manager import DBContextManager
from flask import current_app, session
from pymysql.connections import Connection
from typing import Generator, Optional


class BaseModel:
    """Base model to provide utility methods for database interaction."""

    @classmethod
    def execute_query(cls, query: str, db_config, cursor: Optional[Cursor] = None) -> Cursor:
        """Executes a query on the database.

        Args:
            query (str): SQL query to be executed.
            cursor (Optional[Cursor], optional): Existing database cursor to use. Defaults to None.

        Returns:
            Cursor: The cursor after the query is executed.

        Raises:
            OperationalError: If the cursor could not be created.
        """
        if cursor:
            cursor.execute(query)
            return cursor
        else:
            with DBContextManager(db_config) as cursor:
                if cursor is None:
                    raise OperationalError(
                        "Cursor could not be created.")  # Lost info about error because was catched inside __enter__
                cursor.execute(query)
                return cursor

    @classmethod
    def fetch_all(cls, query: str, db_config, cursor: Optional[Cursor] = None) -> tuple:
        """Fetches all results from a query.

        Args:
            query (str): SQL query to fetch results.
            cursor (Optional[Cursor], optional): Existing database cursor to use. Defaults to None.

        Returns:
            list: A list of rows fetched from the database.
        """
        cursor = cls.execute_query(query, db_config, cursor)
        return cursor.fetchall()

    @classmethod
    def fetch_one(cls, query: str, db_config, cursor: Optional[Cursor] = None) -> Optional[tuple]:
        """Fetches one result from a query.

        Args:
            query (str): SQL query to fetch a result.
            cursor (Optional[Cursor], optional): Existing database cursor to use. Defaults to None.

        Returns:
            Optional[tuple]: A single row fetched from the database, or None if no result.
        """
        cursor = cls.execute_query(query, db_config, cursor)
        return cursor.fetchone()

    @classmethod
    def insert(cls, query: str, db_config, cursor: Optional[Cursor] = None) -> int:
        """Inserts a new record into the database.

        Args:
            query (str): SQL query to insert a new record.
            cursor (Optional[Cursor], optional): Existing database cursor to use. Defaults to None.

        Returns:
            int: The ID of the last inserted row.
        """
        cursor = cls.execute_query(query, db_config, cursor)
        return cursor.lastrowid

    @classmethod
    def call_procedure(cls, procedure_name: str, db_config, *params, cursor: Optional[Cursor] = None) -> tuple:
        """Calls a stored procedure and fetches its output.

        Args:
            procedure_name (str): The name of the stored procedure to call.
            *params: The parameters to pass to the stored procedure.
            cursor (Optional[Cursor], optional): Existing database cursor to use. Defaults to None.

        Returns:
            tuple: The result set returned by the procedure.

        Raises:
            OperationalError: If the cursor could not be created.
        """
        if cursor:
            cursor.callproc(procedure_name, params)
            return cursor.fetchall()
        else:
            with DBContextManager(db_config) as cursor:
                if cursor is None:
                    raise OperationalError("Cursor could not be created.")
                cursor.callproc(f"Advertising.{procedure_name}", params)
                return cursor.fetchall()

    @classmethod
    @contextmanager
    def transaction(cls, db_config) -> Generator[Cursor, None, None]:
        """Manages a database transaction.

        Yields:
            Generator[Cursor, None, None]: A database cursor within a transaction.

        Raises:
            Exception: If an error occurs during the transaction, it will rollback the changes.
        """
        db_manager = DBContextManager(db_config)
        db_manager.connector: Connection = connect(**db_config)
        cursor = db_manager.connector.cursor()
        try:
            yield cursor
            db_manager.connector.commit()
        except Exception as e:
            db_manager.connector.rollback()
            raise e
        finally:
            cursor.close()
            db_manager.connector.close()
