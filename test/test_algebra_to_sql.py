import unittest
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
from remote.DBSchema import DBSchema
from algebra.Exceptions import *


class TestAlgebraToSQL(unittest.TestCase):

    def setUp(self):
        self.db = DBSchema()
        self.db.add_table("users",
                 ["id", "name",  "pw"],
                 ["TEXT", "TEXT", "TEXT"])
        self.db.add_table("CITIES",
                          ["city"],
                          ["TEXT"])

    def test_selection_constant(self):
        query = SelectionConstant(Attribute("city"), Constant("Mons"), Relation("CITIES"))
        self.assertEqual(query.toSQL(self.db), "SELECT * FROM CITIES WHERE city = \"Mons\"")

        # Test that the selection doesn't change the attributes
        self.assertEqual(query.get_attributes(self.db).sort(), Relation("CITIES").get_attributes(self.db).sort())

    def test_selection_constant_attribute_not_in_table(self):
        # Test if the attribute is not in the table
        badquery = SelectionConstant(Attribute("notacity"), Constant("Mons"), Relation("CITIES"))
        with self.assertRaises(InvalidAttributeException):
            badquery.toSQL(self.db)

    def test_selection_constant_constant_different_type_as_attribute(self):
        # Test if the constant is not the same type as the attribute
        badquery = SelectionConstant(Attribute("city"), Constant(1), Relation("CITIES"))
        with self.assertRaises(DifferentTypeException):
            badquery.toSQL(self.db)


    def test_selection_attribute(self):
        query = SelectionAttribute(Attribute("id"), Attribute("name"), Relation("users"))
        self.assertEqual(query.toSQL(self.db),"SELECT * FROM users WHERE id = name")

        # Test that the selection doesn't change the attributes
        self.assertEqual(query.get_attributes(self.db).sort(), Relation("users").get_attributes(self.db).sort())

    def test_selection_attribute_attribute_not_in_table(self):
        # Test if the attribute is not in the table
        badquery = SelectionAttribute(Attribute("id"), Attribute("name"), Relation("users")
        with self.assertRaises(InvalidAttributeException):
            badquery.toSQL(self.db)
