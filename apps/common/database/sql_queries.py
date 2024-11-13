from typing import Tuple, Dict, List
from pymysql.err import OperationalError
from .db_manager import DBContextManager
import logging

logger = logging.getLogger(__name__)


def select_list(db_config: dict, sql: str) -> Tuple[Tuple[Tuple], Tuple[Tuple]]:
    """
    Executes a SQL query and returns a list of results.

    Args:
        db_config (dict): Database configuration.
        sql (str): SQL query to execute.

    Returns:
        tuple: Result set as a list of tuples and the description (column names).

    Raises:
        OperationalError: If an error occurs during query execution.
    """
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise OperationalError("Cursor could not be created.")
        cursor.execute(sql)
        result = cursor.fetchall()
        return result, cursor.description

def select_dict(db_config: dict, sql: str) -> List[Dict[str, str]]:
    """
    Executes a SQL query and returns the results as a list of dictionaries.

    Args:
        db_config (dict): Database configuration.
        sql (str): SQL query to execute.

    Returns:
        list: A list of dictionaries where each dictionary represents a row with column names as keys.
    """
    result, schema = select_list(db_config, sql)

    # Convert result set to a list of dictionaries
    return list(map(lambda x: dict(zip(list(map(lambda y: y[0], schema)), x)), result))
