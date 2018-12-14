from algebra.Expression import Expression
from algebra.Attribute import Attribute
from remote.DBSchema import *
from copy import deepcopy


class Rename(Expression):

    def __init__(self, from_attr: Attribute, to_attr: Attribute, expr: Expression):
        self.from_attr = from_attr
        self.to_attr = to_attr
        self.expr = expr

    def toSQL(self, dbschema):
        attrs = deepcopy(self.expr.get_attributes(dbschema))
        if self.to_attr.get_attr() in map(lambda x: x.get_name(), attrs):
            raise Exception("Attribute " + self.to_attr.get_attr() + " is already in the table.")

        from_col = None
        to_col = None

        for i in range(len(attrs)):
            if attrs[i].get_name() == self.from_attr.get_attr():
                from_col = Column(attrs[i].get_name(), attrs[i].get_type())
                to_col = Column(self.to_attr.get_attr(), attrs[i].get_type())
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

        return "SELECT " + select_attributes + " FROM (" + self.expr.toSQL(dbschema) + ")"

    def get_attributes(self, dbschema):
        attrs = deepcopy(self.expr.get_attributes(dbschema))

        for i in range(len(attrs)):
            if attrs[i].get_name() == self.from_attr.get_attr():
                attrs[i] = Column(self.to_attr.get_attr(), attrs[i].get_type())
                break

        return attrs

    def __str__(self):
        return self.__class__.__name__ + "(" + str(self.from_attr) + ", " + str(self.to_attr) + ", " +\
               str(self.expr) + ")"
