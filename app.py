from datetime import datetime
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
    def __init__(self, id, nome, data_nascimento, email, perfil):
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
def index():
    return redirect(url_for('logistica'))

@app.route('/home')
def home():
    return render_template("base.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("form-email")
        senha = request.form.get("form-senha")

        if not (email and senha):
            print(f'error: valores invalidos')
            return render_template("login.html")
        else:
            try:
                user = post_login(email, senha)
                return render_template('login.html',status_login=user['status'])
            except Exception as e:
                print(e)
                return redirect(url_for('login'))
    return render_template("login.html")

@app.route('/logout')
def logout():
    logout_user()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('home'))

@app.route('/cadastrar_user', methods=['POST'])
def cadastrar_user():
    if request.method == 'POST':
        nome = request.form.get("form-nome")
        data_nascimento = request.form.get("form-nascimento")
        email = request.form.get("form-email")
        senha = request.form.get("form-senha")
        perfil = request.form.get("form-perfil")
        if not (nome and data_nascimento and email and senha and perfil):
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
    return render_template("login.html")

@app.route('/logistica')
def logistica():
    var_galpo = get_galpoes()
    var_encom = get_encomenda()
    movimen = get_movimentacao()
    for i in movimen:
        data_atual = i['movimentacao']['data_atual']

        date_ = datetime.strptime(data_atual, '%a, %d %b %Y %H:%M:%S GMT')

        result_data = date_.strftime('%d/%m/%Y - %H:%M')

        i['movimentacao']['data_atual'] = result_data

    return render_template("logistica.html", var_movi=movimen, var_galpo=var_galpo,
                           var_encom=var_encom)

@app.route('/cadastrar_movimentacao', methods=['GET', 'POST'])
def cadastrar_movimentacao():
    galpao = request.form.get("form-galpao")
    encomenda = request.form.get("form-encomenda")

    if not galpao or not encomenda:
        print(f'error: valores invalidos')
        flash("Digite em todos os campos para Cadastrar a Movimentacao", "danger")
        return redirect(url_for("logistica"))
    try:
        psm1 = post_movimentacao(galpao_id=galpao, encomenda_id=encomenda)
        flash(psm1['msg'], psm1['status'])
        print('logistica cadastrada com sucesso!')
        return redirect(url_for("logistica"))
    except Exception as e:
        print(e)
        flash(f'Falha interna no sistema (Erro: {e}). Tente novamente mais tarde.', 'warning')
        return redirect(url_for("logistica"))

@app.route('/encomendas')
def encomendas():
    var_enco = get_encomenda()
    var_cliente = get_cliente()
    market_place = ["Mercado Livre",'Amazon','Shopee','Magazine Luiza','AliExpress','Shein','Americanas','Casas Bahia',"OLX"]
    return render_template("encomendas.html", var_enco=var_enco,var_cliente=var_cliente,market_place=market_place)

@app.route('/cadastrar_encomenda', methods=['POST'])
def cadastrar_encomenda():
    if request.method == 'POST':
        remetente = request.form.get("form-remetente")
        cliente_id = request.form.get("form-cliente_id")
        if not remetente or not cliente_id:
            print(f'error: valores invalidos')
            flash("Digite em todos os campos para Cadastrar o Encomenda", "danger")
            return redirect(url_for("encomendas"))
        try:
            pse1 = post_encomenda(remetente=remetente, cliente_id=cliente_id)
            flash(pse1['msg'], pse1['status'])
            print('encomenda cadastrada com sucesso!')
            return redirect(url_for("encomendas"))
        except Exception as e:
            print(e)
            flash(f'Falha interna no sistema (Erro: {e}). Tente novamente mais tarde.', 'warning')
            return redirect(url_for("encomendas"))

@app.route('/pesquisar_encomenda', methods=['POST'])
def pesquisar_encomenda():
    if request.method == 'POST':
        termo = request.form.get("form-pesquisa")
        if not termo:
            print(f'error: valores invalidos')
            return redirect(url_for("encomendas"))
        try:
            rastrea_enco = pesquisar_encomenda(termo)
            if rastrea_enco:
                print('encomenda encontrada com sucesso!')
                return redirect(url_for("encomendas"))
        except Exception as e:
            print(e)
            return redirect(url_for("encomendas"))

@app.route('/edit_encomenda/<var_id>', methods=['POST'])
def edit_encomenda(var_id):
    if request.method == 'POST':
        remetente = request.form.get("form-remetente")
        cliente_id = request.form.get("form-cliente_id")
        print(remetente,cliente_id)
        if not remetente or not cliente_id:
            flash("Digite em todos os campos para Editar a Encomenda", "danger")
            return redirect(url_for("encomendas"))
        try:
            pue1 = put_encomenda(remetente,cliente_id,var_id)
            flash(pue1['msg'], pue1["status"])
            return redirect(url_for("encomendas"))
        except Exception as e:
            print(e)
            flash(f"Falha interna no sistema (Erro: {e}). Tente novamente mais tarde.", "warning")
            return redirect(url_for("encomendas"))


