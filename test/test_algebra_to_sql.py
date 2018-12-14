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

    def test_selection_attribute(self):
        query = SelectionAttribute(Attribute("id"), Attribute("name"), Relation("users"))
        self.assertEqual(query.toSQL(self.db),"SELECT * FROM users WHERE id = name")

        # Test that the selection doesn't change the attributes
        self.assertEqual(query.get_attributes(self.db).sort(), Relation("users").get_attributes(self.db).sort())

