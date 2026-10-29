async function puxarDados(){
    let buscaDados = await fetch("http://127.0.0.1:8000/sensors") // vai nesse endereço do servidor e pega os dados na API
    let dados = await buscaDados.json() //pega os dados e guarda em json
    let lista = dados["Dados enviados com sucesso:"]
    let leitura = lista[lista.length - 1 ] // pega o ultimo envio de dados

    document.getElementById("textLuminosidade").innerText = leitura.luminosidade
    document.getElementById("textTemperatura").innerText = leitura.temperatura
    document.getElementById("textUmidade").innerText = leitura.umidade
    document.getElementById("textPressao").innerText = leitura.pressao
    document.getElementById("textValorAr").innerText = leitura.valorAr

    console.log(leitura)
}

   

