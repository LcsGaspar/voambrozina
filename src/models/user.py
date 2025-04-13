from services.db_service import DatabaseService
import hashlib

class User:
    def __init__(self, id=None, email=None):
        self.id = id
        self.email = email

    @staticmethod
    def find_by_credentials(email, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        query = "SELECT id, email FROM usuarios WHERE email = %s AND senha = %s"
        result = DatabaseService.execute_query(query, (email, hashed_password), fetch=True)
        return User(**result[0]) if result else None

    @staticmethod
    def create(email, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        query = """
        INSERT INTO usuarios (email, senha, criado)
        VALUES (%s, %s, CURRENT_TIMESTAMP)
        """
        return DatabaseService.execute_query(query, (email, hashed_password))

    @staticmethod
    def delete(user_id):
        query = "DELETE FROM usuarios WHERE id = %s"
        return DatabaseService.execute_query(query, (user_id,))

    @staticmethod
    def get_all():
        query = "SELECT id, email FROM usuarios"
        return DatabaseService.execute_query(query, fetch=True)