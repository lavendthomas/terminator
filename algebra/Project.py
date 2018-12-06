from algebra.Expression import Expression

class Project(Expression):

    """
    columns: set of attributes to keep
    """
    def __init__(self, columns: list, expr: Expression):
        self.nodes = [columns, expr]

    def toSQL(self):
        return ""

    def get_attributes(self, dbschema):
        attrs = self.nodes[1].get_attributes(dbschema)
        new_attr = list()
        for i in range(len(attrs)):
            if attrs[i].get_name() in self.nodes[0]:
                new_attr.append(attrs[i])

        return new_attr
