from services.db_service import DatabaseService

class DashboardData:
    @staticmethod
    def get_dashboard_data(mes=None, ano=None):
        query = """
        SELECT 
            id_inscricao, 
            nome Nome,
            TIMESTAMPDIFF(YEAR, data_nascimento, CURDATE()) AS Idade,
            o.nome_oficina Oficinas, 
            date(criado) as data,
            MONTH(criado) as mes,
            YEAR(criado) as ano,
            case
                when TIMESTAMPDIFF(YEAR, data_nascimento, CURDATE()) <= 15 then 'Jovem'
                when TIMESTAMPDIFF(YEAR, data_nascimento, CURDATE()) >= 16 
                     or TIMESTAMPDIFF(YEAR, data_nascimento, CURDATE()) <= 64 then 'Adulto'
                else 'Idoso'
            end as Faixa_Etaria
        FROM inscricoes i 
        join oficinas o on i.oficina = o.id_oficina
        WHERE 1=1
        """
        
        params = []
        if mes:
            query += " AND MONTH(criado) = %s"
            params.append(mes)
        if ano:
            query += " AND YEAR(criado) = %s"
            params.append(ano)
            
        return DatabaseService.execute_query(query, params=params, fetch=True)

    @staticmethod
    def get_years():
        query = """
        SELECT DISTINCT YEAR(criado) as ano 
        FROM inscricoes 
        ORDER BY ano DESC
        """
        result = DatabaseService.execute_query(query, fetch=True)
        return [str(row['ano']) for row in result] if result else []

    @staticmethod
    def get_months_with_data():
        query = """
        SELECT DISTINCT MONTH(criado) as mes 
        FROM inscricoes 
        ORDER BY mes
        """
        result = DatabaseService.execute_query(query, fetch=True)
        return [str(row['mes']) for row in result] if result else []

    @staticmethod
    def process_dashboard_data(dados):
        if not dados:
            return None

        total_inscritos = len(dados)
        
        # Contagem por oficina
        oficinas = {}
        for registro in dados:
            oficina = registro['Oficinas']
            oficinas[oficina] = oficinas.get(oficina, 0) + 1

        # Distribuição por faixa etária
        faixas_etarias = {
            'Jovem': 0,
            'Adulto': 0,
            'Idoso': 0
        }
        for registro in dados:
            faixa = registro['Faixa_Etaria']
            faixas_etarias[faixa] += 1

        anos_disponiveis = DashboardData.get_years()

        return {
            'total_inscritos': total_inscritos,
            'oficinas': oficinas,
            'faixas_etarias': faixas_etarias,
            'dados_brutos': dados,
            'anos_disponiveis': anos_disponiveis
        }