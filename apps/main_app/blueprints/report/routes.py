from flask import render_template, request, session

from .blueprint import report_app
from .models import ReportManager


@report_app.route("/create", methods=["GET"])
def create_get_handler() -> str:
    """
    Handles the GET request for the 'Create Report' page.

    Returns:
        Response: Renders the 'create_report.html' template with the current
        user's role and available scenarios for report creation.
    """
    return render_template(
        "create_report.html",
        role=session.get("role"),
        scenarios=ReportManager.get_scenarios(),
    )


@report_app.route("/create", methods=["POST"])
def create_post_handler() -> str:
    """
    Handles the POST request for creating a new report.

    Processes form data to create a report based on the selected scenario and date.
    Returns a success message if the report is created successfully, otherwise
    returns an error message.

    Returns:
        Response: Renders the 'create_report.html' template with a success
        or error message.
    """
    report_scenario = request.form.get("report_scenario")
    report_date = request.form.get("report_date")

    if not report_scenario or not report_date:
        return render_template(
            "create_report.html",
            role=session.get("role"),
            error="Invalid input: both scenario and date are required.",
            scenarios=ReportManager.get_scenarios(),
        )

    try:
        month, year = map(int, report_date.split("/"))
    except ValueError:
        return render_template(
            "create_report.html",
            role=session.get("role"),
            error="Invalid date format. Please use DD/MM/YYYY.",
            scenarios=ReportManager.get_scenarios(),
        )

    res = ReportManager.create_report(report_scenario, month, year)

    if res == "OK":
        return render_template(
            "create_report.html",
            role=session.get("role"),
            message="Report has been successfully created.",
            scenarios=ReportManager.get_scenarios(),
        )

    return render_template(
        "create_report.html",
        role=session.get("role"),
        error=res,
        scenarios=ReportManager.get_scenarios(),
    )


@report_app.route("/view", methods=["GET"])
def view_get_handler() -> str:
    """
    Handles the GET request for the 'View Report' page.

    Returns:
        Response: Renders the 'view_report_form.html' template with the
        current user's role and available scenarios for viewing reports.
    """
    return render_template(
        "view_report_form.html",
        role=session.get("role"),
        scenarios=ReportManager.get_scenarios(),
    )


@report_app.route("/view", methods=["POST"])
def view_post_handler() -> str:
    """
    Handles the POST request for viewing a report.

    Processes form data to fetch and display a report for a specific scenario
    and date. If the report retrieval fails, displays an error message.

    Returns:
        Response: Renders the 'view_report.html' template with the report data
        if successful, or the 'view_report_form.html' template with an error message.
    """
    report_scenario = request.form.get("report_scenario")
    report_date = request.form.get("report_date")

    if not report_scenario or not report_date:
        return render_template(
            "view_report_form.html",
            role=session.get("role"),
            error="Invalid input: both scenario and date are required.",
            scenarios=ReportManager.get_scenarios(),
        )

    try:
        month, year = map(int, report_date.split("/"))
    except ValueError:
        return render_template(
            "view_report_form.html",
            role=session.get("role"),
            error="Invalid date format. Please use MM/YYYY.",
            scenarios=ReportManager.get_scenarios(),
        )

    res = ReportManager.get_report(report_scenario, month, year)

    if res.status:
        return render_template(
            "view_report.html",
            role=session.get("role"),
            column_names=res.column_names,
            report_data=res.result,
            year=year,
            month=month,
            report_type=res.report_desc,
        )

    return render_template(
        "view_report_form.html",
        role=session.get("role"),
        error=res.error_message,
        scenarios=ReportManager.get_scenarios(),
    )
