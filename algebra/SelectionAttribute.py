from algebra.Expression import Expression as Expr
from copy import deepcopy


class SelectionAttribute(Expr):

    def __init__(self, attr1, attr2, expr):
        self.nodes = [attr1, attr2, expr]

    def toSQL(self, dbschema):
        return "SELECT * FROM " + self.nodes[2].toSQL(dbschema) + " WHERE " + self.nodes[0].toSQL(dbschema) + " = " + self.nodes[1].toSQL(dbschema)

    def get_attributes(self, dbschema):
        return deepcopy(self.nodes[2].get_attributes(dbschema))
