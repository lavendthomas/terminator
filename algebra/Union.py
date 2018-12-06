from algebra.Expression import Expression as Expr


class Union(Expr):

    def __init__(self, expr1, expr2):
        self.nodes = [expr1, expr2]

    def toSQL(self, dbschema):

        for (att1, att2) in zip(self.nodes[0].get_attributes(dbschema), self.nodes[1].get_attributes(dbschema)):
            if att1 != att2:
                raise Exception("Not same types or names and Fuck you!")

        return ""

    def get_attributes(self, dbschema):
        return self.nodes[0].getAttributes(dbschema)

