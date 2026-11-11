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
    document.getElementById("textQualidadeArStatus").innerText = leitura.qualidadeArStatus
    document.getElementById("textPrecipitacao").innerText = leitura.precipitacao

    document.getElementById("textLuminosidade-Detalhes").innerText = leitura.luminosidade + " lx"
    document.getElementById("textTemperatura-Detalhes").innerText = leitura.temperatura + " °C"
    document.getElementById("textUmidade-Detalhes").innerText = leitura.umidade + " %"
    document.getElementById("textPressao-Detalhes").innerText = leitura.pressao + " hPa"
    document.getElementById("textValorAr-Detalhes").innerText = leitura.valorAr + " ppm"
    document.getElementById("textPrecipitacao-Detalhes").innerText = leitura.precipitacao + " mm"

    console.log(leitura)
}

window.onload = function() {
  puxarDados(); // puxa os dados quando a pagina carrega primeira vez
};


setInterval(() => {
  puxarDados()
}, 150000); 