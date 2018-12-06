from algebra.Expression import Expression
from copy import deepcopy

class Project(Expression):

    """
    columns: set of attributes to keep
    """
    def __init__(self, columns: list, expr: Expression):
        self.nodes = [columns, expr]

    def toSQL(self, dbschema):
        attrs = deepcopy(self.nodes[1].get_attributes(dbschema))

        select_attributes = ""
        for i in range(len(self.nodes[0])):
            if self.nodes[0][i] not in map(lambda x: x.get_name(), attrs):
                raise Exception(self.nodes[0][i] + " not in " + str(self.nodes[1][i]))

            select_attributes += self.nodes[0][i]
            if i != len(self.nodes[0])-1:
                select_attributes += ", "

        return "SELECT " + select_attributes + " FROM (" + self.nodes[1].toSQL(dbschema) + ")"

    def get_attributes(self, dbschema):
        attrs = deepcopy(self.nodes[1].get_attributes(dbschema))
        new_attr = list()
        for i in range(len(attrs)):
            if attrs[i].get_name() in self.nodes[0]:
                new_attr.append(attrs[i])

        return new_attr
