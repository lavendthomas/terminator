from algebra.Expression import Expression
from copy import deepcopy
from algebra.Exceptions import *


class Difference(Expression):

    def __init__(self, expr1: Expression, expr2: Expression):
        self.expr1 = expr1
        self.expr2 = expr2

    def toSQL(self, dbschema):
        attrs1 = deepcopy(self.expr1.get_attributes(dbschema))
        attrs2 = deepcopy(self.expr2.get_attributes(dbschema))
        attrs1.sort()
        attrs2.sort()

        if len(attrs1) != len(attrs2):
            raise NotMatchingAttributesException("The counts of attributes of " + str(self.expr1) + " and " +
                                                 str(self.expr2) + " are not the same.")

        for (att1, att2) in zip(attrs1, attrs2):
            if att1 != att2:
                raise NotMatchingAttributesException("Attributes " + att1.get_attr() + " and " + att2.get_attr() +
                                                     " are not of same type or do not have same names.")

        select_attributes1 = ""
        select_attributes2 = ""
        conditions = ""
        for i in range(len(attrs1)):
            select_attributes1 += "t1." + attrs1[i].get_name()
            select_attributes2 += "t2." + attrs1[i].get_name()
            conditions += "t1." + attrs1[i].get_name() + " = t2." + attrs1[i].get_name()
            if i != len(attrs1) - 1:
                select_attributes1 += ", "
                select_attributes2 += ", "
                conditions += " AND "

        return "SELECT " + select_attributes1 + " FROM (" + self.expr1.toSQL(dbschema) + ") AS t1 WHERE NOT EXISTS "\
               "(SELECT " + select_attributes2 + " FROM (" + self.expr2.toSQL(dbschema) + ") AS t2 WHERE " +\
               conditions + ")"

    def get_attributes(self, dbschema):
        return deepcopy(self.expr1.get_attributes(dbschema))

    def __str__(self):
        return self.__class__.__name__ + "(" + str(self.expr1) + ", " + str(self.expr2) + ")"
