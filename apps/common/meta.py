import os
import sys
from .database.sql_provider import SQLProvider


class MetaSQL(type):
    def __new__(cls, name, bases, dct):
        module_name = dct.get('__module__')
        module = sys.modules.get(module_name)

        if module and hasattr(module, '__file__') and module.__file__:
            class_file_path = os.path.dirname(module.__file__)
            dct['sql_provider'] = SQLProvider(os.path.join(class_file_path, 'sql'))
        else:
            raise ValueError(f"Can't retrieve path for {module_name}")

        return super().__new__(cls, name, bases, dct)
