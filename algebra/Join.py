from algebra.Expression import Expression as Expr
from copy import deepcopy


class Join(Expr):

    def __init__(self, expr1, expr2):
        self.nodes = [expr1, expr2]

    def toSQL(self, dbschema):
        return ""

    def get_attributes(self, dbschema):
        attrs1 = self.nodes[0].get_attributes(dbschema)
        attrs2 = self.nodes[1].get_attributes(dbschema)
        new_attrs = deepcopy(attrs1)

        for attr in attrs2:
            if attr not in new_attrs:
                new_attrs.append(attr)

        return new_attrs
