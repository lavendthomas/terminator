

class NotMatchingAttributesException(Exception): # != names, types or number in 2 tables

    def __init__(self, message):
        super(message)


class InvalidAttributeException(Exception):     # Missing attribute in table or already in the table

    def __init__(self, message):
        super(message)


class DifferentTypeException(Exception):        # type(cst) != type(attr) or type(attr1) != type(attr2)
    def __init__(self, message):
        super(message)



