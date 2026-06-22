async function get_cep() {
    const input_cep = document.getElementById('form-cep')

    let url = "https://viacep.com.br/ws/" + input_cep.value + "/json/"
    let resultado = await fetch(url)

    if (resultado.ok) {
        let dados = await resultado.json()
        const input_cidade = document.getElementById('form-cidade')
        const input_uf = document.getElementById('form-uf')
        const input_rua = document.getElementById('form-rua')

        input_cidade.value = dados.localidade
        input_uf.value = dados.uf
        input_rua.value = dados.logradouro
    }
}

async function get_cep1(id) {
    const input_cep = document.getElementById('form-cepe'+id)

    console.log(input_cep.value)

    let url = "https://viacep.com.br/ws/" + input_cep.value + "/json/"
    let resultado = await fetch(url)

    if (resultado.ok) {
        let dados = await resultado.json()
        const input_cidade = document.getElementById('form-cidadee'+id)
        const input_uf = document.getElementById('form-ufe'+id)

        input_cidade.value = dados.localidade
        input_uf.value = dados.uf
    }
}

async function get_cep2(id) {
    const input_cep = document.getElementById('form-cepe'+id)

    console.log(input_cep.value)

    let url = "https://viacep.com.br/ws/" + input_cep.value + "/json/"
    let resultado = await fetch(url)

    if (resultado.ok) {
        let dados = await resultado.json()
        const input_endereco = document.getElementById('form-endereco'+id)
        const input_rua = document.getElementById('form-ruae'+id)

        input_endereco.value = dados.localidade + '/' + dados.uf
        console.log(input_endereco.value)
        input_rua.value = dados.logradouro
    }
}