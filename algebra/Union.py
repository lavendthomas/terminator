from algebra.Expression import Expression as Expr
from copy import deepcopy


class Union(Expr):

    def __init__(self, expr1, expr2):
        self.nodes = [expr1, expr2]

    def toSQL(self, dbschema):
        a = deepcopy(self.nodes[0].get_attributes(dbschema))            #TODO change variable names
        b = deepcopy(self.nodes[1].get_attributes(dbschema))
        a.sort()
        b.sort()

        if len(a) != len(b):
            raise Exception("The number of attributes of " + str(self.nodes[0]) + " and " + str(self.nodes[1]) + " are not the same.")

        for (att1, att2) in zip(a, b):
            if att1 != att2:
                raise Exception("Not same types or names and Fuck you!")

        select_attributes = ""
        for i in range(len(a)):
            select_attributes += a[i].get_name()
            if i != len(a) -1 :
                select_attributes += ", "

        return "(SELECT " + select_attributes + " FROM (" + self.nodes[0].toSQL(dbschema) + ")) UNION (SELECT " + select_attributes + " FROM (" + self.nodes[1].toSQL(dbschema) + "))"

    def get_attributes(self, dbschema):
        return  deepcopy(self.nodes[0].getAttributes(dbschema))

