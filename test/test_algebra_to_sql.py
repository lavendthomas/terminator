import unittest
from algebra import *


class TestAlgebraToSQL(unittest.TestCase):

    def setUp(self):
        self.db = DBSchema()
        self.db.add_table("users",
                 ["id", "name",  "pw"],
                 ["TEXT", "TEXT", "TEXT"])
        self.db.add_table("cities",
                          ["city"],
                          ["TEXT"])

    def test_selection_constant(self):
        query = SelectionConstant(Attribute("city"), Constant("Mons"), Relation("cities"))
        self.assertEqual(query.toSQL(self.db), "SELECT * FROM cities WHERE city = \"Mons\"")

        # Test that the selection doesn't change the attributes
        self.assertEqual(query.get_attributes(self.db).sort(), Relation("cities").get_attributes(self.db).sort())

    def test_selection_constant_attribute_not_in_table(self):
        # Test if the attribute is not in the table
        badquery = SelectionConstant(Attribute("notacity"), Constant("Mons"), Relation("cities"))
        with self.assertRaises(InvalidAttributeException):
            badquery.toSQL(self.db)

    def test_selection_constant_constant_different_type_as_attribute(self):
        # Test if the constant is not the same type as the attribute
        badquery = SelectionConstant(Attribute("city"), Constant(1), Relation("cities"))
        with self.assertRaises(DifferentTypeException):
            badquery.toSQL(self.db)

    def test_selection_attribute(self):
        query = SelectionAttribute(Attribute("id"), Attribute("name"), Relation("users"))
        self.assertEqual(query.toSQL(self.db),"SELECT * FROM users WHERE id = name")

        # Test that the selection doesn't change the attributes
        self.assertEqual(query.get_attributes(self.db).sort(), Relation("users").get_attributes(self.db).sort())

    def test_selection_attribute_attribute_not_in_table(self):
        # Test if the attribute is not in the table
        badquery = SelectionAttribute(Attribute("notid"), Attribute("name"), Relation("users"))
        with self.assertRaises(InvalidAttributeException):
            badquery.toSQL(self.db)

    def test_project(self):
        query = Project(["id"], Relation("users"))
        self.assertTrue("id" in map(lambda x: x.get_name(), query.get_attributes(self.db)))
        self.assertFalse("name" in map(lambda x: x.get_name(), query.get_attributes(self.db)))

    def test_project_empty(self):
        query = Project([], Relation("users"))
        self.assertTrue(len(query.get_attributes(self.db)) == 0)
        self.assertEqual(query.toSQL(self.db), "SELECT DISTINCT NULL FROM (users)")

    def test_project_shortcut(self):
        query1 = Project(["id"], Relation("users"))
        query2 = Relation("users")["id"]
        self.assertEqual(query1.toSQL(self.db), query2.toSQL(self.db))

    def test_empty_join(self):
        query = Join(Project([], Relation("users")),Project([], Relation("users")))
        self.assertTrue(len(query.get_attributes(self.db)) == 0)

    def test_join_shortcut(self):
        query1 = Join(Relation("users"), Relation("users"))
        query2 = Relation("users") * Relation("users")
        self.assertEqual(query1.toSQL(self.db), query2.toSQL(self.db))

    def test_rename(self):
        query = Rename("id", "notid", Relation("users"))
        self.assertFalse("id" in map(lambda x: x.get_name(), query.get_attributes(self.db)))
        self.assertTrue("notid" in map(lambda x: x.get_name(), query.get_attributes(self.db)))
