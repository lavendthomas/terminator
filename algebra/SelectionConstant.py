from algebra.Expression import Expression as Expr
from algebra.Attribute import Attribute
from algebra.Constant import Constant
from algebra.Expression import Expression


class SelectionConstant(Expr):

    def __init__(self, attr: Attribute, cst: Constant, expr: Expression):
        self.nodes = [attr, cst, expr]

    def toSQL(self):
        return "SELECT * FROM " + self.nodes[2].toSQL() + " WHERE " + self.nodes[0].toSQL() + " = " + self.nodes[1].toSQL()

    def get_attributes(self, dbschema):
        return self.nodes[2].getAttributes(dbschema)
