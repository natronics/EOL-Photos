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

def get_images(galid):
  images     = []
  connection = sqlite.connect(database)
  cursor     = connection.cursor()
  
  sql = """SELECT 
                    images.collect_date AS id
                  , images.mission
                  , images.roll
                  , images.frame
           FROM  images
           WHERE images.collect_date = '%d';""" % galid
  
  cursor.execute(sql)
  
  for row in cursor:
    mission = str(row[1])
    roll    = str(row[2])
    frame   = int(row[3])
    images.append({"mission": mission, "roll": roll, "frame": frame})
  
  cursor.close()
  connection.close()
  
  return images
  
def get_dates():
  dates      = []
  connection = sqlite.connect(database)
  cursor     = connection.cursor()
  
  sql = """SELECT 
                    images.collect_date AS id
                  , strftime('%Y-%m-%d', images.collect_date, 'unixepoch') AS Date
                  , COUNT(*) AS num
           FROM images
           GROUP BY images.collect_date
           ORDER BY Date DESC;"""
  
  cursor.execute(sql)
  
  for row in cursor:
    galid = int(row[0])
    date  = str(row[1])
    n     = int(row[2])
    dates.append(("%s &mdash; %d photos" % (date, n), galid))
  
  cursor.close()
  connection.close()
  return dates