@app.route('/clientes')
def clientes():
    var_clientes = get_cliente()
    return render_template("clientes.html", var_clientes=var_clientes)

@app.route('/cadastrar_cliente', methods=['POST'])
@app.route('/cadastrar_cliente/<var_id>', methods=['POST'])
def cadastrar_cliente(var_id=None):
    if request.method == 'POST':
        print("ID",var_id)
        if var_id != None:
            nome = request.form.get("form-nome")
            cpf = request.form.get("form-cpf")
            telefone = request.form.get("form-telefone")
            endereco = request.form.get("form-endereco")
            rua = request.form.get("form-rua")
            numero_casa = request.form.get("form-numero_casa")
            if not nome or not cpf or not telefone or not endereco or not rua or not numero_casa:
                print(f'error: valores invalidos')
                flash("Digite em todos os campos para Editar o Cliete", "danger")
                return redirect(url_for("clientes"))
            try:
                puc1 = put_cliente(nome=nome, cpf=cpf, telefone=telefone, endereco=endereco, rua=rua, numero_casa=numero_casa,
                            var_id=var_id)
                flash(puc1['msg'], puc1["status"])
                return redirect(url_for("clientes"))
            except Exception as e:
                print(e)
                flash(f"Falha interna no sistema (Erro: {e}). Tente novamente mais tarde.", "warning")
                return redirect(url_for("clientes"))

        nome = request.form.get("form-nome")
        cpf = request.form.get("form-cpf")
        telefone = request.form.get("form-telefone")
        cidade = request.form.get("form-cidade")
        estado = request.form.get("form-uf")
        rua = request.form.get("form-rua")
        numero_casa = request.form.get("form-numero_casa")
        if not nome or not cpf or not telefone or not cidade or not estado or not rua or not numero_casa:
            print(f'error: valores invalidos')
            flash("Digite em todos os campos para Cadastrar o Cliente", "danger")
            return redirect(url_for("clientes"))

        local = f"{cidade}/{estado}"
        print(local)
        try:
            ptc1 = post_clientes(nome=nome, cpf=cpf, telefone=telefone, endereco=local,rua=rua,numero_casa=numero_casa)

            flash(ptc1['msg'], ptc1['status'])
            print('cliente cadastrado com sucesso!')
            return redirect(url_for("clientes"))
        except Exception as e:
            print(e)
            flash(f"Falha interna no sistema (Erro: {e}). Tente novamente mais tarde.", "warning")
            return redirect(url_for("clientes"))


@app.route('/galpoes')
def galpoes():
    var_galpoes = get_galpoes()
    return render_template("galpoes.html", var_galpoes=var_galpoes)

@app.route('/cadastrar_galpao', methods=['POST'])
@app.route('/cadastrar_galpao/<int:var_id>', methods=['POST'])
def cadastrar_galpao(var_id=None):
    if request.method == 'POST':
        print('ID',var_id)
        if var_id != None:
            cidade = request.form.get("form-cidade")
            estado = request.form.get("form-estado")
            if not cidade or not estado:
                print(f'error: valores invalidos')
                flash("Digite em todos os campos para Editar o Galpão", "danger")
                return redirect(url_for("galpoes"))
            try:
                pug1 = put_galpao(cidade, estado, var_id)

                flash(pug1['msg'], pug1["status"])
                return redirect(url_for("galpoes"))
            except Exception as e:
                print(e)
                flash(f"Falha interna no sistema (Erro: {e}). Tente novamente mais tarde.", "warning")
                return redirect(url_for("galpoes"))

        cep = request.form.get("form-cep")
        if not cep:
            print(f'error: valores invalidos')
            flash("Digite em todos os campos para Cadastrar o Galpão", "danger")
            return redirect(url_for("galpoes"))
        try:
            endereco_galpao = get_endereco(cep=cep)
            ptg1 = post_galpao(cidade=endereco_galpao["localidade"], estado=endereco_galpao["uf"])

            flash(ptg1['msg'], ptg1['status'])
            print('galpão cadastrado com sucesso!')
            return redirect(url_for("galpoes"))

        except Exception as e:
            print(e)
            flash(f'Falha interna no sistema (Erro: {e}). Tente novamente mais tarde.', 'warning')
            return redirect(url_for("galpoes"))



if __name__ == '__main__':
    app.run(debug=True, port=5002, host='0.0.0.0')