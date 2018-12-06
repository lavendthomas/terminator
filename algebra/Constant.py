class Constant:

    def __init__(self, cst):
        self.cst = str(cst)

    def toSQL(self, dbschema):
        return '"' + self.cst + '"'
