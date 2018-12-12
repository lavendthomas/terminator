from algebra.Expression import Expression
from algebra.Attribute import Attribute
from algebra.Constant import Constant
from algebra.Expression import Expression
from copy import deepcopy


class SelectionConstant(Expression):

    def __init__(self, attr: Attribute, cst: Constant, expr: Expression):
        self.attr = attr
        self.cst = cst
        self.expr = expr

    def toSQL(self, dbschema):
        return "SELECT * FROM " + self.expr.toSQL(dbschema) + " WHERE " + self.attr.toSQL(dbschema) + " = " +\
               self.cst.toSQL(dbschema)

    def get_attributes(self, dbschema):
        return deepcopy(self.expr.getAttributes(dbschema))
