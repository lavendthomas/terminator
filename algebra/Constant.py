from typing import Union
import re


class Constant:
    """
    Represents constant in a form of string
    """

    def __init__(self, cst: Union[str, int, float]):
        """
        Converts constant to string and saves the type of the constant according to types used by SQL
        (int as INTEGER, float as REAL, str as TEXT otherwise as NONE)

        :param cst: The name of the constant (can contains str, int or float)
        """
        self.cst = str(cst)

        if isinstance(cst, int):
            self.type = "INTEGER"
        elif isinstance(cst, float):
            self.type = "REAL"
        elif isinstance(cst, str):
            self.type = "TEXT"
        else:
            self.type = "NONE"

    def get_type(self):
        """
        Returns SQL type of the constant

        :return: Type of the constant
        """
        return self.type

    def toSQL(self, dbschema):
        """
        Returns constant in a form in which SQLite is able to read it (str)

        :param dbschema: Instance of DBSchema
        :return: The name of the constant
        """
        if self.type == "INTEGER" or self.type == "REAL":
            return str(self.cst)
        return '"' + re.sub(r'(["\'\\])', r'\\\1', self.cst) + '"'

    def get_cst(self):
        """
        Returns name of the constant

        :return: The name of the constant
        """
        return self.cst

    def __str__(self):
        """
        Overwritten method str()

        :return: String in a form: Constant("name")
        """
        return self.__class__.__name__ + "(\"" + self.cst + "\")"
