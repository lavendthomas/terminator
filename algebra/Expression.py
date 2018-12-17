from algebra.Attribute import Attribute
from algebra.Constant import Constant
from algebra.Exceptions import *
from remote.DBSchema import *
from copy import deepcopy
from typing import Union as _Union
from typing import List


class Expression:

    def __init__(self):
        pass

    def toSQL(self, db_schema):
        return ""

    def get_attributes(self, db_schema):
        """
            Returns a list of all the attributes of the table given by the toSQL() function.
        """
        return []

    def __str__(self):
        return ""

    def __add__(self, other):
        return Union(self, other)

    def __sub__(self, other):
        return Difference(self, other)

    def __mul__(self, other):
        return Join(self, other)

    def __getitem__(self, *items):
        attrs = []
        attrs.extend(items)
        return Project(attrs, self)


class Relation(Expression):

    def __init__(self, table):
        self.table = str(table)

    def toSQL(self, dbschema):
        if not dbschema.is_table(self.table):
            raise Exception("Table " + self.table + " is not in the database.")

        return self.table

    def get_attributes(self, dbschema):
        return dbschema.get_attributes(self.table)

    def __str__(self):
        return "Relation(\"" + self.table + "\")"


class SelectionConstant(Expression):

    def __init__(self, attr: _Union[Attribute, str], cst: _Union[Constant, str, float, int], expr: Expression):
        if isinstance(attr, Attribute):
            self.attr = attr
        else:
            self.attr = Attribute(attr)
        if isinstance(cst, Constant):
            self.cst = cst
        else:
            self.cst = Constant(cst)
        self.expr = expr

    def toSQL(self, dbschema):
        attributes = self.expr.get_attributes(dbschema)
        if self.attr.get_attr() not in map(lambda x:x.get_name(), attributes):
            raise InvalidAttributeException("Attribute " + self.attr.get_attr() + " is not in the table.")

        attr_type = ""
        for col in attributes:
            if col.get_name() == self.attr.get_attr():
                attr_type = col.get_type()
                break

        if attr_type != self.cst.get_type():
            raise DifferentTypeException("Constant " + self.cst.get_cst() + " is not the same type as the attribute.\n "
                                         "Attribute " + self.attr.get_attr() + " is of type " + attr_type + " and the "
                                         "constant of type " + self.cst.get_type() + ".")

        return "SELECT * FROM " + self.expr.toSQL(dbschema) + " WHERE " + self.attr.toSQL(dbschema) + " = " +\
               self.cst.toSQL(dbschema)

    def get_attributes(self, dbschema):
        return deepcopy(self.expr.get_attributes(dbschema))

    def __str__(self):
        return self.__class__.__name__ + "(" + str(self.attr) + ", " + str(self.cst) + ", " + str(self.expr) + ")"


class SelectionAttribute(Expression):

    def __init__(self, attr1: _Union[Attribute, str], attr2: _Union[Attribute, str], expr: Expression):
        if isinstance(attr1, str):
            self.attr1 = Attribute(attr1)
        else:
            self.attr1 = attr1
        if isinstance(attr2, str):
            self.attr2 = Attribute(attr2)
        else:
            self.attr2 = attr2
        self.expr = expr

    def toSQL(self, dbschema):
        attributes = self.expr.get_attributes(dbschema)
        if self.attr1.get_attr() not in map(lambda x: x.get_name(), attributes):
            raise InvalidAttributeException("Attribute " + self.attr1.get_attr() + " is not in the table.")

        if self.attr2.get_attr() not in map(lambda x: x.get_name(), attributes):
            raise InvalidAttributeException("Attribute " + self.attr2.get_attr() + " is not in the table.")

        attr1_type = ""
        attr2_type = ""
        for col in attributes:
            if col.get_name() == self.attr1.get_attr():
                attr1_type = col.get_type()
                break
        for col in attributes:
            if col.get_name() == self.attr2.get_attr():
                attr2_type = col.get_type()
                break

        if attr1_type != attr2_type:
            raise NotMatchingAttributesException("Attributes do not have the same type. \n First attribute is of type "
                                                 + attr1_type + " and second attribute is of type " + attr2_type + ".")

        return "SELECT * FROM " + self.expr.toSQL(dbschema) + " WHERE " + self.attr1.toSQL(dbschema) + " = " +\
               self.attr2.toSQL(dbschema)

    def get_attributes(self, dbschema):
        return deepcopy(self.expr.get_attributes(dbschema))

    def __str__(self):
        return self.__class__.__name__ + "(" + str(self.attr1) + ", " + str(self.attr2) + ", " + str(self.expr) + ")"


