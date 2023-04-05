import oracledb
from configs import config

settings = config.Settings()

def get_cursor():
  try:
    connection = oracledb.connect(
      user="Admin",
      password="DuocAdmin@2023",
      dsn=f"13.72.86.125/oratest2")

    print("Successfully connected to Oracle Database")

    cursor = connection.cursor()
    return cursor, connection
  except oracledb.Error as error:
    print("Error while connecting to Oracle", error)