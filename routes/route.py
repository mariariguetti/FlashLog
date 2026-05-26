import requests

url = "http://10.135.232.18:5006"


def logar_user(id):
    endereco = f"{url}/load_user"

    dados_user_1 = {
        "user_id":id
    }

    dados = requests.post(endereco, json=int(dados_user_1["user_id"]))
    print('geraldo',dados)
    return dados.json()


def post_usuario(nome, email, senha, data_nascimento, perfil):
    endereco = f"{url}/cadastrar_usuario"

    dados_user = {
        "nome": nome,
        "email": email,
        "senha": senha,
        "data_nascimento": data_nascimento,
        "perfil": perfil
    }
    print("user_",dados_user)

    dados = requests.post(endereco, json=dados_user)
    print('flamingo',dados)
    return dados.json()


def post_login(email, senha):
    endereco = f"{url}/logar_usuario"

    dados_usuario = {
        "email": email,
        "senha": senha
    }

    dados = requests.post(endereco, json=dados_usuario)
    print(dados)

    return dados.json()

def get_empresas():
    endereco = f"{url}/get_empresas"

    dados = requests.get(endereco)
    print('asd',dados)

    return dados.json()

def get_encomenda():
    endereco = f"{url}/get_encomenda"

    dados = requests.get(endereco)

    return dados.json()


def post_encomenda(remetente,destinatario,status_encomenda):
    endereco = f"{url}/post_encomenda"

    dados_encomenda = {
        "remetente": remetente,
        "destinatario": destinatario,
        "status_encomenda": status_encomenda
    }
    print('fla',dados_encomenda)
    dados = requests.post(endereco, json=dados_encomenda)
    print("mingo",dados)
    return dados.json()


def get_movimentacao(id_cliente, id_encomenda):
    endereco = f"{url}/get_movimentacao"

    dados_movimentacao = {
        "var_cliente": id_cliente,
        "var_encomenda": id_encomenda
    }

    print('flamingo',dados_movimentacao)
    dados = requests.post(endereco, json=dados_movimentacao)
    print('movi',dados)

    return dados.json()


def post_movimentacao(cep, encomenda_id, cliente_id):
    endereco = f"{url}/post_movimentacao"

    dados_movimentacao = {
        "cep": cep,
        "encomenda_id": encomenda_id,
        "cliente_id": cliente_id
    }

    dados = requests.post(endereco, json=dados_movimentacao)

    return dados.json()


def get_cliente():
    endereco = f"{url}/get_clientes"

    dados = requests.get(endereco)

    return dados.json()


def post_clientes(nome, cpf, telefone, cep):
    endereco = f"{url}/post_clientes"

    dados_clientes = {
        "nome": nome,
        "cpf": cpf,
        "telefone": telefone,
        "cep": cep
    }

    dados = requests.post(endereco, json=dados_clientes)

    return dados.json()


def pesquisar_encomenda(termo):
    endereco = f"{url}/pesquisar_encomenda"

    dados_pesquisa = {
        "termo": termo
    }

    dados = requests.post(endereco, json=dados_pesquisa)

    return dados.json()
