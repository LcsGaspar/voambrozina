from flask import Flask, render_template, request, redirect, url_for, session, jsonify, abort
from functools import wraps
import os
import json
import mysql.connector
import hashlib

app = Flask(__name__)

base_dir = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(base_dir, 'static/relatorios')  # Diretório para salvar PDFs
app.config['CONFIG_FILE'] = os.path.join(base_dir, 'config.json')           # Arquivo de configuração
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

def get_db_config():
    filepath = app.config['CONFIG_FILE']
    with open(filepath, 'r') as config_file:
        config = json.load(config_file)
        return config["db_config"]
    
def get_secret_key():
    filepath = app.config['CONFIG_FILE']
    with open(filepath, 'r') as config_file:
        config = json.load(config_file)
        return config["secret_key"]

config = get_db_config()
app.secret_key = get_secret_key()

def connect_to_database(cfgs):
    db_config = cfgs
    return mysql.connector.connect(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        port=db_config["port"]
    )

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

    db = connect_to_database(config)

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
        INSERT INTO inscricoes (nome, email, telefone, data_nascimento, cep, rua, numero, cidade, estado, oficina, mensagem, criado)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
        """
        values = (nome, email, telefone, data_nascimento, cep, rua, numero, cidade, estado, oficina, mensagem)

        cursor.execute(query, values)
        db.commit()

        return '', 204

    except mysql.connector.Error as err:
        print(f"Erro: {err}")
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
            #return redirect(request.url)
            return '', 204
        

        file = request.files['file']
        if file.filename == '':
            #return redirect(request.url)
            return '', 204

        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
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
            db = connect_to_database(config)
            cursor = db.cursor(dictionary=True)

            # Verificar credenciais
            query = "SELECT id, email FROM usuarios WHERE email = %s AND senha = %s"
            cursor.execute(query, (email, hashed_password))
            user = cursor.fetchone()

            if user:
                session['user_id'] = user['id']
                session['user_email'] = user['email']
                return redirect(url_for('usuarios'))

        except mysql.connector.Error as err:
            print(f'Erro ao realizar login: {err}')

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
    return redirect(url_for('login'))

# Função para verificar e criar o usuário padrão
def create_default_user():
    db = connect_to_database(config)
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
                "INSERT INTO usuarios (email, senha, criado) VALUES (%s, %s, CURRENT_TIMESTAMP)",
                ("dados_secretos_dados_secretos_dados_secretos@exemplo.com", default_password)
            )
            db.commit()
            print("Usuário padrão criado com sucesso.")

        else:
            print("Usuários já cadastrados no banco de dados. Nenhuma ação necessária.")

    except mysql.connector.Error as err:
        print(f"Erro ao criar o usuário padrão: {err}")

    finally:
        cursor.close()
        db.close()

################################## AREA DE LOGIN ##################################


################################### GERENCIAMENTO DE USUARIOS ###################################

@app.route('/usuarios')
@login_required
def usuarios():
    try:
        db = connect_to_database(config)
        cursor = db.cursor(dictionary=True)

        # Busca todos os usuários
        cursor.execute("SELECT id, email FROM usuarios")
        usuarios = cursor.fetchall()

        return render_template('usuarios.html', usuarios=usuarios)

    except mysql.connector.Error as err:
        print(f'Erro ao carregar usuários: {err}')
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
        db = connect_to_database(config)
        cursor = db.cursor()

        # Verifica se o email já existe
        cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({'success': False, 'message': 'Email já cadastrado'}), 400

        # Hash da senha
        hashed_password = hashlib.sha256(senha.encode()).hexdigest()

        # Insere novo usuário
        cursor.execute(
            "INSERT INTO usuarios (email, senha, criado) VALUES (%s, %s, CURRENT_TIMESTAMP)",
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
        db = connect_to_database(config)
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
