from services.db_service import DatabaseService

class Oficina:
    @staticmethod
    def get_all():
        query = "SELECT * FROM oficinas"
        return DatabaseService.execute_query(query, fetch=True)