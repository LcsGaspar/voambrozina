from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector

app = Flask(__name__)

# Página inicial
@app.route('/')
@app.route('/home')
def home():
    success_message = request.args.get('success')
    return render_template('index.html', success=success_message)

@app.route('/formulario_antigo')
def formulario():
    return render_template('formulario.html')

@app.route('/formulario')
def novo_formulario():
    return render_template('novo_formulario.html')

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
         host="dados_secretos_dados_secretos_dados_secretos_dados_secretos",
         user="dados_secretos_dados_secretos_dados_secretos_dados_secretos",
         password="dados_secretos_dados_secretos_dados_secretos_dados_secretos",
         database="dados_secretos_dados_secretos_dados_secretos_dados_secretos",
         port=3306  # Use a porta 3306, que é a padrão do MySQL no XAMPP
     )

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

        return redirect(url_for('home', success="Inscrição realizada com sucesso!"))

    except mysql.connector.Error as err:
        print(f"Erro: {err}")
        mensagem = jsonify({"message": "Erro ao realizar inscrição."}), 500
        return '', 204

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

if __name__ == '__main__':
    app.run(debug=True)
