from algebra.Expression import Expression as Expr


class SelectionAttribute(Expr):

    def __init__(self, attr1, attr2, expr):
        self.nodes = [attr1, attr2, expr]

    def toSQL(self):
        return "SELECT * FROM " + self.nodes[2].toSQL() + " WHERE " + self.nodes[0].toSQL() + " = " + self.nodes[1].toSQL()

    def get_attributes(self, dbschema):
        return self.nodes[2].get_attributes(dbschema)
