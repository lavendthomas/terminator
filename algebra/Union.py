from algebra.Expression import Expression
from copy import deepcopy


class Union(Expression):

    def __init__(self, expr1: Expression, expr2: Expression):
        self.expr1 = expr1
        self.expr2 = expr2

    def toSQL(self, dbschema):
        attrs1 = deepcopy(self.expr1.get_attributes(dbschema))
        attrs2 = deepcopy(self.expr2.get_attributes(dbschema))
        attrs1.sort()
        attrs2.sort()

        if len(attrs1) != len(attrs2):
            raise Exception("The number of attributes of " + str(self.expr1) + " and " + str(self.expr2) +
                            " are not the same.")

        for (att1, att2) in zip(attrs1, attrs2):
            if att1 != att2:
                raise Exception("Not same types or names and Fuck you!")

        select_attributes = ""
        for i in range(len(attrs1)):
            select_attributes += attrs1[i].get_name()
            if i != len(attrs1) - 1 :
                select_attributes += ", "

        return "(SELECT " + select_attributes + " FROM (" + self.expr1.toSQL(dbschema) + ")) UNION (SELECT " +\
               select_attributes + " FROM (" + self.expr2.toSQL(dbschema) + "))"

    def get_attributes(self, dbschema):
        return  deepcopy(self.expr1.getAttributes(dbschema))

