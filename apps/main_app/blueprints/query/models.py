import logging
from dataclasses import dataclass
from typing import Any, Dict, Tuple

from flask import current_app, session
from pymysql import OperationalError

from apps.common.database.base_model import BaseModel
from apps.common.database.sql_provider import SQLProvider
from apps.common.meta import MetaSQL

logger = logging.getLogger(__name__)


@dataclass
class InfoResponse:
    """
    Data class for holding the response of query requests.

    Attributes:
        result (Tuple[Any, ...]): The fetched data as a tuple of rows.
        error_message (str): Error message, if any.
        status (bool): Indicates whether the request was successful or not.
    """

    result: Tuple[Any, ...]
    error_message: str
    status: bool


class QueryHandler(BaseModel, metaclass=MetaSQL):
    """Handles database queries and processes user input for fetching information."""
    sql_provider: SQLProvider

    @classmethod
    def check_input(cls, input_data: Dict[str, str]) -> bool:
        """
        Validates user input to ensure proper formatting.

        Args:
            input_data (Dict[str, str]): Dictionary containing input data

        Returns:
            bool: True if the input data is valid.

        Raises:
            ValueError: If a non-numeric value is found in a numeric field.
        """
        for key, value in input_data.items():
            if key != "city" and not value.isdigit() and value != "~0":
                raise ValueError(
                    f"Non-numeric value found in field {key}: '{value.capitalize()}'"
                )
        return True

    @classmethod
    def process_user_input(cls, input_data: Dict[str, str]) -> InfoResponse:
        """
        Processes user input to generate and execute an SQL query.

        Args:
            input_data (Dict[str, str]): Dictionary containing input parameters for filtering results

        Returns:
            InfoResponse: Contains the query result, error message, and status.
        """
        sql_query = QueryHandler.sql_provider.get(
            "select_billboard.sql",
            min_price=input_data["min_price"],
            max_price=input_data["max_price"],
            city=input_data["city"],
            min_quality=input_data["min_quality"],
            max_quality=input_data["max_quality"],
            min_size=input_data["min_size"],
            max_size=input_data["max_size"],
        )
        try:
            logger.debug(f"Executing SQL query: {sql_query}")
            result = cls.fetch_all(
                sql_query, current_app.config["db_config"][session["role"]]
            )
            if result:
                logger.info("Query executed successfully, results found.")
                return InfoResponse(result=result, error_message="", status=True)

            logger.warning("Query executed, but no results found.")
            return InfoResponse(
                result=tuple(), error_message="Nothing could be found", status=False
            )
        except OperationalError as e:
            logger.error(
                f"SQL Operational Error - Code: {e.args[0]}, Description: {e.args[1]}"
            )
            return InfoResponse(
                result=tuple(), error_message="Bad SQL query", status=False
            )
