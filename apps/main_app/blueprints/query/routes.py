from flask import render_template, request, session

from .blueprint import query_app
from .models import QueryHandler


@query_app.route("/", methods=["GET"])
def handle_index_query() -> str:
    """
    Handles GET requests for the index page.

    Returns:
        str: Rendered HTML for the index page, including the user role from the session.
    """
    return render_template("query_index.html", role=session.get("role"))


@query_app.route("/billboard_query", methods=["GET"])
def billboard_get_handler() -> str:
    """
    Handles GET requests for the billboard query form.

    Returns:
        str: Rendered HTML for the billboard query form.
    """
    return render_template("billboard_query_form.html", role=session.get("role"))


@query_app.route("/billboard_query", methods=["POST"])
def billboard_post_handler() -> str:
    """
    Handles POST requests for processing a billboard query.

    Processes user input, validates it, executes the query, and returns the results.

    Returns:
        str:
            - Rendered HTML with search results if the query is successful.
            - Rendered HTML with the form and an error message if validation or the query fails.
    """
    user_input = {
        "min_price": request.form.get("min_price", "0"),
        "max_price": request.form.get("max_price", "~0"),
        "city": request.form.get("city", "%"),
        "min_quality": request.form.get("min_quality", "0"),
        "max_quality": request.form.get("max_quality", "~0"),
        "min_size": request.form.get("min_size", "0"),
        "max_size": request.form.get("max_size", "~0"),
    }

    try:
        QueryHandler.check_input(user_input)
    except ValueError as e:
        return render_template(
            "billboard_query_form.html",
            role=session.get("role"),
            error=str(e),
        )

    result = QueryHandler.process_user_input(user_input)

    if result.status:
        return render_template(
            "billboard_query_result.html",
            role=session.get("role"),
            search_results=result.result,
        )
    return render_template(
        "billboard_query_form.html",
        role=session.get("role"),
        error=result.error_message,
    )
