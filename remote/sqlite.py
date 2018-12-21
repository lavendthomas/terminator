from algebra.Expression import *
from remote.DBSchema import DBSchema
from typing import Union


class SQLiteDB:
    """
    Represents the communication between SQLite and the SPJRUD to SQL Converter
    """
    def __init__(self, db: str):
        """
        Constructor of the class SQLiteDB

        :param db: Path of the database file
        """
        self.filename = db
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
        self.dbschema = DBSchema(db)

    def getDB(self):
        """f
        :return: Dbschema
        """
        return self.dbschema

    def execute(self, query: Union[Expression, str]):
        """
        Executes the query and prints its result

        :param query: Expression to execute in the database or an SQL request
        """
        if isinstance(query, Expression):
            sql = query.toSQL(self.dbschema)
        else:
            sql = query

        for line in self.cursor.execute(sql):
            empty = True
            if print(line):
                empty = False
            if empty:
                print("Empty set")

        if "table" in sql.lower():
            self.dbschema = DBSchema(self.filename)

    def commit(self):
        """
        Saves changes to the database
        """
        self.conn.commit()

    def toSQL(self, query: Expression):
        """
        Returns expression in a form in which SQLite is able to read it (str)

        :param query: Expression which will be converted to SQL
        :return: String in the form of SQL request
        """
        return query.toSQL(self.dbschema)
