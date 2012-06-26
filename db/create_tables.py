#!/usr/bin/env python
from pysqlite2 import dbapi2 as sqlite
import sqlite as db

# Create the images Table
def create_images():
  connection = sqlite.connect(db.database)
  
  sql  = """CREATE TABLE images
            (   image_id      INTEGER PRIMARY KEY
              , collect_date  INTEGER
              , mission       TEXT    NOT NULL
              , roll          TEXT    NOT NULL
              , frame         INTEGER NOT NULL
              , nadir_lat     REAL
              , nadir_lon     REAL
              , posted        INTEGER DEFAULT(0)
            );"""
  db.run_sql(connection, sql)

def drop_images():
  connection = sqlite.connect(db.database)
  
  sql  = "DROP TABLE images;"
  
  db.run_sql(connection, sql)

# Build out the table structure
drop_images()
create_images()
