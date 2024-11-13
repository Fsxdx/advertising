from flask import render_template, render_template_string, request
from . import report_app
from .models import ReportManager


@report_app.route('/create', methods=["GET"])
def create_get_handler():
    return render_template('create_report.html', scenarios=ReportManager.get_scenarios())


@report_app.route('/create', methods=["POST"])
def create_post_handler():
    res = ReportManager.create_report(request.form['report_scenario'],
                                      *request.form['report_date'].split('/'))
    print(res)
    if res == 'OK':
        return render_template("create_report.html", message="Report has been successfully created",
                               scenarios=ReportManager.get_scenarios())
    return render_template('create_report.html', error=res, scenarios=ReportManager.get_scenarios())


@report_app.route('/view', methods=["GET"])
def view_get_handler():
    return render_template('view_report_form.html', scenarios=ReportManager.get_scenarios())


@report_app.route('/view', methods=["POST"])
def view_post_handler():
    res = ReportManager.get_report(request.form['report_scenario'],
                                   *request.form['report_date'].split('/'))
    if res.status:
        return render_template("view_report.html", column_names=res.column_names, report_data=res.result)

    return render_template('view_report_form.html', error=res.error_message, scenarios=ReportManager.get_scenarios())
