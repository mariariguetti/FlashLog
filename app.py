from xml.dom.pulldom import END_ELEMENT

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user, UserMixin

from routes.rota_banco import *
from routes.rota_endereco import get_endereco

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
    encomendas = get_encomenda()
    clientes = get_cliente()
    print('enco',encomendas["encomendas"])
    print('clie',clientes["clientes"])
    return render_template("base.html",var_e=encomendas["encomendas"],var_c=clientes["clientes"])

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

@app.route('/logistica',methods=['GET','POST'])
def logistica():
    var_clien = get_cliente()
    var_encom = get_encomenda()
    movimen = get_movimentacao()
    movi_1 = movimen["movimentacao"]
    for i in movi_1:
        endereco = i["movimentacao"]["cep"]
        ende_ = get_endereco(endereco)
        endereco_ = f"{ende_['localidade']}/{ende_['uf']}"
        i["movimentacao"]["cep"] = endereco_
    return render_template("logistica.html",var_movi=movimen["movimentacao"], var_clien=var_clien["clientes"],var_encom=var_encom["encomendas"],var_ender=movimen)


@app.route('/post_movimentacao',methods=['GET','POST'])
def post_movimentacao():
    cep = request.form.get("form-cep")
    encomenda = request.form.get("form-encomenda")

    if not (cep and encomenda):
        print(f'error: valores invalidos')
        return redirect(url_for("logistica"))
    try:
        new_logistica = cadastrar_movimentacao(cep, encomenda)
        if new_logistica:
            print('logistica cadastrada com sucesso!')
            return redirect(url_for("logistica"))

    except Exception as e:
        print(e)
        return redirect(url_for("logistica"))

@app.route('/edit_movimentacao',methods=['GET','POST'])
def edit_movimentacao():
    pass

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

        if not(remetente and destinatario):
            print(f'error: valores invalidos')
            return redirect(url_for("get_encomendas"))
        elif not status:
            status = "POSTADO"
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
    clien_ = var_clientes["clientes"]
    for i in clien_:
        endereco = i["cep"]
        ende_ = get_endereco(endereco)
        endereco_ = f"{ende_['localidade']}/{ende_['uf']}"
        i["cep"] = endereco_
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

@app.route('/galpoes')
def ver_galpoes():
    var_galpoes = get_galpoes()
    return render_template("galpoes.html",var_galpoes=var_galpoes["galpoes"])

@app.route('/postar_galpao', methods=['POST'])
def postar_galpao():
    if request.method == 'POST':
        cep = request.form.get("form-cep")

        if not(cep):
            print(f'error: valores invalidos')
            return redirect(url_for("ver_galpoes"))
        try:
            endereco_galpao = get_endereco(cep=cep)
            print(endereco_galpao)
            new_ende = post_galpao(cidade=endereco_galpao["logradouro"],estado=endereco_galpao["estado"])
            if new_ende:
                print('galpão cadastrado com sucesso!')
                return redirect(url_for("ver_galpoes"))

        except Exception as e:
            print(e)
            return redirect(url_for("ver_galpoes"))

    return redirect(url_for("ver_galpoes"))




if __name__ == '__main__':
    app.run(debug=True, port=5004, host='0.0.0.0')


