from algebra.Expression import Expression as Expr
from copy import deepcopy


class Difference(Expr):

    def __init__(self, expr1, expr2):
        self.nodes = [expr1, expr2]

    def toSQL(self, dbschema):
        attrs1 = deepcopy(self.nodes[0].get_attributes(dbschema))
        attrs2 = deepcopy(self.nodes[1].get_attributes(dbschema))
        attrs1.sort()
        attrs2.sort()

        if len(attrs1) != len(attrs2):
            raise Exception("The numbers of attributes of " + str(self.nodes[0]) + " and " + str(self.nodes[1]) +
                            " are not the same.")

        for (att1, att2) in zip(attrs1, attrs2):
            if att1 != att2:
                raise Exception("Not same types or names and Fuck you!")        # TODO fuck you :*

        select_attributes1 = ""
        for i in range(len(attrs1)):
            select_attributes1 += "t1." + attrs1[i].get_name()
            if i != len(attrs1) - 1:
                select_attributes1 += ", "

        select_attributes2 = ""
        for i in range(len(attrs1)):
            select_attributes2 += "t2." + attrs1[i].get_name()
            if i != len(attrs1) - 1:
                select_attributes2 += ", "

        conditions = ""
        for i in range(len(attrs1)):
            conditions += "t1." + attrs1[i].get_name() + " = t2." + attrs1[i].get_name()
            if i != len(attrs1) - 1:
                conditions += " AND "

        return "SELECT " + select_attributes1 + " FROM (" + self.nodes[0].toSQL(dbschema) + ") AS t1 WHERE NOT EXISTS "\
               "(SELECT " + select_attributes2 + " FROM (" + self.nodes[1].toSQL(dbschema) + ") AS t2 WHERE " +\
               conditions + ")"

    def get_attributes(self, dbschema):
        return deepcopy(self.nodes[0].getAttributes(dbschema))
