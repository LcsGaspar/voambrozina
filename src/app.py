from flask import Flask, render_template, request, redirect, jsonify
import mysql.connector

app = Flask(__name__)

# Página inicial
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/formulario')
def formulario():
    return render_template('formulario.html')

@app.route('/submit_course_registration', methods=['POST'])
def submit_course_registration():

    # Configuração do banco de dados
    # -------------------------------------------------------------------
    # -------------------------->>> ATENÇÃO <<<--------------------------
    # -------------------------------------------------------------------
    # --------- Editar essas configurações abaixo com os dados ----------
    # ---------------- que serão utilizados em produção! ----------------
    # -------------------------------------------------------------------
    db = mysql.connector.connect(
         host="AlexAlmeidaLeonardo.mysql.pythonanywhere-services.com",
         user="AlexAlmeidaLeona",
         password="vo_ambrosina_2024",  # Se a senha estiver em branco, deixe assim
         database="AlexAlmeidaLeona$vo_ambrosina",
         port=3306  # Use a porta 3306, que é a padrão do MySQL no XAMPP
     )

    
    try:
        # Recebendo os dados do formulário
        data = request.form
        nome = data.get('name')
        email = data.get('email')
        telefone = data.get('phone')
        data_nascimento = data.get('dob')
        cep = data.get('cep')
        rua = data.get('rua')
        numero = data.get('numero')
        cidade = data.get('cidade')
        estado = data.get('estado')
        oficina = data.get('course')
        mensagem = data.get('message')

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

        return jsonify({"message": "Inscrição realizada com sucesso!"}), 200

    except mysql.connector.Error as err:
        print(f"Erro: {err}")
        return jsonify({"message": "Erro ao realizar inscrição."}), 500

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

if __name__ == '__main__':
    app.run(debug=True)
