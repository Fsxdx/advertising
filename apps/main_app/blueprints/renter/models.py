from datetime import datetime
from os import path
from typing import Any, Dict, List, Optional, Type

from flask import current_app, session

from apps.common.database.base_model import BaseModel
from apps.common.meta import MetaSQL


class Renter(BaseModel, metaclass=MetaSQL):
    """
    Represents a renter and their associated data.

    Attributes:
        renter_id (int): Unique ID of the renter.
        first_name (str): First name of the renter.
        last_name (str): Last name of the renter.
        phone_number (str): Contact number of the renter.
        address (str): Address of the renter.
        business_sphere (str): Business sphere of the renter.
        user_id (int): Associated user ID.
        img (Optional[str]): Path to the renter's image.
    """

    def __init__(
        self,
        renter_id: int,
        first_name: str,
        last_name: str,
        phone_number: str,
        address: str,
        business_sphere: str,
        user_id: int,
        img: Optional[str] = None,
    ) -> None:
        self.renter_id = renter_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.address = address
        self.business_sphere = business_sphere
        self.user_id = user_id
        self.img = img

    @classmethod
    def get_by_user_id(cls, user_id: int) -> Type["Renter"]:
        """
        Fetches a renter by the user ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            Optional[Renter]: A Renter instance if found, None otherwise.

        Raises:
            ValueError: If the renter does not exist.
        """
        result = cls.fetch_one(
            cls.sql_provider.get("get_renter_by_user_id.sql", user_id=user_id),
            current_app.config["db_config"][session["role"]],
        )
        if not result:
            raise ValueError("Renter with such ID does not exist.")
        return Renter(*result)


class Billboard(BaseModel, metaclass=MetaSQL):
    """
    Represents a billboard and its attributes.

    Attributes:
        billboard_id (int): Unique ID of the billboard.
        price_per_month (float): Monthly price for the billboard.
        size (float): Size of the billboard in square meters.
        billboard_address (str): Physical address of the billboard.
        mount_date (Optional[datetime]): Date the billboard was mounted.
        quality (int): Quality rating of the billboard.
        owner_id (int): ID of the owner of the billboard.
        img_path (Optional[str]): Path to the billboard's image.
    """

    def __init__(
        self,
        billboard_id: int,
        price_per_month: float,
        size: float,
        billboard_address: str,
        mount_date: Optional[datetime],
        quality: int,
        owner_id: int,
    ) -> None:
        self.billboard_id = billboard_id
        self.price_per_month = price_per_month
        self.size = size
        self.billboard_address = billboard_address
        self.mount_date = mount_date
        self.quality = quality
        self.owner_id = owner_id
        self.img_path = (
            f"img/{self.billboard_id}.jpg"
            if path.isfile(
                path.join(path.dirname(__file__), f"static/img/{self.billboard_id}.jpg")
            )
            else None
        )

    @classmethod
    def get_billboard(cls, billboard_id: int) -> "Billboard":
        """
        Fetches a billboard by ID.

        Args:
            billboard_id (int): The ID of the billboard.

        Returns:
            Billboard: A Billboard instance if found.

        Raises:
            ValueError: If the billboard does not exist.
        """
        result = cls.fetch_one(
            cls.sql_provider.get("get_billboard.sql", billboard_id=billboard_id),
            current_app.config["db_config"][session["role"]],
        )
        if not result:
            raise ValueError("Billboard with such ID does not exist.")
        return Billboard(*result)

    @classmethod
    def get_random_billboards(cls, count: int) -> List["Billboard"]:
        """
        Fetches a random set of billboards.

        Args:
            count (int): Number of random billboards to fetch.

        Returns:
            List[Billboard]: A list of Billboard instances.
        """
        result = cls.fetch_all(
            cls.sql_provider.get("get_n_random_billboards.sql", n=count),
            db_config=current_app.config["db_config"][session["role"]],
        )
        return [Billboard(*x) for x in result]

    def get_occupied_periods(self) -> List[Dict[str, datetime]]:
        """
        Fetches occupied periods for the billboard.

        Returns:
            List[Dict[str, datetime]]: A list of occupied periods with start and end dates.
        """
        result = self.fetch_all(
            Billboard.sql_provider.get(
                "get_occupied_periods.sql", billboard_id=self.billboard_id
            ),
            current_app.config["db_config"][session["role"]],
        )
        return (
            [
                {
                    "start": datetime.strptime(f"{x[0]}/{x[1]}", "%m/%Y"),
                    "end": datetime.strptime(f"{x[2]}/{x[3]}", "%m/%Y"),
                }
                for x in result
            ]
            if result
            else []
        )

    def is_period_overlaps(self, start_date: datetime, end_date: datetime) -> bool:
        """
        Checks if a given period overlaps with occupied periods.

        Args:
            start_date (datetime): Start date of the period.
            end_date (datetime): End date of the period.

        Returns:
            bool: True if the period overlaps, False otherwise.
        """
        occupied_periods = self.get_occupied_periods()
        return any(
            period["start"] <= end_date and start_date <= period["end"]
            for period in occupied_periods
        )


