from pymysql import ProgrammingError
from os import path

from apps.common.wrappers import login_required, role_required
from flask import render_template, request, render_template_string, redirect, current_app, session, url_for
from .models import Billboard, OrderHandler, CheckoutHandler
from . import renter_app
from flask import make_response


@renter_app.route('/<int:billboard_id>', methods=["GET"])
def get_billboard_details(billboard_id):
    billboard = Billboard.get_billboard(billboard_id)
    if billboard:
        print(billboard.get_occupied_periods())
        return render_template('billboard_details.html',
                               billboard=billboard,
                               occupied_periods=billboard.get_occupied_periods(),
                               is_auth='user_id' in session)
    else:
        return "Billboard not found", 404


@renter_app.route('/<int:billboard_id>', methods=["POST"])
def add_billboard_to_cart(billboard_id):
    billboard = Billboard.get_billboard(billboard_id)
    try:
        OrderHandler.check_input(request.form['start_date'], request.form['end_date'], billboard)
    except ValueError as e:
        return render_template('billboard_details.html',
                        billboard=billboard,
                        occupied_periods=billboard.get_occupied_periods(),
                        error=e.args[0],
                        is_auth='user_id' in session)

    OrderHandler.save_order_row_in_cart(billboard_id,
                                        *request.form['start_date'].split('/'),
                                        *request.form['end_date'].split('/'))
    return render_template('success_cart_add.html')


@renter_app.route('/cart', methods=["GET"])
def cart_handler():
    items = [
        {**order, 'price_per_month': Billboard.get_billboard(order['billboard_id']).price_per_month}
        for order in session.get('cart', [])
    ]
    return render_template('cart.html', cart_items=items,
                           total=sum(map(lambda item: ((item['end_year'] - item['start_year']) * 12 + (
                                       item['end_month'] - item['start_month'] + 1)) * item['price_per_month'], items)))


@renter_app.route('/checkout', methods=["POST"])
def checkout_handler():
    try:
        CheckoutHandler.checkout(session['cart'])
        return render_template('success_order.html')
    except ProgrammingError:
        return render_template_string('ok')


@renter_app.route('/remove-from-cart', methods=["POST"])
def remove_billboard_from_cart():
    session['cart'].pop(int(request.form['order_id']))
    session['cart'] = session['cart']  # ???????????
    return redirect(url_for('renter.cart_handler'))
