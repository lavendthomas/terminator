import sqlite3


class DBSchema:
    """
    Represents a remote which can store and work with information (attributes and their types)
    about one database (but not its data)
    """

    def __init__(self, db=None):
        """
        Constructor of the class DBSchema

        :param db: Database, default value is None
        """
        if db is not None:
            # create table to convert SQL types to our types (e.g. VARCHAR -> TEXT)
            c = sqlite3.connect(db).cursor()

            self.tables = dict()

            for line in c.execute("SELECT name FROM sqlite_master WHERE type = \"table\""):
                table_name = line[0]
                self.tables[table_name] = list()
                for column in c.execute('PRAGMA table_info(' + table_name + ');'):
                    self.tables[table_name].append(Column(column[1], self._get_type_from_sql(column[2])))
        else:
            self.tables = dict()

    def _get_type_from_sql(self, sql_type: str):
        """
        Returns the internal type of the column from the SQL type
        E.g. varchar, char will be converted to "TEXT", int will be converted to "INT",...

        :param sql_type: Type which will be converted to SQL type
        :return: SQL type
        """
        if "int" in sql_type:
            return "INTEGER"
        elif "char" in sql_type:        # also works for varchar
            return "TEXT"
        elif "decimal" in sql_type:
            return "INTEGER"
        elif "date" in sql_type:
            return "DATE"
        elif "float" in sql_type:
            return "REAL"
        elif "blob" in sql_type:
            return "BLOB"
        else:
            return

    def add_table(self, name: str, attributes: list, types: list):
        """
        Adds table with given name, attributes and types of attributes to database
        Raise exception in case that the count of attributes and the count of types are not same

        :param name: The name of the table
        :param attributes: List of attributes
        :param types: List of types of attributes
        """
        if len(attributes) != len(types):
            raise Exception("The count of attributes and the count of types has to be same.")

        self.tables[name] = list()
        for i in range(len(attributes)):
            self.tables[name].append(Column(attributes[i], types[i]))

    def delete_table(self, name: str):
        """
        Deletes table with the given name from database

        :param name: The name of the table
        """
        self.tables.pop(name)

    def is_table(self, name: str):
        """
        Checks if there exists any table with given name in database

        :param name: Name of a table
        :return: True if there exists a table with given name
        """
        return name in self.tables.keys()

    def get_attributes(self, name: str):
        """
        Returns all attributes and their types of given table in form of a map

        :param name: Name of the table
        :return: Attributes with their types
        """
        if name in self.tables.keys():
            return self.tables[name]
        else:
            return dict()


class Column:

    def __init__(self, name: str, type: str):
        """
        Constructor of the class Column

        :param name: The name of the column
        :param type: The type of the column
        """
        self.name = str(name).lower()
        self.type = str(type).upper()

    def get_name(self):
        """
        Return the name of the column (by another name attribute)

        :return: Name of the column
        """
        return self.name

    def get_type(self):
        """
        Returns the type of the column (by another name the type of the attribute)

        :return: Type of the column
        """
        return self.type

    def __eq__(self, other):
        if not isinstance(other, Column):
            return False
        return self.name == other.name and self.type == other.type

    def __str__(self):
        return "[" + self.name + ":" + self.type + "]"

    def __repr__(self):
        return str(self)

    def __lt__(self, other):
        return (self.name, self.type) < (other.name, other.type)

    def __gt__(self, other):
        return (self.name, self.type) > (other.name, other.type)
