from algebra.Expression import Expression
from copy import deepcopy


class Join(Expression):

    def __init__(self, expr1: Expression, expr2: Expression):
        self.expr1 = expr1
        self.expr2 = expr2

    def toSQL(self, dbschema):
        attrs1 = deepcopy(self.expr1.get_attributes(dbschema))
        attrs2 = deepcopy(self.expr2.get_attributes(dbschema))

        common_attributes = []
        t2_attributes = []
        for i in range(len(attrs2)):
            if attrs2[i] in attrs1:
                common_attributes.append(attrs2[i])
            else:
                t2_attributes.append(attrs2[i])

        select_attributes = ""
        for i in range(len(attrs1)):
            select_attributes += "t1." + attrs1[i].get_name()
            if i != len(attrs1) - 1:
                select_attributes += ", "
        for i in range(len(t2_attributes)):
            if i == 0:
                select_attributes += ", "
            select_attributes += "t2." + t2_attributes[i].get_name()
            if i != len(t2_attributes) - 1:
                select_attributes += ", "

        conditions = ""
        if len(t2_attributes) > 0:
            conditions += " WHERE "
            for i in range(len(common_attributes)):
                conditions += "t1." + common_attributes[i].get_name() + " = t2." + common_attributes[i].get_name()
                if i != len(common_attributes) - 1:
                    conditions += " AND "

        return "SELECT " + select_attributes + " FROM (" + self.expr1.toSQL(dbschema) + ") AS t1, (" +\
               self.expr2.toSQL(dbschema) + ") AS t2" + conditions

    def get_attributes(self, dbschema):
        attrs1 = self.expr1.get_attributes(dbschema)
        attrs2 = self.expr2.get_attributes(dbschema)
        new_attrs = deepcopy(attrs1)

        for attr in attrs2:
            if attr not in new_attrs:
                new_attrs.append(attr)

        return new_attrs

    def __str__(self):
        return self.__class__.__name__ + "(" + str(self.expr1) + ", " + str(self.expr2) + ")"
