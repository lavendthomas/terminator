class Attribute:

    def __init__(self, attr):
        self.attr = str(attr)

    def toSQL(self, dbschema):
        return self.attr

    def get_attr(self):
        return self.attr

    def __str__(self):
        return self.__class__.__name__ + "(\"" + self.attr + "\")"