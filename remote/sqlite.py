from algebra.Expression import *
from remote.DBSchema import DBSchema


class SQLiteDB:

    """
    db : path of the database file
    """
    def __init__(self, db: str):
        self.filename = db
        self.cursor = c = sqlite3.connect(db).cursor()
        self.dbschema = DBSchema(db)

    def getDB(self):
        return self.dbschema

    def execute(self, query: Expression):
        """
        query: Expression to execute in the database
        """
        for line in self.cursor.execute(query.toSQL(self.dbschema)):
            print(line)

    def toSQL(self, query: Expression):
        return query.toSQL(self.dbschema)
