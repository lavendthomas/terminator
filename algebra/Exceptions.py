

class NotMatchingAttributesException(Exception): # != names, types or number in 2 tables

    pass


class InvalidAttributeException(Exception):     # Missing attribute in table or already in the table

    pass


class DifferentTypeException(Exception):        # type(cst) != type(attr) or type(attr1) != type(attr2)

    pass


