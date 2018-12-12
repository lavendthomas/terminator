class DBSchema:

    def __init__(self, db=None):
        if db is not None:
            # load tables from database
            pass
        else:
            self.tables = dict()

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
        return self.tables[table]


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
