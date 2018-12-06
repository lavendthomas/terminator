class Constant:

    def __init__(self, cst):
        self.cst = str(cst)

    def toSQL(self):
        return '"' + self.cst + '"'
