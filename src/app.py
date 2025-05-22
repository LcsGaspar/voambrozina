from flask import Flask, render_template

def create_app():
    app = Flask(__name__)
    
    from config import Config
    app.config.from_object(Config)
    app.secret_key = Config.get_secret_key()

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

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)