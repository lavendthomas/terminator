from algebra.Expression import Expression as Expr
from copy import deepcopy


class Difference(Expr):

    def __init__(self, expr1, expr2):
        self.nodes = [expr1, expr2]

    def toSQL(self, dbschema):
        return "SELECT * FROM "

    def get_attributes(self, dbschema):
        return deepcopy(self.nodes[0].getAttributes(dbschema))
