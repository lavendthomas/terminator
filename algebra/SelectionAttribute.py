from algebra.Expression import Expression
from algebra.Attribute import Attribute
from copy import deepcopy


class SelectionAttribute(Expression):

    def __init__(self, attr1: Attribute, attr2: Attribute, expr: Expression):
        self.attr1 = attr1
        self.attr2 = attr2
        self.expr = expr

    def toSQL(self, dbschema):
        return "SELECT * FROM " + self.expr.toSQL(dbschema) + " WHERE " + self.attr1.toSQL(dbschema) + " = " +\
               self.attr2.toSQL(dbschema)

    def get_attributes(self, dbschema):
        return deepcopy(self.expr.get_attributes(dbschema))
