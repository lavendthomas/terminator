from algebra.Expression import Expression as Expr
from remote.DBSchema import *
from copy import deepcopy


class Rename(Expr):

    def __init__(self, from_attr, to_attr, expr):
        self.nodes = [from_attr, to_attr, expr]

    def toSQL(self, dbschema):
        attrs = deepcopy(self.nodes[2].get_attributes(dbschema))

        for i in range(len(attrs)):
            if attrs[i].get_name() == self.nodes[0].get_attr():
                from_col = Column(attrs[i].get_name(), attrs[i].get_type())
                to_col = Column(self.nodes[1].get_attr(), attrs[i].get_type())
                attrs[i] = to_col
                break

        select_attributes = ""
        for i in range(len(attrs)):
            if attrs[i] == to_col:
                select_attributes += from_col.get_name() + " AS " + to_col.get_name()
            else:
                select_attributes += attrs[i].get_name()
            if i != len(attrs)-1:
                select_attributes += ", "

        return "SELECT " + select_attributes + " FROM (" + self.nodes[2].toSQL(dbschema) + ")"

    def get_attributes(self, dbschema):
        attrs = deepcopy(self.nodes[2].get_attributes(dbschema))

        for i in range(len(attrs)):
            if attrs[i].get_name() == self.nodes[0].get_attr():
                attrs[i] = Column(self.nodes[1].get_attr(), attrs[i].get_type())
                break

        return attrs
