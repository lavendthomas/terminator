import re


class Attribute:
    """
    Represents one single attribute (column) of a table
    """
    def __init__(self, attr: str):
        """
        Constructor of the class attribute

        :param attr: The name of the attribute
        """
        self.attr = attr
        self._check_attribute_name()

    def toSQL(self, dbschema):
        """
        Returns attribute in a form in which SQLite is able to read it (str)

        :param dbschema: Instance of DBSchema
        :return: The name of the attribute
        """
        return self.attr

    def get_attr(self):
        """
        Returns name of the attribute

        :return: The name of the attribute
        """
        return self.attr

    def __str__(self):
        """
        Overwritten method str()

        :return: String in a form: Attribute("name")
        """
        return self.__class__.__name__ + "(\"" + self.attr + "\")"

    def _check_attribute_name(self):
        """
        Checks if the attribute is alphanumeric string and if it does not start with a number
        Raise exception if the attribute is not an alphanumeric string or starts with a number
        """
        if re.fullmatch(r'[a-zA-Z][a-zA-Z0-9]*', str(self.attr)) is None:
            raise ValueError(str(self.attr) + " is not an alphanumeric string or starts with a number.")