class Project(Expression):

    """
    columns: set of attributes to keep
    """
    def __init__(self, columns: List[str], expr: Expression):
        self.columns = columns
        self.expr = expr

    def toSQL(self, dbschema):
        attrs = deepcopy(self.expr.get_attributes(dbschema))

        select_attributes = ""
        for i in range(len(self.columns)):
            if self.columns[i] not in map(lambda x: x.get_name(), attrs):
                raise InvalidAttributeException(self.columns[i] + " not in " + str(self.expr))

            select_attributes += self.columns[i]
            if i != len(self.columns)-1:
                select_attributes += ", "

        if len(self.columns) == 0:
            select_attributes = "NULL"

        return "SELECT DISTINCT " + select_attributes + " FROM (" + self.expr.toSQL(dbschema) + ")"

    def get_attributes(self, dbschema):
        attrs = deepcopy(self.expr.get_attributes(dbschema))
        new_attr = list()
        for i in range(len(attrs)):
            if attrs[i].get_name() in self.columns:
                new_attr.append(attrs[i])

        return new_attr

    def __str__(self):
        col_str = "["
        for i in range(len(self.columns)):
            col_str += "\"" + str(self.columns[i]) + "\""
            if i != len(self.columns)-1:
                col_str += ", "
            else:
                col_str += "]"

        return self.__class__.__name__ + "(" + col_str + ", " + str(self.expr) + ")"


class Join(Expression):

    def __init__(self, expr1: Expression, expr2: Expression):
        self.expr1 = expr1
        self.expr2 = expr2

    def toSQL(self, dbschema):
        attrs1 = deepcopy(self.expr1.get_attributes(dbschema))
        attrs2 = deepcopy(self.expr2.get_attributes(dbschema))

        common_attributes = []
        t2_attributes = []
        for i in range(len(attrs2)):
            if attrs2[i] in attrs1:
                common_attributes.append(attrs2[i])
            else:
                t2_attributes.append(attrs2[i])

        select_attributes = ""
        for i in range(len(attrs1)):
            select_attributes += "t1." + attrs1[i].get_name()
            if i != len(attrs1) - 1:
                select_attributes += ", "
        for i in range(len(t2_attributes)):
            if i == 0:
                select_attributes += ", "
            select_attributes += "t2." + t2_attributes[i].get_name()
            if i != len(t2_attributes) - 1:
                select_attributes += ", "

        if len(select_attributes) == 0:
            select_attributes = "NULL"

        conditions = ""
        if len(t2_attributes) > 0:
            for i in range(len(common_attributes)):
                conditions += "t1." + common_attributes[i].get_name() + " = t2." + common_attributes[i].get_name()
                if i != len(common_attributes) - 1:
                    conditions += " AND "
        if len(conditions) != 0:
            conditions = " WHERE " + conditions

        return "SELECT " + select_attributes + " FROM (" + self.expr1.toSQL(dbschema) + ") AS t1, (" +\
               self.expr2.toSQL(dbschema) + ") AS t2" + conditions

    def get_attributes(self, dbschema):
        attrs1 = self.expr1.get_attributes(dbschema)
        attrs2 = self.expr2.get_attributes(dbschema)
        new_attrs = deepcopy(attrs1)

        for attr in attrs2:
            if attr not in new_attrs:
                new_attrs.append(attr)

        return new_attrs

    def __str__(self):
        return self.__class__.__name__ + "(" + str(self.expr1) + ", " + str(self.expr2) + ")"


