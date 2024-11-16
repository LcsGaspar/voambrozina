from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from models.user import User
from utils.decorators import login_required

users = Blueprint('users', __name__)

@users.route('/adicionar_usuario', methods=['POST'])
def adicionar_usuario():
    email = request.form.get('email')
    password = request.form.get('password')

    retorno = User.create(email, password)
    if retorno == True:
        return jsonify({'success': True, 'message': 'Usuário adicionado com sucesso'})
    
    return jsonify({'success': False, 'message': f'Erro ao adicionar usuário!'}), 500


@users.route('/excluir_usuario/<int:user_id>', methods=['POST'])
def excluir_usuario(user_id):
    if user_id == session.get('user_id'):
        return jsonify({'success': False, 'message': 'Não é possível excluir o próprio usuário'}), 400

    retorno = User.delete(user_id)
    if retorno == True:
        return jsonify({'success': True, 'message': 'Usuário removido com sucesso'})
    
    return jsonify({'success': False, 'message': f'Erro ao remover o usuário!'}), 500