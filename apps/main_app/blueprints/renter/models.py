import os
from typing import Optional
from os import path
from flask import session, current_app
from datetime import datetime

from apps.auth.app import db_config
from apps.auth.models import User
from apps.common.database.base_model import BaseModel
from apps.common.meta import MetaSQL


class Renter(BaseModel, metaclass=MetaSQL):

    def __init__(self, renter_id, first_name, last_name, phone_number, address, business_sphere, user_id,
                 img=None) -> None:
        self.renter_id = renter_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.address = address
        self.business_sphere = business_sphere
        self.user_id = user_id

    @classmethod
    def get_by_user_id(cls, user_id: int) -> Optional['Renter']:
        result = cls.fetch_one(Renter.sql_provider.get('get_renter_by_user_id.sql', user_id=user_id),
                               current_app.config['db_config'][session['role']])
        return Renter(*result) if result else None


class Billboard(BaseModel, metaclass=MetaSQL):
    def __init__(self, billboard_id, price_per_month, size, billboard_address, mount_date, quality, owner_id):
        self.billboard_id = billboard_id
        self.price_per_month = price_per_month
        self.size = size
        self.billboard_address = billboard_address
        self.mount_date = mount_date
        self.quality = quality
        self.owner_id = owner_id
        self.img_path = f"img/{self.billboard_id}.jpg" if path.isfile(
            path.join(path.dirname(__file__), f'static/img/{self.billboard_id}.jpg')) else None

    @classmethod
    def get_billboard(cls, billboard_id):
        result = cls.fetch_one(Billboard.sql_provider.get('get_billboard.sql', billboard_id=billboard_id), current_app.config['db_config'][session['role']])
        if result:
            return Billboard(*result)
        return result

    @classmethod
    def get_random_billboards(cls, count) -> list['Billboard']:
        result = cls.fetch_all(Billboard.sql_provider.get('get_n_random_billboards.sql', n=count),
                               db_config=current_app.config['db_config'][session['role']])
        return list(map(lambda x: Billboard(*x), result))

    def get_occupied_periods(self):
        result = self.fetch_all(Billboard.sql_provider.get('get_occupied_periods.sql', billboard_id=self.billboard_id),
                                current_app.config['db_config'][session['role']])
        if result:
            return list(map(lambda x:
                            {'start': {'month': x[0], 'year': x[1]},
                             'end': {'month': x[2], 'year': x[3]}},
                            result))
        return result


class OrderHandler(BaseModel, metaclass=MetaSQL):
    @classmethod
    def save_order_row_in_cart(cls, billboard_id, start_month, start_year, end_month, end_year):
        if 'cart' not in session:
            session['cart'] = []
        session['cart'].append({
            "billboard_id": billboard_id,
            "start_month": int(start_month),
            "start_year": int(start_year),
            "end_month": int(end_month),
            "end_year": int(end_year),
        })
        session['cart'] = session['cart']  # ????????


class CheckoutHandler(BaseModel, metaclass=MetaSQL):
    @classmethod
    def checkout(cls, order_rows: dict):
        def get_price(price_per_month, start_month, start_year, end_month, end_year):
            return price_per_month * ((end_year - start_year) * 12 + (end_month - start_month + 1))

        prices = [get_price(
            Billboard.get_billboard(order['billboard_id']).price_per_month,
            order['start_month'],
            order['start_year'],
            order['end_month'],
            order['end_year']
        )
            for order in session['cart']]

        with CheckoutHandler.transaction() as cursor:
            order_id = cls.insert(CheckoutHandler.sql_provider.get(
                'add_order.sql',
                registration_date=datetime.now().date(),
                total_cost=sum(prices),
                renter_id=Renter.get_by_user_id(session['user_id']).renter_id
            ),
                current_app.config['db_config'][session['role']],
                cursor=cursor
            )
            for order_row, price in zip(order_rows, prices):
                cls.insert(CheckoutHandler.sql_provider.get(
                    'add_order_row.sql',
                    start_year=order_row['start_year'],
                    start_month=order_row['start_month'],
                    end_year=order_row['end_year'],
                    end_month=order_row['end_month'],
                    price=price,
                    order_id=order_id,
                    billboard_id=order_row['billboard_id']
                ),
                    current_app.config['db_config'][session['role']],
                    cursor=cursor
                )
        session['cart'] = []
