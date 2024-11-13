from pymysql import ProgrammingError
from os import path

from apps.common.wrappers import login_required
from flask import render_template, request, render_template_string, redirect, current_app, session, url_for
from .models import Billboard, OrderHandler, CheckoutHandler
from . import renter_app


@renter_app.route('/<int:billboard_id>', methods=["GET"])
@login_required
def get_billboard_details(billboard_id):
    print(session)
    billboard = Billboard.get_billboard(billboard_id)
    if billboard:
        return render_template('billboard_details.html',
                               billboard=billboard,
                               occupied_periods=billboard.get_occupied_periods(),
                               is_auth='user_id' in session)  # path.join(path.dirname(__file__), rf"data\img\{billboard_id}.jpg"))
    else:
        return "Billboard not found", 404


@renter_app.route('/<int:billboard_id>', methods=["POST"])
@login_required
def add_billboard_to_cart(billboard_id):
    print('aaaaaaaaaaaaaaaaa')
    OrderHandler.save_order_row_in_cart(billboard_id,
                                        *request.form['start_date'].split('/'),
                                        *request.form['end_date'].split('/'))
    return render_template_string('ok')


@renter_app.route('/cart', methods=["GET"])
@login_required
def cart_handler():
    return render_template('cart.html', cart_items=[
        {**order, 'price_per_month': Billboard.get_billboard(order['billboard_id']).price_per_month}
        for order in session.get('cart', [])
    ])


@renter_app.route('/checkout', methods=["POST"])
@login_required
def checkout_handler():
    CheckoutHandler.checkout(session['cart'])
    return render_template_string('ok')


@renter_app.route('/remove-from-cart', methods=["POST"])
@login_required
def remove_billboard_from_cart():
    session['cart'].pop(int(request.form['order_id']))
    session['cart'] = session['cart']  # ???????????
    return redirect(url_for('renter.cart_handler'))