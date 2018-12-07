from algebra.Expression import Expression as Expr
from copy import deepcopy


class Join(Expr):

    def __init__(self, expr1, expr2):
        self.nodes = [expr1, expr2]

    def toSQL(self, dbschema):
        attrs1 = deepcopy(self.nodes[0].get_attributes(dbschema))
        attrs2 = deepcopy(self.nodes[1].get_attributes(dbschema))
        t2_attributes = []
        common_attributes = []

        for i in range(len(attrs2)):
            if attrs2[i] not in attrs1:
                t2_attributes.append(attrs2[i])
            else:
                common_attributes.append(attrs2[i])

        selected_attributes = ""

        for i in range(len(attrs1)):
            selected_attributes += "t1." + attrs1[i].get_name()
            if i != len(attrs1) - 1:
                selected_attributes += ", "

        for i in range(len(t2_attributes)):
            if i == 0:
                selected_attributes += ", "
            selected_attributes += "t2." + t2_attributes[i].get_name()
            if i != len(t2_attributes) - 1:
                selected_attributes += ", "

        conditions = ""

        if len(t2_attributes) > 0:
            conditions += " WHERE "
            for i in range(len(common_attributes)):
                conditions += "t1." + common_attributes[i].get_name() + " = t2." + common_attributes[i].get_name()
                if i != len(common_attributes) - 1:
                    conditions += " AND "

        return "SELECT " + selected_attributes + " FROM (" + self.nodes[0].toSQL(dbschema) + ") AS t1, (" +\
               self.nodes[1].toSQL(dbschema) + ") AS t2" + conditions

    def get_attributes(self, dbschema):
        attrs1 = self.nodes[0].get_attributes(dbschema)
        attrs2 = self.nodes[1].get_attributes(dbschema)
        new_attrs = deepcopy(attrs1)

        for attr in attrs2:
            if attr not in new_attrs:
                new_attrs.append(attr)

        return new_attrs
