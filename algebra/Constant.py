from typing import Union
import re


class Constant:

    def __init__(self, cst: Union[str, int, float]):
        self.cst = str(cst)

        if isinstance(cst, int):
            self.type = "INTEGER"
        elif isinstance(cst, float):
            self.type = "REAL"
        elif isinstance(cst, str):
            self.type = "TEXT"
        else:
            self.type = "NONE"      # TODO handle unknown formats

    def get_type(self):
        return self.type

    def toSQL(self, dbschema):
        if self.type == "INTEGER" or self.type == "REAL":
            return str(self.cst)
        return '"' + re.sub(r'(["\'\\])', r'\\\1', self.cst) + '"'

    def get_cst(self):
        return self.cst

    def __str__(self):
        return self.__class__.__name__ + "(\"" + self.cst + "\")"
