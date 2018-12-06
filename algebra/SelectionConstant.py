from algebra.Expression import Expression as Expr
from algebra.Attribute import Attribute
from algebra.Constant import Constant
from algebra.Expression import Expression
from copy import deepcopy

class SelectionConstant(Expr):

    def __init__(self, attr: Attribute, cst: Constant, expr: Expression):
        self.nodes = [attr, cst, expr]

    def toSQL(self, dbschema):
        return "SELECT * FROM " + self.nodes[2].toSQL(dbschema) + " WHERE " + self.nodes[0].toSQL(dbschema) + " = " + self.nodes[1].toSQL(dbschema)

    def get_attributes(self, dbschema):
        return deepcopy(self.nodes[2].getAttributes(dbschema))
