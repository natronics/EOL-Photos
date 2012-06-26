#!/usr/bin/env python
from pysqlite2 import dbapi2 as sqlite

database   = "web.db"
connection = sqlite.connect(database)
cursor     = connection.cursor()

sql = """SELECT * FROM images;"""

cursor.execute(sql)

for row in cursor:
  for col in row:
    print col,
  print " "

cursor.close()
