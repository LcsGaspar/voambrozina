from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, abort
from functools import wraps
import os
import mysql.connector
import hashlib

app = Flask(__name__)
app.secret_key = 'dados_secretos_dados_secretos_dados_secretos'
app.config['UPLOAD_FOLDER'] = './static/relatorios'  # Diretório para salvar PDFs
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Configuração do banco de dados
# -------------------------------------------------------------------
# -------------------------->>> ATENÇÃO <<<--------------------------
# -------------------------------------------------------------------
# --------- Editar essas configurações abaixo com os dados ----------
# ---------------- que serão utilizados em produção! ----------------
# -------------------------------------------------------------------

DB_CONFIG = {
    "host": "dados_secretos_dados_secretos_dados_secretos",
    "user": "dados_secretos_dados_secretos_dados_secretos",
    "password": "dados_secretos_dados_secretos_dados_secretos",
    "database": "dados_secretos_dados_secretos_dados_secretos",
    "port": 3306
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Página inicial
@app.route('/')
@app.route('/home')
def home():
    success_message = request.args.get('success')
    return render_template('index.html', success=success_message)

@app.route('/alternativo')
def home_alternativo():
    success_message = request.args.get('success')
    return render_template('index_alternativo.html', success=success_message)

@app.route('/formulario_antigo')
def formulario():
    return render_template('formulario.html')

@app.route('/formulario')
def novo_formulario():
    return render_template('novo_formulario.html')

@app.route('/submit_course_registration', methods=['POST'])
def submit_course_registration():

    db = mysql.connector.connect(**DB_CONFIG)

    try:
        data = request.form
        nome = data.get('nome')
        email = data.get('email')
        telefone = data.get('telefone')
        data_nascimento = data.get('data_nascimento')
        cep = data.get('cep')
        rua = data.get('rua')
        numero = data.get('numero')
        cidade = data.get('cidade')
        estado = data.get('estado')
        oficina = data.get('course')
        mensagem = data.get('observacoes')

        # Conectando ao banco de dados
        cursor = db.cursor()

        # Inserindo os dados no banco de dados
        query = """
        INSERT INTO inscricoes (nome, email, telefone, data_nascimento, cep, rua, numero, cidade, estado, oficina, mensagem)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (nome, email, telefone, data_nascimento, cep, rua, numero, cidade, estado, oficina, mensagem)

        cursor.execute(query, values)
        db.commit()

        flash("Inscrição realizada com sucesso!")
        return '', 204

    except mysql.connector.Error as err:
        print(f"Erro: {err}")

        flash("Erro ao realizar inscrição.", "error")
        return '', 204

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

# Função para upload de arquivo
@app.route('/upload_pdf', methods=['GET', 'POST'])
def upload_pdf():
    # Processa o upload se o método for POST
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Nenhum arquivo selecionado')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            # flash('Nenhum arquivo selecionado')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # flash('Upload realizado com sucesso')
            return redirect(url_for('upload_pdf'))

    # Obtém a lista de arquivos do diretório
    arquivos = os.listdir(app.config['UPLOAD_FOLDER'])
    arquivos = [f for f in arquivos if f.endswith('.pdf')]  # Filtra para apenas arquivos PDF
    return render_template('upload_pdf.html', arquivos=arquivos)


# Função para deletar arquivo
@app.route('/delete_pdf/<filename>', methods=['POST'])
def delete_pdf(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        # flash(f'{filename} excluído com sucesso')
#    else:
#        flash('Arquivo não encontrado')
    return redirect(url_for('upload_pdf'))

@app.route('/listar_pdfs')
def listar_pdfs():
    # Coleta todos os arquivos PDF do diretório
    caminho = app.config['UPLOAD_FOLDER']

    # Verifica se o diretório existe
    if not os.path.exists(caminho) or not os.path.isdir(caminho):
        # Se o diretório não existir, você pode retornar um erro 404 ou uma mensagem apropriada
        abort(404)  # ou você pode retornar um render_template com uma mensagem de erro

    arquivos = [f for f in os.listdir(caminho) if f.endswith('.pdf')]  # Lista apenas arquivos PDF
    return render_template('listar_pdfs.html', arquivos=arquivos)

################################## AREA DE LOGIN ##################################

# Decorator para verificar se o usuário está logado
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, faça login para acessar esta página.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    create_default_user()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Hash da senha
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            db = mysql.connector.connect(**DB_CONFIG)
            cursor = db.cursor(dictionary=True)

            # Verificar credenciais
            query = "SELECT id, email FROM usuarios WHERE email = %s AND senha = %s"
            cursor.execute(query, (email, hashed_password))
            user = cursor.fetchone()

            if user:
                session['user_id'] = user['id']
                session['user_email'] = user['email']
                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('usuarios'))
            else:
                flash('Email ou senha incorretos.', 'error')

        except mysql.connector.Error as err:
            flash(f'Erro ao realizar login: {err}', 'error')

        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    return render_template('login.html')

# Rota de logout
@app.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('login'))

# Função para verificar e criar o usuário padrão
def create_default_user():
    db = mysql.connector.connect(**DB_CONFIG)
    cursor = db.cursor()

    try:
        # Verifica se existe algum usuário cadastrado no banco de dados
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        result = cursor.fetchone()

        if result and result[0] == 0:
            # Hash da senha padrão
            default_password = hashlib.sha256("dados_secretos_dados_secretos_dados_secretos".encode()).hexdigest()

            # Criação do usuário padrão com email e senha
            cursor.execute(
                "INSERT INTO usuarios (email, senha) VALUES (%s, %s)",
                ("dados_secretos_dados_secretos_dados_secretos@exemplo.com", default_password)
            )
            db.commit()
            print("Usuário padrão criado com sucesso.")
            #flash('Usuário padrão criado com sucesso!', 'success')

        else:
            print("Usuários já cadastrados no banco de dados. Nenhuma ação necessária.")
            #flash('Usuários já cadastrados no banco de dados. Nenhuma ação necessária.', 'error')

    except mysql.connector.Error as err:
        print(f"Erro ao criar o usuário padrão: {err}")
        #flash(f"Erro ao criar o usuário padrão: {err}", 'error')

    finally:
        cursor.close()
        db.close()

################################## AREA DE LOGIN ##################################


################################### GERENCIAMENTO DE USUARIOS ###################################

@app.route('/usuarios')
@login_required
def usuarios():
    try:
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor(dictionary=True)

        # Busca todos os usuários
        cursor.execute("SELECT id, email FROM usuarios")
        usuarios = cursor.fetchall()

        return render_template('usuarios.html', usuarios=usuarios)

    except mysql.connector.Error as err:
        flash(f'Erro ao carregar usuários: {err}', 'error')
        return redirect(url_for('home'))

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

@app.route('/adicionar_usuario', methods=['POST'])
@login_required
def adicionar_usuario():
    email = request.form.get('email')
    senha = request.form.get('password')

    if not email or not senha:
        return jsonify({'success': False, 'message': 'Email e senha são obrigatórios'}), 400

    try:
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor()

        # Verifica se o email já existe
        cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({'success': False, 'message': 'Email já cadastrado'}), 400

        # Hash da senha
        hashed_password = hashlib.sha256(senha.encode()).hexdigest()

        # Insere novo usuário
        cursor.execute(
            "INSERT INTO usuarios (email, senha) VALUES (%s, %s)",
            (email, hashed_password)
        )
        db.commit()

        return jsonify({'success': True, 'message': 'Usuário adicionado com sucesso'})

    except mysql.connector.Error as err:
        return jsonify({'success': False, 'message': f'Erro ao adicionar usuário: {err}'}), 500

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

@app.route('/excluir_usuario/<int:user_id>', methods=['POST'])
@login_required
def excluir_usuario(user_id):
    if user_id == session.get('user_id'):
        return jsonify({'success': False, 'message': 'Não é possível excluir o próprio usuário'}), 400

    try:
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor()

        # Exclui o usuário
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
        db.commit()

        if cursor.rowcount > 0:
            return jsonify({'success': True, 'message': 'Usuário excluído com sucesso'})
        else:
            return jsonify({'success': False, 'message': 'Usuário não encontrado'}), 404

    except mysql.connector.Error as err:
        return jsonify({'success': False, 'message': f'Erro ao excluir usuário: {err}'}), 500

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

################################### GERENCIAMENTO DE USUARIOS ###################################

if __name__ == '__main__':
    create_default_user()  # Criação do usuário padrão se necessário
    app.run(debug=True)
