from services.database import Database

class BaseService:
    def __init__(self):
        self.__db = Database()

    def _get_db_connection(self):
        return self.__db.get_connection()