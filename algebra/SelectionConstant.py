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
        attributes = self.expr.get_attributes(dbschema)
        if self.attr.get_attr() not in map(lambda x:x.get_name(), attributes):
            raise Exception("Attribute " + self.attr.get_attr() + " is not in the table.")

        attr_type = ""
        for col in attributes:
            if col.get_name() == self.attr.get_attr():
                attr_type = col.get_type()
                break

        if attr_type != self.cst.get_type():
            raise Exception("Constant " + self.cst.get_cst() + " is not the same type as the attribute. \n "
                            "Attribute " + self.attr.get_attr() + " is of type " + attr_type + " and the "
                            "constant of type " + self.cst.get_type() + ".")

        return "SELECT * FROM " + self.expr.toSQL(dbschema) + " WHERE " + self.attr.toSQL(dbschema) + " = " +\
               self.cst.toSQL(dbschema)

    def get_attributes(self, dbschema):
        return deepcopy(self.expr.get_attributes(dbschema))
