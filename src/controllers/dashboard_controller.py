from flask import Blueprint, render_template
from models.dashboard_data import DashboardData
from utils.decorators import login_required

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
@login_required
def show_dashboard():
    dados = DashboardData.get_dashboard_data()
    dashboard_data = DashboardData.process_dashboard_data(dados)
    
    if not dashboard_data:
        return render_template('dashboard.html', error="Não foram encontrados dados para exibir.")
    
    return render_template('dashboard.html', 
                         dashboard=dashboard_data,
                         total_inscritos=dashboard_data['total_inscritos'],
                         oficinas=dashboard_data['oficinas'],
                         faixas_etarias=dashboard_data['faixas_etarias'],
                         dados_brutos=dashboard_data['dados_brutos'],
                         anos_disponiveis=dashboard_data['anos_disponiveis'])