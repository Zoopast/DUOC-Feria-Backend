import oracledb
import os
from configs import config

def get_cursor():
  try:
    connection = oracledb.connect(
      user="Admin",
      password=config.settings.db_password,
      dsn=f"{config.settings.db_public_ip}/{config.settings.db_sid}")

    print("Successfully connected to Oracle Database")

    cursor = connection.cursor()
    return cursor, connection
  except oracledb.Error as error:
    print("Error while connecting to Oracle", error)