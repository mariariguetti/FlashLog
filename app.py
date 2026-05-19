from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

# login_manager = LoginManager(app)
# login_manager.login_view = 'login'
# login_manager.login_message = 'Por favor, cadastre-se'


# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     db_session.remove()
#
#
# @login_manager.user_loader
# def load_user(user_id):
#     user = select(Funcionario).where(Funcionario.id == int(user_id))
#     resultado = db_session.execute(user).scalar_one_or_none()
#     return resultado


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/login')
def get_funcionario():
    return render_template("login.html")

@app.route('/cadastrar', methods=['POST'])
def post_funcionario():
    return render_template("cadastrar.html")

@app.route('/logistica')
def get_logistica():
    return render_template("logistica.html")

@app.route('/encomendas')
def get_encomendas():
    return render_template("encomendas.html")

@app.route('/clientes')
def get_clientes():
    return render_template("clientes.html")

if __name__ == '__main__':
    app.run(debug=True)


