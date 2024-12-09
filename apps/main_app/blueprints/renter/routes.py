from flask import redirect, render_template, request, session, url_for
from pymysql import ProgrammingError
from werkzeug import Response

from .blueprint import renter_app
from .models import Billboard, CheckoutHandler, OrderHandler


@renter_app.route("/<int:billboard_id>", methods=["GET"])
def get_billboard_details(billboard_id: int) -> str:
    """
    Handle GET requests to display billboard rental details.

    Args:
        billboard_id (int): The ID of the billboard to retrieve.

    Returns:
        str: Rendered HTML for the billboard details page, or an error page if the billboard is not found.
    """
    try:
        billboard = Billboard.get_billboard(billboard_id)
        return render_template(
            "billboard_details.html",
            billboard=billboard,
            occupied_periods=billboard.get_occupied_periods(),
            is_auth="user_id" in session,
        )
    except ValueError:
        return render_template("billboard_not_found.html")


@renter_app.route("/<int:billboard_id>", methods=["POST"])
def add_billboard_to_cart(billboard_id: int) -> str:
    """
    Handle POST requests to add a billboard rental to the cart.

    Validates the rental dates and adds the billboard to the cart.

    Args:
        billboard_id (int): The ID of the billboard to add to the cart.

    Returns:
        str: Rendered HTML indicating success or failure of adding to the cart.
    """
    try:
        billboard = Billboard.get_billboard(billboard_id)
    except ValueError:
        return render_template("billboard_not_found.html")

    try:
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        OrderHandler.check_input(start_date, end_date, billboard)
    except ValueError as e:
        return render_template(
            "billboard_details.html",
            billboard=billboard,
            occupied_periods=billboard.get_occupied_periods(),
            error=str(e),
            is_auth="user_id" in session,
        )

    start_year, start_month = map(int, start_date.split("/"))
    end_year, end_month = map(int, end_date.split("/"))

    OrderHandler.save_order_row_in_cart(
        billboard_id, start_year, start_month, end_year, end_month
    )
    return render_template("success_cart_add.html")


@renter_app.route("/cart", methods=["GET"])
def cart_handler() -> str:
    """
    Handle GET requests to display the user's shopping cart.

    Retrieves cart items from the session and calculates the total.

    Returns:
        str: Rendered HTML for the cart page with item details and total cost.
    """
    items = OrderHandler.get_cart()
    total_cost = OrderHandler.get_total_cost(items)

    return render_template(
        "cart.html",
        cart_items=items,
        total=total_cost,
    )


@renter_app.route("/checkout", methods=["POST"])
def checkout_handler() -> str:
    """
    Handle POST requests to process the checkout.

    Finalizes the cart into an order and saves it to the database.

    Returns:
        str: Rendered HTML for the success page or cart page with errors.
    """
    try:
        CheckoutHandler.checkout(session.get("cart", []))
        return render_template("success_order.html")
    except ValueError as e:
        items = OrderHandler.get_cart()
        total_cost = OrderHandler.get_total_cost(items)
        return render_template(
            "cart.html",
            cart_items=items,
            error=str(e),
            total=total_cost,
        )
    except ProgrammingError:
        return render_template("cart.html", error="Database error occurred during checkout.")


@renter_app.route("/remove-from-cart", methods=["POST"])
def remove_billboard_from_cart() -> str | Response:
    """
    Handle POST requests to remove an item from the cart.

    Removes the specified order from the session cart.

    Returns:
        str: Redirects to the cart handler page.
    """
    try:
        order_id = int(request.form["order_id"])
        session["cart"].pop(order_id)
        session.modified = True  # Explicitly mark session as modified
    except (KeyError, ValueError, IndexError):
        return render_template("cart.html", error="Failed to remove item from cart.")

    return redirect(url_for("renter.cart_handler"))
