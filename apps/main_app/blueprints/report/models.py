import dataclasses
import json
import logging
from dataclasses import dataclass, fields, field

from flask import render_template_string, render_template, current_app, session
from pymysql import OperationalError
from apps.common.database.base_model import BaseModel
from apps.common.meta import MetaSQL

logger = logging.getLogger(__name__)


@dataclass
class ReportResponse:
    """
    Data class for holding the response of report requests.

    Attributes:
        column_names (list): Names of the columns.
        result (tuple[tuple, ...]): The fetched report data.
        error_message (str): Error message, if any.
        status (bool): Whether the request was successful or not.
    """
    error_message: str
    status: bool
    column_names: list = field(default=None)
    result: tuple[tuple, ...] = field(default=None)


class ReportManager(BaseModel, metaclass=MetaSQL):
    with open('data/report_config.json', 'r') as file:
        report_config = json.load(file)

    @classmethod
    def create_report(cls, report_type, month, year) -> str:
        result = cls.call_procedure(cls.report_config[report_type]['procedure_name'], current_app.config['db_config'][session['role']], year, month)
        print(result)
        return result[0][0] if result else "Error has occurred"

    @classmethod
    def get_report(cls, report_type, month, year) -> ReportResponse:
        sql_query = cls.sql_provider.get("get_report.sql", year=year, month=month,
                                         table=cls.report_config[report_type]['table'])
        try:
            result = cls.fetch_all(sql_query, current_app.config['db_config'][session['role']])
            if result:
                return ReportResponse(column_names=cls.report_config[report_type]['displayable_column_names'],
                                      result=result,
                                      error_message='',
                                      status=True)
            return ReportResponse(error_message="Report for selected period has not been created", status=False)
        except OperationalError as e:
            logger.error(f"Error code: {e.args[0]}, Error description: {e.args[1]}")
            # raise e
            return ReportResponse(error_message='Try again later', status=False)

    @classmethod
    def get_scenarios(cls):
        return [(name, data['desc']) for name, data in cls.report_config.items()]
