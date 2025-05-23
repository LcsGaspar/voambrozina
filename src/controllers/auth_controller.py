from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from models.oficina import Oficina
from models.user import User
from utils.decorators import login_required

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.find_by_credentials(email, password)
        if user:
            session['user_id'] = user.id
            session['user_email'] = user.email
            return redirect(url_for('auth.usuarios'))

    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@auth.route('/usuarios')
@login_required
def usuarios():
    usuarios = User.get_all()
    return render_template('usuarios.html', usuarios=usuarios)

#@auth.route('/dashboard')
#@login_required
#def dashboard():
#    oficinas = Oficina.get_all()
#
#    """ oficinas = [
#        {"id_oficina": 1, "nome_oficina": "Informática"},
#        {"id_oficina": 2, "nome_oficina": "Clubinho de Inglês"},
#        {"id_oficina": 3, "nome_oficina": "Educação Ambiental"},
#        {"id_oficina": 4, "nome_oficina": "Inclusão Digital"},
#        {"id_oficina": 5, "nome_oficina": "Pequeninos"},
#        {"id_oficina": 6, "nome_oficina": "Mundo Digital"},
#        {"id_oficina": 7, "nome_oficina": "Projeto de vida"},
#    ] """
#    return render_template('dashboard.html', oficinas=oficinas)