class Rename(Expression):

    def __init__(self, from_attr: _Union[Attribute, str], to_attr: _Union[Attribute, str], expr: Expression):
        if isinstance(from_attr, str):
            self.from_attr = Attribute(from_attr)
        else:
            self.from_attr = from_attr
        if isinstance(to_attr, str):
            self.to_attr = Attribute(to_attr)
        else:
            self.to_attr = to_attr
        self.expr = expr

    def toSQL(self, dbschema):
        attrs = deepcopy(self.expr.get_attributes(dbschema))
        if self.to_attr.get_attr() in map(lambda x: x.get_name(), attrs):
            raise InvalidAttributeException("Attribute " + self.to_attr.get_attr() + " is already in the table.")

        from_col = None
        to_col = None

        for i in range(len(attrs)):
            if attrs[i].get_name() == self.from_attr.get_attr():
                from_col = Column(attrs[i].get_name(), attrs[i].get_type())
                to_col = Column(self.to_attr.get_attr(), attrs[i].get_type())
                attrs[i] = to_col
                break

        select_attributes = ""
        for i in range(len(attrs)):
            if attrs[i] == to_col:
                select_attributes += from_col.get_name() + " AS " + to_col.get_name()
            else:
                select_attributes += attrs[i].get_name()
            if i != len(attrs)-1:
                select_attributes += ", "

        return "SELECT " + select_attributes + " FROM (" + self.expr.toSQL(dbschema) + ")"

    def get_attributes(self, dbschema):
        attrs = deepcopy(self.expr.get_attributes(dbschema))

        for i in range(len(attrs)):
            if attrs[i].get_name() == self.from_attr.get_attr():
                attrs[i] = Column(self.to_attr.get_attr(), attrs[i].get_type())
                break

        return attrs

    def __str__(self):
        return self.__class__.__name__ + "(" + str(self.from_attr) + ", " + str(self.to_attr) + ", " +\
               str(self.expr) + ")"


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
            raise NotMatchingAttributesException("The counts of attributes of " + str(self.expr1) + " and " +
                                                 str(self.expr2) + " are not the same.")

        for (att1, att2) in zip(attrs1, attrs2):
            if att1 != att2:
                raise NotMatchingAttributesException("Attributes " + att1.get_attr() + " and " + att2.get_attr() +
                                                     " are not of same type or do not have same names.")

        select_attributes = ""
        for i in range(len(attrs1)):
            select_attributes += attrs1[i].get_name()
            if i != len(attrs1) - 1 :
                select_attributes += ", "

        return "(SELECT " + select_attributes + " FROM (" + self.expr1.toSQL(dbschema) + ")) UNION (SELECT " +\
               select_attributes + " FROM (" + self.expr2.toSQL(dbschema) + "))"

    def get_attributes(self, dbschema):
        return deepcopy(self.expr1.get_attributes(dbschema))

    def __str__(self):
        return self.__class__.__name__ + "(" + str(self.expr1) + ", " + str(self.expr2) + ")"


class Difference(Expression):

    def __init__(self, expr1: Expression, expr2: Expression):
        self.expr1 = expr1
        self.expr2 = expr2

    def toSQL(self, dbschema):
        attrs1 = deepcopy(self.expr1.get_attributes(dbschema))
        attrs2 = deepcopy(self.expr2.get_attributes(dbschema))
        attrs1.sort()
        attrs2.sort()

        if len(attrs1) != len(attrs2):
            raise NotMatchingAttributesException("The counts of attributes of " + str(self.expr1) + " and " +
                                                 str(self.expr2) + " are not the same.")

        for (att1, att2) in zip(attrs1, attrs2):
            if att1 != att2:
                raise NotMatchingAttributesException("Attributes " + att1.get_attr() + " and " + att2.get_attr() +
                                                     " are not of same type or do not have same names.")

        select_attributes1 = ""
        select_attributes2 = ""
        conditions = ""
        for i in range(len(attrs1)):
            select_attributes1 += "t1." + attrs1[i].get_name()
            select_attributes2 += "t2." + attrs1[i].get_name()
            conditions += "t1." + attrs1[i].get_name() + " = t2." + attrs1[i].get_name()
            if i != len(attrs1) - 1:
                select_attributes1 += ", "
                select_attributes2 += ", "
                conditions += " AND "

        return "SELECT " + select_attributes1 + " FROM (" + self.expr1.toSQL(dbschema) + ") AS t1 WHERE NOT EXISTS "\
               "(SELECT " + select_attributes2 + " FROM (" + self.expr2.toSQL(dbschema) + ") AS t2 WHERE " +\
               conditions + ")"

    def get_attributes(self, dbschema):
        return deepcopy(self.expr1.get_attributes(dbschema))

    def __str__(self):
        return self.__class__.__name__ + "(" + str(self.expr1) + ", " + str(self.expr2) + ")"
