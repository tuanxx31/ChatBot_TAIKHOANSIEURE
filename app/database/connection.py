import mysql.connector
from config.settings import settings

class DBConnection:
    _instance = None

    @staticmethod
    def get_instance():
        if DBConnection._instance is None:
            DBConnection()
        return DBConnection._instance

    def __init__(self):
        if DBConnection._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            DBConnection._instance = mysql.connector.connect(
                host=settings.MYSQL_HOST,
                user=settings.MYSQL_USER,
                password=settings.MYSQL_PASSWORD,
                database=settings.MYSQL_DB
            )

