from algebra.Expression import *
from remote.DBSchema import *
from remote.sqlite import SQLiteDB

def printQuery(query, dbschema):
    print(query.toSQL(dbschema) + ";")

if __name__ == "__main__":

    pass
