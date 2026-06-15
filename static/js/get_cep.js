async function get_cep() {
    const input_cep = document.getElementById('form-cep')

    let url = "https://viacep.com.br/ws/" + input_cep.value + "/json/"
    let resultado = await fetch(url)

    if (resultado.ok) {
        let dados = await resultado.json()
        const input_cidade = document.getElementById('form-cidade')
        const input_uf = document.getElementById('form-uf')

        input_cidade.value = dados.localidade
        input_uf.value = dados.uf
    }
}