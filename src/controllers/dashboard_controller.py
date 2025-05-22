from flask import Blueprint, render_template, request
from models.dashboard_data import DashboardData
from utils.decorators import login_required

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
@login_required
def show_dashboard():
    mes = request.args.get('mes', type=int)
    ano = request.args.get('ano', type=int)
    
    # Sempre busca os anos disponíveis
    anos_disponiveis = DashboardData.get_years()
    
    dados = DashboardData.get_dashboard_data(mes=mes, ano=ano)
    dashboard_data = DashboardData.process_dashboard_data(dados)
    
    return render_template('dashboard.html', 
                         dashboard=dashboard_data,
                         total_inscritos=dashboard_data.get('total_inscritos', 0) if dashboard_data else 0,
                         oficinas=dashboard_data.get('oficinas', {}) if dashboard_data else {},
                         faixas_etarias=dashboard_data.get('faixas_etarias', {}) if dashboard_data else {},
                         dados_brutos=dashboard_data.get('dados_brutos', []) if dashboard_data else [],
                         anos_disponiveis=anos_disponiveis,
                         mes_selecionado=mes,
                         ano_selecionado=ano)