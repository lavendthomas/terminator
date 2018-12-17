# SPJRUD to SQL Converter

## Introduction

This library allows you to write database queries and execute them in a SQLite database. The SPJRUD expressions are first checked according to a database pattern and can then be translated to SQL.

This software is written as part of a project for the course of Databases I, given by Professor Jef Wijsen at the University of Mons (UMONS).

## Usage

To use the module, you must first create a `SQLiteDB` object. This is the interface between the SQLite database and the SPJRUD to SQL Converter. To open execute queries using the database stored in the `example.db` file:
```
from algebra import *
db = SQLiteDB("example.db")
```

Once your have a database connector, you can start performing queries, either as `str` or `Expression` by using the `execute()` command. For example:
```
db.execute("SELECT * FROM my_table")
db.execute(Relation("my_table")["id"])
```

Please note that SQL queries sent by text are not checked in any way before executing them on the SQLite connector, whereas SPJRUD are checked before execution.

To save the changes if you made changes to the database, use `commit()`:
```
db.commit()
```


## SPJRUD expressions

### Selection

The selection is separated in two operations: `SelectionConstant` and `SelectionAttribute`.