class OrderHandler(BaseModel, metaclass=MetaSQL):
    """
    Handles operations related to billboard orders.
    """

    @classmethod
    def check_input(cls, start_date: str, end_date: str, billboard: Billboard) -> bool:
        """
        Validates input for order dates and checks for conflicts.

        Args:
            start_date (str): Start date in MM/YYYY format.
            end_date (str): End date in MM/YYYY format.
            billboard (Billboard): The billboard being ordered.

        Raises:
            ValueError: If the input dates are invalid or conflict with existing bookings.

        Returns:
            bool: True if input is valid.
        """

        def is_valid_format(date_str: str) -> bool:
            """
            Validates if a date string is in the correct MM/YYYY format.

            Args:
                date_str (str): The date string to validate.

            Returns:
                bool: True if the date string is valid, False otherwise.
            """
            try:
                datetime.strptime(date_str, "%m/%Y")
                return True
            except ValueError:
                return False

        if not is_valid_format(start_date):
            raise ValueError(
                f"Invalid start date format: {start_date}. Expected MM/YYYY."
            )
        if not is_valid_format(end_date):
            raise ValueError(f"Invalid end date format: {end_date}. Expected MM/YYYY.")

        start_date_obj = datetime.strptime(start_date, "%m/%Y")
        end_date_obj = datetime.strptime(end_date, "%m/%Y")

        if end_date_obj < start_date_obj:
            raise ValueError("End date must be equal to or later than start date.")

        if billboard.is_period_overlaps(start_date_obj, end_date_obj):
            raise ValueError("Selected period conflicts with existing booking.")
        return True

    @classmethod
    def save_order_row_in_cart(
        cls,
        billboard_id: int,
        start_month: int,
        start_year: int,
        end_month: int,
        end_year: int,
    ) -> None:
        """
        Saves order details into the cart session.

        Args:
            billboard_id (int): Billboard ID.
            start_month (int): Start month.
            start_year (int): Start year.
            end_month (int): End month.
            end_year (int): End year.
        """
        session.setdefault("cart", []).append(
            {
                "billboard_id": billboard_id,
                "start_month": start_month,
                "start_year": start_year,
                "end_month": end_month,
                "end_year": end_year,
            }
        )


class CheckoutHandler(BaseModel, metaclass=MetaSQL):
    """
    Handles the checkout process for billboard orders.
    """

    @classmethod
    def checkout(cls, order_rows: List[Dict[str, Any]]) -> None:
        """
        Processes the checkout for the user's cart.

        Args:
            order_rows (List[Dict[str, Any]]): List of order details from the cart.
        """

        def calculate_price(
            price_per_month: float,
            start_month: int,
            start_year: int,
            end_month: int,
            end_year: int,
        ) -> float:
            """
            Calculates the total price for the selected rental period.

            Args:
                price_per_month (float): Monthly rental price.
                start_month (int): Start month of the rental.
                start_year (int): Start year of the rental.
                end_month (int): End month of the rental.
                end_year (int): End year of the rental.

            Returns:
                float: Total price for the rental period.
            """
            months = (end_year - start_year) * 12 + (end_month - start_month + 1)
            return price_per_month * months

        # Retrieve all billboard data and associated prices
        cart = session.get("cart", [])
        billboards = [Billboard.get_billboard(order["billboard_id"]) for order in cart]
        prices = [
            calculate_price(
                billboard.price_per_month,
                order["start_month"],
                order["start_year"],
                order["end_month"],
                order["end_year"],
            )
            for billboard, order in zip(billboards, cart)
        ]

        # Begin transaction for order processing
        with cls.transaction(
            current_app.config["db_config"][session["role"]]
        ) as cursor:
            renter = Renter.get_by_user_id(session["user_id"])
            order_id = cls.insert(
                cls.sql_provider.get(
                    "add_order.sql",
                    registration_date=datetime.now().date(),
                    total_cost=sum(prices),
                    renter_id=renter.renter_id,
                ),
                current_app.config["db_config"][session["role"]],
                cursor=cursor,
            )

            # Process each order row
            for billboard, order_row, price in zip(billboards, order_rows, prices):
                start_date = datetime(
                    order_row["start_year"], order_row["start_month"], 1
                )
                end_date = datetime(order_row["end_year"], order_row["end_month"], 1)

                if billboard.is_period_overlaps(start_date, end_date):
                    raise ValueError(
                        f"Selected period for billboard {billboard.billboard_id} overlaps with existing bookings."
                    )

                cls.insert(
                    cls.sql_provider.get(
                        "add_order_row.sql",
                        start_year=order_row["start_year"],
                        start_month=order_row["start_month"],
                        end_year=order_row["end_year"],
                        end_month=order_row["end_month"],
                        price=price,
                        order_id=order_id,
                        billboard_id=order_row["billboard_id"],
                    ),
                    current_app.config["db_config"][session["role"]],
                    cursor=cursor,
                )

        # Clear the session cart after successful checkout
        session["cart"] = []
