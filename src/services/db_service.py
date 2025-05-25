import mysql.connector
import os
from config import Config

class DatabaseService:
    @staticmethod
    def get_connection():
        ENV_DATABASE_HOST = os.getenv("ENV_DATABASE_HOST")
        ENV_DATABASE_NAME = os.getenv("ENV_DATABASE_NAME")
        ENV_DATABASE_PASSWORD = os.getenv("ENV_DATABASE_PASSWORD")
        ENV_DATABASE_PORT = os.getenv("ENV_DATABASE_PORT")
        ENV_DATABASE_USER = os.getenv("ENV_DATABASE_USER")
        ENV_SECRET_KEY = os.getenv("ENV_SECRET_KEY")

        db_config = Config.get_db_config()
        return mysql.connector.connect(
            host=ENV_DATABASE_HOST,
            user=ENV_DATABASE_USER,
            password=ENV_DATABASE_PASSWORD,
            database=ENV_DATABASE_NAME,
            port=ENV_DATABASE_PORT
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