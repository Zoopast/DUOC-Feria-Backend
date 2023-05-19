import cx_Oracle
from configs.config import get_settings
from functools import lru_cache

settings = get_settings()

@lru_cache()
def get_cursor():
    try:
        dsn = cx_Oracle.makedsn(
            settings.db_public_ip,
            settings.db_port,
            sid=settings.db_sid
        )
        connection = cx_Oracle.connect(
            settings.db_user,
            settings.db_password,
            dsn,
            encoding="UTF-8"
        )
        print("Successfully connected to Oracle Database")

        cursor = connection.cursor()
        return cursor, connection
    except cx_Oracle.Error as error:
        print("Error while connecting to Oracle:", error)

    return None, None

