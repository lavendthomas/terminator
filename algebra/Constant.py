class Constant:

    def __init__(self, cst):
        self.cst = str(cst)

        if isinstance(cst, int):
            self.type = "INT"
        elif isinstance(cst, float):
            self.type = "FLOAT"
        elif isinstance(cst, str):
            self.type = "TEXT"

    def get_type(self):
        return self.type

    def toSQL(self, dbschema):
        return '"' + self.cst + '"'

    def get_cst(self):
        return self.cst
