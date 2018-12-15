from algebra.Expression import Expression
from algebra.Attribute import Attribute
from copy import deepcopy
from algebra.Exceptions import *


class SelectionAttribute(Expression):

    def __init__(self, attr1: Attribute, attr2: Attribute, expr: Expression):
        self.attr1 = attr1
        self.attr2 = attr2
        self.expr = expr

    def toSQL(self, dbschema):
        attributes = self.expr.get_attributes(dbschema)
        if self.attr1.get_attr() not in map(lambda x:x.get_name(), attributes):
            raise InvalidAttributeException("Attribute " + self.attr1.get_attr() + " is not in the table.")

        if self.attr2.get_attr() not in map(lambda x:x.get_name(), attributes):
            raise InvalidAttributeException("Attribute " + self.attr2.get_attr() + " is not in the table.")

        attr1_type = ""
        attr2_type = ""
        for col in attributes:
            if col.get_name() == self.attr1.get_attr():
                attr1_type = col.get_type()
                break
        for col in attributes:
            if col.get_name() == self.attr2.get_attr():
                attr2_type = col.get_type()
                break

        if attr1_type != attr2_type:
            raise NotMatchingAttributesException("Attributes do not have the same type. \n First attribute is of type "
                                                 + attr1_type + " and second attribute is of type " + attr2_type + ".")

        return "SELECT * FROM " + self.expr.toSQL(dbschema) + " WHERE " + self.attr1.toSQL(dbschema) + " = " +\
               self.attr2.toSQL(dbschema)

    def get_attributes(self, dbschema):
        return deepcopy(self.expr.get_attributes(dbschema))

    def __str__(self):
        return self.__class__.__name__ + "(" + str(self.attr1) + ", " + str(self.attr2) + ", " + str(self.expr) + ")"
