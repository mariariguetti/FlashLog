import requests

url = "https://viacep.com.br/ws/"

def get_endereco(cep):
    endereco = f"{url}/{cep}/json"

    dados = requests.get(endereco)

    return dados.json()