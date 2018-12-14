from algebra.Expression import Expression
from copy import deepcopy

class Project(Expression):

    """
    columns: set of attributes to keep
    """
    def __init__(self, columns: list, expr: Expression):
        self.columns = columns
        self.expr = expr

    def toSQL(self, dbschema):
        attrs = deepcopy(self.expr.get_attributes(dbschema))

        select_attributes = ""
        for i in range(len(self.columns)):
            if self.columns[i] not in map(lambda x: x.get_name(), attrs):
                raise Exception(self.columns[i] + " not in " + str(self.expr))

            select_attributes += self.columns[i]
            if i != len(self.columns)-1:
                select_attributes += ", "

        return "SELECT " + select_attributes + " FROM (" + self.expr.toSQL(dbschema) + ")"

    def get_attributes(self, dbschema):
        attrs = deepcopy(self.expr.get_attributes(dbschema))
        new_attr = list()
        for i in range(len(attrs)):
            if attrs[i].get_name() in self.columns:
                new_attr.append(attrs[i])

        return new_attr

    def __str__(self):
        col_str = "["
        for i in range(len(self.columns)):
            col_str += "\"" + str(self.columns[i]) + "\""
            if i != len(self.columns)-1:
                col_str += ", "
            else:
                col_str += "]"

        return self.__class__.__name__ + "(" + col_str + ", " + str(self.expr) + ")"
