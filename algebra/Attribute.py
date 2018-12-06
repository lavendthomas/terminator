class Attribute:

    def __init__(self, attr):
        self.attr = str(attr)

    def toSQL(self):
        return self.attr

    def get_attr(self):
        return self.attr
