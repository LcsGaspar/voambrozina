from services.db_service import DatabaseService

class Registration:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @staticmethod
    def create(data):
        query = """
        INSERT INTO inscricoes (
            nome, email, telefone, data_nascimento, 
            cep, rua, numero, cidade, estado, 
            oficina, mensagem, criado, bairro
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            CURRENT_TIMESTAMP, %s
        )
        """
        values = (
            data.get('nome'), data.get('email'), data.get('telefone'), data.get('data_nascimento'),
            data.get('cep'), data.get('rua'), data.get('numero'), data.get('cidade'), data.get('estado'),
            data.get('course'), data.get('observacoes'), data.get('bairro')
        )
        return DatabaseService.execute_query(query, values)