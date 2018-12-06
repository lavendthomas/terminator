from algebra.Expression import Expression as Expr
from remote.DBSchema import *


class Rename(Expr):

    def __init__(self, from_attr, to_attr, expr):
        self.nodes = [from_attr, to_attr, expr]

    def toSQL(self):
        return "SELECT * FROM "

    def get_attributes(self, dbschema):
        attrs = self.nodes[2].get_attributes(dbschema)

        for i in range(len(attrs)):
            a = attrs[i].get_name()
            b = self.nodes[0].get_attr()
            c = type(a)
            d = type(b)
            if attrs[i].get_name() == self.nodes[0].get_attr():
                attrs[i] = Column(self.nodes[1].get_attr(), attrs[i].get_type())
                break

        return attrs
