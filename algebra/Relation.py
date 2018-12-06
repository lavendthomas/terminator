class Relation:

    def __init__(self, table):
        self.table = str(table)

    def toSQL(self):
        return self.table

    def get_attributes(self, dbschema):
        return dbschema.get_attributes(self.table)
