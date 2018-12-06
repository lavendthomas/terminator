from algebra.Attribute import Attribute
from algebra.Constant import Constant
from algebra.Relation import Relation
from algebra.SelectionAttribute import SelectionAttribute
from algebra.SelectionConstant import SelectionConstant
from algebra.Rename import Rename
from algebra.Project import Project
from algebra.Join import Join
from algebra.Union import Union
from algebra.Difference import Difference
from remote.DBSchema import *

def printQuery(query, dbschema):
    print(query.toSQL(dbschema) + ";")

if __name__ == "__main__":

    db = DBSchema()
    db.add_table("users",
                 ["id", "name" ,  "pw"],
                 ["TEXT", "TEXT", "TEXT"])
    db.add_table("users2",
                 ["name", "id", "pw"],
                 ["TEXT", "TEXT", "TEXT"])

    print(Constant("test").toSQL(db))
    print(Attribute("test").toSQL(db))

    printQuery(SelectionConstant(Attribute("city"),Constant("Mons"),Relation("CITIES")), db)

    exp = SelectionAttribute(Attribute("id"), Attribute("name"), Relation("users"))
    print(exp.get_attributes(db))

    exp2 = Rename(Attribute("name"), Attribute("username"), exp)

    print(exp2.get_attributes(db))

    exp3 = Project(['username'], exp2)

    print(exp3.get_attributes(db))

    exp4 = Join(exp3, Project(['id'], exp2))

    print(exp4.get_attributes(db))

    print(Join(exp2,exp3).get_attributes(db))

    printQuery(Union(exp, exp), db)


    #TODO Unit tests to do : Check if the union correctly checks the attributs if they are not in the same order

    printQuery(Union(Relation("users"), Relation("users2")), db)

    printQuery(Rename(Attribute("name"), Attribute("username"), Relation("users2")), db)

    printQuery(Project(["pw", "name"], Relation("users2")), db)