import requests

url = "http://10.135.232.36:5006"

def get_galpoes():
    url_ = f"{url}/get_galpoes"

    dados = requests.get(url_)

    return dados.json()

def get_empresas():
    url_ = f"{url}/get_empresas"

    dados = requests.get(url_)
    print('asd',dados)

    return dados.json()

def get_encomenda():
    url_ = f"{url}/get_encomenda"

    dados = requests.get(url_)

    return dados.json()

def get_movimentacao():
    url_ = f"{url}/get_movimentacao"

    dados = requests.get(url_)
    print('movi',dados)

    return dados.json()

def get_cliente():
    url_ = f"{url}/get_clientes"

    dados = requests.get(url_)
    print(dados)
    return dados.json()

def post_clientes(nome, cpf, telefone, endereco):
    url_ = f"{url}/post_cliente"

    dados_clientes = {
        "nome": nome,
        "cpf": cpf,
        "telefone": telefone,
        "endereco": endereco
    }

    dados = requests.post(url_, json=dados_clientes)

    return dados.json()

def post_encomenda(remetente,cliente_id):
    url_ = f"{url}/post_encomenda"

    dados_encomenda = {
        "remetente": remetente,
        "cliente_id": cliente_id,
    }

    dados = requests.post(url_, json=dados_encomenda)
    print(dados)

    return dados.json()

def post_galpao(cidade, estado):
    url_ = f"{url}/post_galpao"

    dados = {
        "cidade": cidade,
        "estado": estado,
    }

    dados = requests.post(url_, json=dados)

    return dados.json()

def post_usuario(nome, email, senha, data_nascimento, perfil):
    url_ = f"{url}/cadastrar_usuario"

    dados_user = {
        "nome": nome,
        "email": email,
        "senha": senha,
        "data_nascimento": data_nascimento,
        "perfil": perfil
    }
    print("user_",dados_user)

    dados = requests.post(url_, json=dados_user)
    print('flamingo',dados)
    return dados.json()

def post_login(email, senha):
    url_ = f"{url}/logar_usuario"

    dados_usuario = {
        "email": email,
        "senha": senha
    }

    dados = requests.post(url_, json=dados_usuario)
    print(dados)

    return dados.json()

def post_movimentacao(galpao_id, encomenda_id):
    url_ = f"{url}/post_movimentacao"

    dados_movimentacao = {
        "galpao_id": galpao_id,
        "encomenda_id": encomenda_id,
    }

    dados = requests.post(url_, json=dados_movimentacao)

    return dados.json()

def pesquisar_encomenda(termo):
    url_ = f"{url}/pesquisar_encomenda"

    dados_pesquisa = {
        "termo": termo
    }

    dados = requests.post(url_, json=dados_pesquisa)

    return dados.json()

def logar_user(id):
    print(id)
    pass

def put_cliente(nome,cpf,telefone,endereco,var_id):
    url_ = f"{url}/put_cliente/{var_id}"

    dados_clientes = {
        "nome": nome,
        "cpf": cpf,
        "telefone": telefone,
        "endereco": endereco
    }

    dados = requests.put(url_, json=dados_clientes)
    return dados.json()

def put_encomenda(remetente,var_id):
    url_ = f"{url}/put_encomenda/{var_id}"

    dados_encomenda = {
        "remetente": remetente
    }

    dados = requests.put(url_, json=dados_encomenda)
    return dados.json()

def put_galpao(cidade,estado,var_id):
    url_ = f"{url}/put_galpao/{var_id}"

    dados_galpao = {
        "cidade": cidade,
        "estado": estado,
    }

    dados = requests.put(url_, json=dados_galpao)
    return dados.json()

