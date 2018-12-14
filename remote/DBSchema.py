import sqlite3

class DBSchema:

    def __init__(self, db=None):
        if db is not None:
            # TODO load tables from database
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

    """
    Returns the internal type of the column from the SQL type.
    E.g. varchar, char will be converted to "TEXT",
         int will be converted to "INT",...
    """
    def _get_type_from_sql(self, sql_type: str):
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
            return                      # TODO handle unknown formats


    def add_table(self, name, attributes : list, types : list):
        if len(attributes) != len(types):
            raise Exception("Fuck You!")

        self.tables[name] = list()
        for i in range(len(attributes)):
            self.tables[name].append(Column(attributes[i], types[i]))

    def delete_table(self, name):
        self.tables.pop(name)

    def is_table(self, name):
        return name in self.tables.keys()

    def get_attributes(self, table):
        if table in self.tables.keys():
            return self.tables[table]
        else:
            return dict()


class Column:

    def __init__(self, name, type):
        self.name = str(name).lower()
        self.type = str(type).upper()

    def get_name(self):
        return self.name

    def get_type(self):
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
