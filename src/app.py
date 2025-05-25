from flask import Flask, render_template, request
import os

def create_app():
    app = Flask(__name__)
    
    from config import Config
    app.config.from_object(Config)
    app.secret_key = os.getenv("ENV_SECRET_KEY")  #Config.get_secret_key()

    # Register blueprints
    from controllers.auth_controller import auth
    from controllers.registration_controller import registration
    from controllers.pdf_controller import pdf
    from controllers.user_controller import users
    from controllers.dashboard_controller import dashboard

    app.register_blueprint(auth)
    app.register_blueprint(registration)
    app.register_blueprint(pdf)
    app.register_blueprint(users)
    app.register_blueprint(dashboard)    

    # Register main routes
    @app.route('/')
    @app.route('/index')
    @app.route('/home')
    def home():
        return render_template('index.html')

    @app.route('/alternativo')
    def home_alternativo():
        return render_template('index_alternativo.html')

    @app.route('/formulario')
    def novo_formulario():
        return render_template('novo_formulario.html')

    @app.route('/inscricao', methods=['POST'])
    def inscricao():
        # Adicione logs para debug
        print("Formulário recebido:", request.form)
        print("Bairro:", request.form.get('bairro'))
        
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        cpf = request.form.get('cpf')
        rg = request.form.get('rg')
        cep = request.form.get('cep')
        rua = request.form.get('rua')
        numero = request.form.get('numero')
        bairro = request.form.get('bairro')
        cidade = request.form.get('cidade')
        estado = request.form.get('estado')
        
        # Na query SQL, adicione o campo bairro
        cursor.execute("""
            INSERT INTO inscricoes (
                nome, email, telefone, cpf, rg, 
                cep, rua, numero, bairro, cidade, estado
            ) VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s
            )
        """, (
            nome, email, telefone, cpf, rg,
            cep, rua, numero, bairro, cidade, estado
        ))

        return 'Inscrição recebida com sucesso!'

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)