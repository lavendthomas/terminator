class Relation:

    def __init__(self, table):
        self.table = str(table)

    def toSQL(self, dbschema):
        return self.table

    def get_attributes(self, dbschema):
        return dbschema.get_attributes(self.table)
