from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Configurando a conexão com o MySQL
db_config = db_config = {
    'host': '127.0.0.1',
    'port': '3306',
    'user': 'root',
    'password': 'Arthur17*',
    'database': 'oficina_db'
}

@app.route('/submit_course_registration', methods=['POST'])
def submit_course_registration():
    try:
        # Conectando ao banco de dados
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

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

        # Inserindo os dados no banco de dados
        query = """
        INSERT INTO inscricoes (nome, email, telefone, data_nascimento, cep, rua, numero, cidade, estado, oficina, mensagem)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (nome, email, telefone, data_nascimento, cep, rua, numero, cidade, estado, oficina, mensagem)

        cursor.execute(query, values)
        conn.commit()

        return jsonify({"message": "Inscrição realizada com sucesso!"}), 200

    except mysql.connector.Error as err:
        print(f"Erro: {err}")
        return jsonify({"message": "Erro ao realizar inscrição."}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)
