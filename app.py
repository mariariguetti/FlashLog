from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user, UserMixin

from routes.route import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, cadastre-se'

class User(UserMixin):
    def __init__(self, id, nome,data_nascimento,email,perfil):
        self.id = id
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.email = email
        self.perfil = perfil

@login_manager.user_loader
def load_user(user_id):
    resultado = logar_user(user_id)
    return resultado

@app.route('/')
def home():
    encomendas = get_encomenda()['encomendas']
    clientes = get_cliente()['clientes']
    print('enco',encomendas)
    print('clie',clientes)
    return render_template("base.html",var_encomendas=encomendas,var_clientes=clientes)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("form-email")
        senha = request.form.get("form-senha")

        if not(email and senha):
            print(f'error: valores invalidos')
            return render_template("login.html")
        else:
            user = post_login(email, senha)
            print(user)
            if user:
                perfil = user['perfil_status']
                usuario = User(nome=perfil["nome"], email=perfil["email"], id=perfil["id"], data_nascimento=perfil["data_nascimento"], perfil=perfil["perfil"])
                print(usuario)
                login_user(usuario)
                return redirect(url_for("home"))
            else:
                print(f'error')
                return redirect(url_for("login"))
    return render_template("login.html")

@app.route('/logout')
def logout():
    logout_user()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('home'))

@app.route('/cadastrar_funcionario', methods=['POST'])
def post_funcionario():
    if request.method == 'POST':
        nome = request.form.get("form-nome")
        data_nascimento = request.form.get("form-nascimento")
        email = request.form.get("form-email")
        senha = request.form.get("form-senha")
        perfil = request.form.get("form-perfil")
        if not(nome and data_nascimento and email and senha and perfil):
            print(f'error: valores invalidos')
            return redirect(url_for("login"))
        try:
            new_user = post_usuario(nome=nome, data_nascimento=data_nascimento, email=email, senha=senha, perfil=perfil)

            if new_user:
                print('user cadastrado com sucesso!')
                return redirect(url_for("home"))
        except Exception as e:
            print(e)
            return redirect(url_for("login"))
    return render_template("cadastrar.html")

@app.route('/logistica/{var_clie}/{var_enco}',methods=['GET','POST'])
def logistica(var_clie,var_enco):
    for i in var_clie:
        print(i)
    movimen = get_movimentacao(id_cliente=var_clie,id_encomenda=var_enco)
    var_movi = movimen["movimentacao"]
    var_clien = movimen["cliente"]
    var_encom = movimen["encomenda"]
    return render_template("logistica.html",var_movi=var_movi,var_clien=var_clien,var_encom=var_encom)


@app.route('/post_movimentacao',methods=['GET','POST'])
def post_movimentacao():
    cep = request.form.get("form-cep")
    encomenda = request.form.get("form-encomenda")
    cliente = request.form.get("form-cliente")

    if not (cep and encomenda and cliente):
        print(f'error: valores invalidos')
        return redirect(url_for("get_logistica"))
    try:
        new_logistica = post_movimentacao(cep, encomenda, cliente)
        if new_logistica:
            print('logistica cadastrada com sucesso!')
            return redirect(url_for("get_logistica"))

    except Exception as e:
        print(e)
        return redirect(url_for("get_logistica"))

@app.route('/encomendas')
def get_encomendas():
    var_enco = get_encomenda()
    var_empre = get_empresas()
    var_cliente = get_cliente()
    return render_template("encomendas.html",var_enco=var_enco["encomendas"],var_empre=var_empre["empresas"],var_cliente=var_cliente["clientes"])

@app.route('/post_encomenda', methods=['POST'])
def cadastrar_encomenda():
    if request.method == 'POST':
        remetente = request.form.get("form-remetente")
        destinatario = request.form.get("form-destinatario")
        status = request.form.get("form-status")

        if not(remetente and destinatario and status):
            print(f'error: valores invalidos')
            return redirect(url_for("get_encomendas"))

        try:
            new_encom = post_encomenda(remetente, destinatario, status)

            if new_encom:
                print('encomenda cadastrada com sucesso!')
                return redirect(url_for("get_encomendas"))
        except Exception as e:
            print(e)
            return redirect(url_for("get_encomendas"))

    return render_template("encomendas.html")

@app.route('/pesquisar_encomenda', methods=['POST'])
def pesquisar_encomenda():
    if request.method == 'POST':
        termo = request.form.get("form-pesquisa")

        if not(termo):
            print(f'error: valores invalidos')
            return redirect(url_for("get_encomendas"))

        try:
            rastrea_enco = pesquisar_encomenda(termo)
            if rastrea_enco:
                print('encomenda encontrada com sucesso!')
                return redirect(url_for("get_encomendas"))
        except Exception as e:
            print(e)
            return redirect(url_for("get_encomendas"))
    return render_template("encomendas.html")

@app.route('/clientes')
def get_clientes():
    var_clientes = get_cliente()
    return render_template("clientes.html",var_clientes=var_clientes["clientes"])

@app.route('/cadastrar_cliente', methods=['POST'])
def post_cliente():
    if request.method == 'POST':
        nome = request.form.get("form-nome")
        cpf = request.form.get("form-cpf")
        telefone = request.form.get("form-telefone")
        cep = request.form.get("form-cep")

        if not(nome and cpf and telefone and cep):
            print(f'error: valores invalidos')
            return redirect(url_for("get_clientes"))
        try:
            new_cli = post_clientes(nome, cpf, telefone, cep)

            if new_cli:
                print('cliente cadastrado com sucesso!')
                return redirect(url_for("get_clientes"))

        except Exception as e:
            print(e)
            return redirect(url_for("get_clientes"))

    return render_template("clientes.html")

if __name__ == '__main__':
    app.run(debug=True, port=5004, host='0.0.0.0')


