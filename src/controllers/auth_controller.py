from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
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