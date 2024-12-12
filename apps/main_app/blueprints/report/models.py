import json
import logging
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from flask import current_app, session
from pymysql import OperationalError

from apps.common.database.base_model import BaseModel
from apps.common.database.sql_provider import SQLProvider
from apps.common.meta import MetaSQL

logger = logging.getLogger(__name__)


@dataclass
class ReportResponse:
    """
    Represents the response from a report generation or retrieval operation.

    Attributes:
        error_message (str): Error message in case of failure.
        status (bool): Whether the operation was successful.
        column_names (Optional[List[str]]): Names of the columns in the report.
        report_desc (Optional[str]): description of the report.
        result (Optional[Tuple[Tuple, ...]]): The fetched report data.
    """

    error_message: str
    status: bool
    column_names: Optional[List[str]] = field(default=None)
    report_desc: Optional[str] = field(default=None)
    result: Optional[Tuple[Tuple[str, ...], ...]] = field(default=None)


class ReportManager(BaseModel, metaclass=MetaSQL):
    """
    Handles the creation and retrieval of reports.

    Attributes:
        report_config (dict): Configuration for available report scenarios.
        sql_provider(SQLProvider): SQLProvider instance.
    """
    sql_provider: SQLProvider
    try:
        with open("apps/main_app/data/report_config.json", "r") as file:
            report_config = json.load(file)
    except FileNotFoundError:
        report_config = {}

    @classmethod
    def create_report(cls, report_type: str, month: int, year: int) -> str:
        """
        Generates a report by calling a stored procedure.

        Args:
            report_type (str): The type of report to create.
            month (int): The month for the report.
            year (int): The year for the report.

        Returns:
            str: The status message or result of the procedure.
        """
        try:
            result = cls.call_procedure(
                cls.report_config[report_type]["procedure_name"],
                current_app.config["db_config"][session["role"]],
                year,
                month,
            )
            logger.info(f"Report created successfully: {result}")
            return result[0][0] if result else "Error has occurred"
        except Exception as e:
            logger.error(f"Failed to create report: {e}")
            return "Error has occurred"

    @classmethod
    def get_report(cls, report_type: str, month: int, year: int) -> ReportResponse:
        """
        Retrieves a report from the database.

        Args:
            report_type (str): The type of report to retrieve.
            month (int): The month for the report.
            year (int): The year for the report.

        Returns:
            ReportResponse: Contains the report data, column names, and status.
        """
        try:
            sql_query = cls.sql_provider.get(
                "get_report.sql",
                year=year,
                month=month,
                db_columns=", ".join(cls.report_config[report_type]["db_columns"]),
                table=cls.report_config[report_type]["table"],
            )
            result = cls.fetch_all(
                sql_query, current_app.config["db_config"][session["role"]]
            )
            if result:
                return ReportResponse(
                    column_names=cls.report_config[report_type][
                        "displayable_column_names"
                    ],
                    result=result,
                    error_message="",
                    report_desc=cls.report_config[report_type]["desc"],
                    status=True,
                )
            logger.warning("Report not found for the selected period.")
            return ReportResponse(
                error_message="Report for selected period has not been created",
                status=False,
            )
        except OperationalError as e:
            logger.error(f"Database error: {e.args[0]} - {e.args[1]}")
            return ReportResponse(error_message="Try again later", status=False)
        except KeyError as e:
            logger.error(f"Invalid report type: {e}")
            return ReportResponse(error_message="Invalid report type", status=False)

    @classmethod
    def get_scenarios(cls) -> List[Tuple[str, str]]:
        """
        Fetches available report scenarios.

        Returns:
            List[Tuple[str, str]]: A list of report type names and descriptions.
        """
        return [(name, data["desc"]) for name, data in cls.report_config.items()]
