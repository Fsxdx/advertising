import os
from dataclasses import dataclass

from flask import current_app, session
from pymysql import OperationalError

from apps.common.database.base_model import BaseModel
from apps.common.database.sql_provider import SQLProvider
from apps.common.database.sql_queries import select_dict
import logging

from apps.common.meta import MetaSQL

logger = logging.getLogger(__name__)


@dataclass
class InfoResponse:
    """
    Data class for holding the response of information requests.

    Attributes:
        result (dict): The fetched product data.
        error_message (str): Error message, if any.
        status (bool): Whether the request was successful or not.
    """
    result: tuple
    error_message: str
    status: bool

class QueryHandler(BaseModel, metaclass=MetaSQL):
    @classmethod
    def process_user_input(cls, input_data: dict) -> InfoResponse:
        print(input_data)
        # TODO: Handle empty input
        sql_query = QueryHandler.sql_provider.get('select_billboard.sql',
                                                  min_price = input_data['min_price'],
                                                  max_price = input_data['max_price'],
                                                  city = input_data['city'],
                                                  min_quality = input_data['min_quality'],
                                                  max_quality = input_data['max_quality'],
                                                  min_size = input_data['min_size'],
                                                  max_size = input_data['max_size'])
        try:
            print(sql_query)
            result = cls.fetch_all(sql_query, current_app.config['db_config'][session['role']])
            if result:
                print(result)
                return InfoResponse(result=result, error_message='', status=True)
            return InfoResponse(result=result, error_message='Nothing could be found', status=False)
        except OperationalError as e:
            logger.error(f"Error code: {e.args[0]}, Error description: {e.args[1]}")
            # raise e
            return InfoResponse(result=dict(), error_message='Bad sql query ', status=False)
