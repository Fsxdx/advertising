import os
from string import Template
import logging
from pathlib import Path

class SQLProvider:
    """
    Class for managing and processing SQL templates.

    This class loads SQL scripts from a directory and provides methods to substitute variables in the SQL templates.

    Args:
        file_path (str): Path to the directory containing SQL files.
    """

    def __init__(self, file_path: str):
        self.scripts = {}

        # Load all .sql files from the provided directory
        for file in os.listdir(file_path):
            if file.endswith(".sql"):
                with open(os.path.join(file_path, file), 'r') as sql_file:
                    self.scripts[file] = Template(sql_file.read())


    def get(self, file: str, **kwargs) -> str:
        """
        Retrieve and substitute variables in a SQL template.

        Args:
            file (str): The name of the SQL file.
            **kwargs: Key-value pairs to substitute in the SQL template.

        Returns:
            str: The resulting SQL query after substitution.
        """
        sql_template = self.scripts.get(file)
        if not sql_template:
            raise ValueError(f"SQL template {file} not found.")

        try:
            query = sql_template.substitute(**kwargs)
        except KeyError as e:
            raise ValueError(f"Missing parameter for SQL substitution: {e}")

        return query
