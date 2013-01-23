from pysqlite2 import dbapi2 as sqlite

database   = "db/web.db"

def run_sql(connection, sql):
  cursor = connection.cursor()
  cursor.execute(sql)
  connection.commit()
  cursor.close()

class Images():
  def __init__(self):
    self.connection = sqlite.connect(database)

  def begin_transaction(self):
    self.cursor     = self.connection.cursor()
  
  def commit_transaction(self):
    self.connection.commit()
    self.cursor.close()

  def insert_image(self, time, image):
    self.cursor.execute('INSERT INTO images VALUES (?, ?, ?, ?, ?, ?, ?, ?);', 
                      ( None
                      , time
                      , image['mission']
                      , image['roll']
                      , image['frame']
                      , image['lat']
                      , image['lon']
                      , 0))
