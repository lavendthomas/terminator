from algebra.Expression import Expression


class Relation(Expression):

    def __init__(self, table):
        self.table = str(table)

    def toSQL(self, dbschema):
        if not dbschema.is_table(self.table):
            raise Exception("Table " + self.table + " is not in the database.")

        return self.table

    def get_attributes(self, dbschema):
        return dbschema.get_attributes(self.table)
