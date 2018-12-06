from algebra.Expression import Expression as Expr


class Difference(Expr):

    def __init__(self, expr1, expr2):
        self.nodes = [expr1, expr2]

    def toSQL(self):
        return "SELECT * FROM "

    def get_attributes(self, dbschema):
        return self.nodes[0].getAttributes(dbschema)

