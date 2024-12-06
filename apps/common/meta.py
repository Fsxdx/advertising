import os
import sys
from typing import Any

from .database.sql_provider import SQLProvider


class MetaSQL(type):
    """Metaclass for automatically injecting an SQL provider into classes.

    The SQL provider is initialized based on the file path of the module
    where the class is defined. It assumes that SQL files are stored
    in a directory named 'sql' located in the same directory as the module.

    Raises:
        ValueError: If the module's file path cannot be determined.
    """

    def __new__(cls, name: str, bases: tuple[type, ...], dct: dict[str, Any]) -> type:
        module_name = dct["__module__"]
        module = sys.modules.get(module_name)

        if module and hasattr(module, "__file__") and module.__file__:
            class_file_path = os.path.dirname(module.__file__)
            sql_directory = os.path.join(class_file_path, "sql")
            dct["sql_provider"] = SQLProvider(sql_directory)
        # else:
        #     raise ValueError(
        #         f"Cannot retrieve file path for module '{module_name}'. Ensure the module has a valid '__file__' attribute."
        #     )

        return super().__new__(cls, name, bases, dct)
