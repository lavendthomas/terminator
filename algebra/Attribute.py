import re

class Attribute:

    def __init__(self, attr: str):
        self.attr = attr
        self._check_attribute_name()

    def toSQL(self, dbschema):
        return self.attr

    def get_attr(self):
        return self.attr

    def __str__(self):
        return self.__class__.__name__ + "(\"" + self.attr + "\")"

    def _check_attribute_name(self):
        if re.fullmatch(r'[a-zA-Z][a-zA-Z0-9]*', str(self.attr)) is None:
            raise ValueError(str(self.attr) + " is not an alphanumeric string or starts with a number.")
