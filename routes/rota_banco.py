import requests

url = "http://10.135.232.19:5006"

def get_galpoes():
    endereco = f"{url}/get_galpoes"

    dados = requests.get(endereco)

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

def get_movimentacao():
    endereco = f"{url}/get_movimentacao"

    dados = requests.get(endereco)
    print('movi',dados)

    return dados.json()

def get_cliente():
    endereco = f"{url}/get_clientes"

    dados = requests.get(endereco)
    print(dados)
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

def post_encomenda(remetente,cliente_id):
    endereco = f"{url}/post_encomenda"

    dados_encomenda = {
        "remetente": remetente,
        "cliente_id": cliente_id,
    }

    dados = requests.post(endereco, json=dados_encomenda)
    print(dados)

    return dados.json()

def post_galpao(cidade, estado):
    endereco = f"{url}/post_galpao"

    dados = {
        "cidade": cidade,
        "estado": estado,
    }

    dados = requests.post(endereco, json=dados)

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

def post_movimentacao(galpao_id, encomenda_id,status_movi):
    endereco = f"{url}/post_movimentacao"

    dados_movimentacao = {
        "galpao_id": galpao_id,
        "encomenda_id": encomenda_id,
        "status_movimentacao": status_movi
    }

    dados = requests.post(endereco, json=dados_movimentacao)

    return dados.json()

def pesquisar_encomenda(termo):
    endereco = f"{url}/pesquisar_encomenda"

    dados_pesquisa = {
        "termo": termo
    }

    dados = requests.post(endereco, json=dados_pesquisa)

    return dados.json()

def logar_user(id):
    print(id)
    pass

def put_cliente(nome,cpf,telefone,cep,var_id):
    endereco = f"{url}/put_cliente/{var_id}"

    dados_clientes = {
        "nome": nome,
        "cpf": cpf,
        "telefone": telefone,
        "cep": cep
    }

    dados = requests.put(endereco, json=dados_clientes)
    return dados.json()

def put_encomenda(remetente,var_id):
    endereco = f"{url}/put_encomenda/{var_id}"

    dados_encomenda = {
        "remetente": remetente
    }

    dados = requests.put(endereco, json=dados_encomenda)
    return dados.json()

def put_galpao(cidade,estado,var_id):
    endereco = f"{url}/put_galpao/{var_id}"

    dados_galpao = {
        "cidade": cidade,
        "estado": estado,
    }

    dados = requests.put(endereco, json=dados_galpao)
    return dados.json()

