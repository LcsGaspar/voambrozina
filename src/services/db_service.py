import mysql.connector
from config import Config

class DatabaseService:
    @staticmethod
    def get_connection():
        db_config = Config.get_db_config()
        return mysql.connector.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["database"],
            port=db_config["port"]
        )

    @staticmethod
    def execute_query(query, params=None, fetch=False):
        connection = None
        cursor = None
        try:
            connection = DatabaseService.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch:
                result = cursor.fetchall()
                return result
            
            connection.commit()
            return True
            
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            if connection:
                connection.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()