

class NotMatchingAttributesException(Exception):
    """
    Exception is raised when names or types of attributes of two tables are not matching or when the counts of
    attributes of two tables are not matching
    """
    pass


class InvalidAttributeException(Exception):
    """
    Exception is raised when attribute does not correspond with rules of relational algebra
    """
    pass


class DifferentTypeException(Exception):
    """
    Exception is raised when types of two attributes or types of an attribute and a constant are not the same
    """
    pass


