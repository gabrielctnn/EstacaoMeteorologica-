async function puxarDados(){
    let buscaDados = await fetch("http://127.0.0.1:8000/sensors") // vai nesse endereço do servidor e pega os dados na API
    let dados = await buscaDados.json() //pega os dados e guarda em json
    let lista = dados["Dados enviados com sucesso:"]
    let leitura = lista[lista.length - 1 ] // pega o ultimo envio de dados

    document.getElementById("textLuminosidade").innerText = validarDadoNulo(leitura.luminosidade)
    document.getElementById("textTemperatura").innerText = validarDadoNulo(leitura.temperatura)
    document.getElementById("textUmidade").innerText = validarDadoNulo(leitura.umidade)
    document.getElementById("textPressao").innerText = validarDadoNulo(leitura.pressao)
    document.getElementById("textValorAr").innerText = validarDadoNulo(leitura.valorAr)
    document.getElementById("textQualidadeArStatus").innerText = validarDadoNulo(leitura.qualidadeArStatus)
    document.getElementById("textPrecipitacao").innerText = validarDadoNulo(leitura.precipitacao)

    document.getElementById("textLuminosidade-Detalhes").innerText = validarDadoNulo(leitura.luminosidade," ADC")
    document.getElementById("textTemperatura-Detalhes").innerText = validarDadoNulo(leitura.temperatura," °C")
    document.getElementById("textUmidade-Detalhes").innerText = validarDadoNulo(leitura.umidade," %")
    document.getElementById("textPressao-Detalhes").innerText = validarDadoNulo(leitura.pressao, "hPa")
    document.getElementById("textValorAr-Detalhes").innerText = validarDadoNulo(leitura.valorAr," indice")
    document.getElementById("textPrecipitacao-Detalhes").innerText = validarDadoNulo(leitura.precipitacao," mm")

    statusSensores("status-temperatura", leitura.temperatura)
    statusSensores("status-pressao", leitura.pressao)
    statusSensores("status-umidade", leitura.umidade)
    statusSensores("status-luminosidade", leitura.luminosidade)
    statusSensores("status-ar", leitura.valorAr)
    statusSensores("status-chuva", leitura.precipitacao)

    statusSensoresDosDetalhes("situacao-temperatura", leitura.temperatura, FAIXAS.temperatura)
    statusSensoresDosDetalhes("situacao-pressao", leitura.pressao, FAIXAS.pressao)
    statusSensoresDosDetalhes("situacao-umidade", leitura.umidade, FAIXAS.umidade)
    statusSensoresDosDetalhes("situacao-luminosidade", leitura.luminosidade, FAIXAS.luminosidade)
    statusSensoresDosDetalhes("situacao-ar", leitura.valorAr, FAIXAS.ar)
    statusSensoresDosDetalhes("situacao-chuva", leitura.precipitacao, FAIXAS.chuva)

    console.log(leitura)
}

window.onload = function() {
  puxarDados(); // puxa os dados quando a pagina carrega primeira vez
};


setInterval(() => {
  puxarDados()
}, 150000); 


function validarDadoNulo(valor, unidade = "") {
    if (valor === null || valor === undefined) return "—"
    return unidade ? valor + " " + unidade : valor
}

function validarUmidade(umidade){
  if (umidade<= 30){
    let textoStatusUmidade = "TempoSeco"
    let corStatus = corzinhavermelha
  } else if (umidade > 30 && umidade <= 60){
    let textoStatusUmidade = "TempoConfortável"
    let corStatus= verde
  } else {
    let textoStatusUmidade = "TempoUmido"
    let corStatus= ciano
  }
  return {textoStatusUmidade, corStatus}
}

function statusSensores (id, valor){
  const identidade = document.getElementById(id)
  const semDado = valor === null || valor === undefined
  identidade.className = "bolinha-status " + (semDado ? "off" : "ligado")
  identidade.innerHTML = "<i></i>" + (semDado ? "Sem dado" : "Ligado")
}


function statusSensoresDosDetalhes(id, valor, faixas) {
    const identidade = document.getElementById(id)
    const semDado = valor === null || valor === undefined

    if (semDado) {
        identidade.className = "detalhes-situacao off"
        identidade.innerHTML = "<i></i>Sem dado"
        return
    }

    const faixa = classificar(valor, faixas)
    identidade.className = "detalhes-situacao " + faixa.nivel
    identidade.innerHTML = "<i></i>" + faixa.texto
}

const FAIXAS = {
    temperatura: [
        { ate: 15, texto: "Frio", nivel: "atencao" },
        { ate: 28, texto: "Agradável", nivel: "ok" },
        { ate: 35, texto: "Quente", nivel: "atencao" },
        { ate: Infinity, texto: "Calor extremo", nivel: "alerta" }
    ],
    umidade: [
        { ate: 30, texto: "Ar seco", nivel: "atencao" },
        { ate: 60, texto: "Confortável", nivel: "ok" },
        { ate: 80, texto: "Úmido", nivel: "atencao" },
        { ate: Infinity, texto: "Muito úmido", nivel: "alerta" }
    ],
    luminosidade: [
    { ate: 400, texto: "Escuro", nivel: "ok" },
    { ate: 3000, texto: "Claro", nivel: "ok" },
    { ate: Infinity, texto: "Muito claro", nivel: "ok" }
    ],
    ar: [
        { ate: 600, texto: "Boa", nivel: "ok" },
        { ate: 1000, texto: "Moderada", nivel: "atencao" },
        { ate: Infinity, texto: "Ruim", nivel: "alerta" }
    ],
    pressao: [
        { ate: 1000, texto: "Baixa", nivel: "atencao" },
        { ate: 1025, texto: "Normal", nivel: "ok" },
        { ate: Infinity, texto: "Alta", nivel: "atencao" }
    ],
    chuva: [
        { ate: 0, texto: "Sem chuva agora", nivel: "ok" },
        { ate: 2.5, texto: "Chuva fraca", nivel: "atencao" },
        { ate: 7.5, texto: "Chuva moderada", nivel: "atencao" },
        { ate: Infinity, texto: "Chuva forte", nivel: "alerta" }
    ]
}

function classificar(valor, faixas) {
    for (const faixa of faixas) {
        if (valor <= faixa.ate) return faixa
    }
}