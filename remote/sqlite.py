from algebra.Expression import *
from remote.DBSchema import DBSchema
from typing import Union


class SQLiteDB:

    """
    db : path of the database file
    """
    def __init__(self, db: str):
        self.filename = db
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
        self.dbschema = DBSchema(db)

    def getDB(self):
        return self.dbschema

    def execute(self, query: Union[Expression, str]):
        """
        query: Expression to execute in the database or an SQL request
        """
        if isinstance(query, Expression):
            sql = query.toSQL(self.dbschema)
        else:
            sql = query

        for line in self.cursor.execute(sql):
            print(line)

        if "table" in sql.lower():
            self.dbschema = DBSchema(self.filename)

    def commit(self):
        self.conn.commit()

    def toSQL(self, query: Expression):
        return query.toSQL(self.dbschema)
