import oracledb
from configs.config import get_settings

settings = get_settings()

def get_cursor():
  try:
    connection = oracledb.connect(
      user=settings.db_user,
      password=settings.db_password,
      dsn=f"{settings.db_public_ip}/{settings.db_sid}")

    print("Successfully connected to Oracle Database")

    cursor = connection.cursor()
    return cursor, connection
  except oracledb.Error as error:
    print("Error while connecting to Oracle", error)