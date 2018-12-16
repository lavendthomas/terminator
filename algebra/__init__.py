from algebra.Expression import *
from remote.DBSchema import *
from remote.sqlite import SQLiteDB

def printQuery(query, dbschema):
    print(query.toSQL(dbschema) + ";")

if __name__ == "__main__":

    db = DBSchema()
    db.add_table("users",
                 ["id", "name",  "pw"],
                 ["TEXT", "TEXT", "TEXT"])
    db.add_table("users2",
                 ["name", "id", "pw"],
                 ["TEXT", "TEXT", "TEXT"])
    db.add_table("CITIES",
                 ["city"],
                 ["TEXT"])

    print(Constant("test").toSQL(db))
    print(Attribute("test").toSQL(db))


    printQuery(SelectionConstant(Attribute("city"), Constant("Mons"), Relation("CITIES")), db)

    exp0 = SelectionAttribute(Attribute("id"), Attribute("name"), Relation("users"))
    printQuery(exp0, db)
    exp1 = SelectionAttribute(Attribute("id"), Attribute("name"), Relation("users2"))
    print(exp0.get_attributes(db))

    exp2 = Rename(Attribute("name"), Attribute("username"), exp0)

    print(exp2.get_attributes(db))

    exp3 = Project(['username'], exp2)

    print(exp3.get_attributes(db))

    exp4 = Join(exp3, Project(['id'], exp2))

    printQuery(exp4, db)

    print(exp4.get_attributes(db))

    print(Join(exp2, exp3).get_attributes(db))

    printQuery(Union(exp0, exp0), db)


    #TODO Unit tests to do : Check if the union correctly checks the attributs if they are not in the same order

    printQuery(Union(Relation("users"), Relation("users2")), db)

    printQuery(Rename(Attribute("name"), Attribute("username"), Relation("users2")), db)

    printQuery(Project(["pw", "name"], Relation("users2")), db)

    printQuery(Difference(exp0, exp1), db)

    printQuery(Join(exp0,exp2),db)

    experiment = SelectionConstant(Attribute("city"), Constant("Mons"), Relation("CITIES"))
    experiment2 = Rename(Attribute("name"), Attribute("username"), Relation("users2"))
    print("\n\n\n\n" + experiment2.__str__())

    e1 = Join(Relation("emp"), Relation("emp"))
    e2 = SelectionConstant("ename", "SMITH", Relation("emp"))
    e3 = SelectionConstant("empno", 7369, Relation("emp"))
    e4 = e3["ename"] * Relation("emp")["empno"]
    d = SQLiteDB("/home/thomas/Documents/École/Université/BA2 - Info/Bases de données 1/Projet/terminator/remote/test")
    d.execute("DELETE FROM emp")
    d.execute("INSERT INTO `emp` VALUES (7369,'SMITH','CLERK',7902,'2000-12-17',800.00,NULL,20),(7499,'ALLEN','SALESMAN',7698,'2001-02-20',1600.00,300.00,30),(7521,'WARD','SALESMAN',7698,'2001-02-22',1250.00,500.00,30),(7566,'JONES','MANAGER',7839,'2001-04-02',2975.00,NULL,20),(7654,'MARTIN','SALESMAN',7698,'2001-09-28',1250.00,1400.00,30),(7698,'BLAKE','MANAGER',7839,'2001-05-01',2850.00,NULL,30),(7782,'CLARK','MANAGER',7839,'2001-06-09',2450.00,NULL,10),(7788,'SCOTT','ANALYST',7566,'2002-12-09',3000.00,NULL,20),(7839,'KING','PRESIDENT',NULL,'2001-11-17',5000.00,NULL,10),(7844,'TURNER','SALESMAN',7698,'2001-09-08',1500.00,0.00,30),(7876,'ADAMS','CLERK',7788,'2003-01-12',1100.00,NULL,20),(7900,'JAMES','CLERK',7698,'2001-12-03',950.00,NULL,30),(7902,'FORD','ANALYST',7566,'2001-12-03',3000.00,NULL,20),(7934,'MILLER','CLERK',7902,'2002-01-23',1300.00,NULL,10),(7939,'PALMER','ANALYST',7902,'2012-01-23',1300.00,NULL,10),(7983,'LOPEZ','SALESMAN',7566,'2012-01-23',1500.00,600.00,20),(7994,'WILLIAMS','ANALYST',7698,'2012-01-23',950.00,NULL,30);")
    print(d.toSQL(e4))
    print(e4)
    d.execute(e4)
