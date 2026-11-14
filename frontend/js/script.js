async function puxarDados(){
    try {
        let buscaDados = await fetch("http://127.0.0.1:8000/sensors") // vai nesse endereço do servidor e pega os dados na API
        let dados = await buscaDados.json() //pega os dados e guarda em json
        let lista = dados["Dados enviados com sucesso:"]
        if (!buscaDados.ok || !lista || lista.length === 0){
           throw new Error("Offline")
        }
        let leitura = lista[lista.length - 1 ] // pega o ultimo envio de dados
        atualizarLeitura(leitura)
        ultimaCriadoEm = leitura.criado_em
        const online = atualizarEstacao(leitura.criado_em)
        if (!online) {
            document.getElementById("resumoAmbiente").className = "painelDetalhes-resultado off"
            document.getElementById("resumoTitulo").innerText = "Estação offline"
            document.getElementById("resumoTexto").innerText = "Sem previsão do ambiente."

            ["temperatura","pressao","umidade","luminosidade","ar","chuva"].forEach(s => {
            const el = document.getElementById("status-" + s)
            el.className = "bolinha-status off"
            el.innerHTML = "<i></i>Sem sinal"
        })
        }
        console.log(leitura)
    } catch(erro){
      atualizarLeitura({})
      atualizarEstacao(null)
      ultimaCriadoEm = null
    }

}

window.onload = function() {
  puxarDados(); // puxa os dados quando a pagina carrega primeira vez
};

let ultimaCriadoEm = null
setInterval(() => {
  atualizarEstacao(ultimaCriadoEm)
}, 1000)

setInterval(() => {
  puxarDados()
}, 15000);


function validarDadoNulo(valor, unidade = "") {
    if (valor === null || valor === undefined) return "—"
    return unidade ? valor + " " + unidade : valor
}

function statusSensores (id, valor){
  const identidade = document.getElementById(id)
  const semDado = valor === null || valor === undefined
  identidade.className = "bolinha-status " + (semDado ? "off" : "ligado")
  identidade.innerHTML = "<i></i>" + (semDado ? "Sem dado" : "Ligado")
}

function atualizarEstacao(criadoEm) {
    const bolinha = document.getElementById("statusEstacaoBolinha")
    const texto = document.getElementById("statusEstacaoTexto")

    if (!criadoEm) {
        bolinha.className = "status-bolinha off"
        texto.innerText = "Offline · sem leitura"
        return false
    }

    let iso = String(criadoEm).replace(" ", "T")
    if (!/(Z|[+-]\d\d:?\d\d)$/i.test(iso)) iso += "Z"

    const segundos = (Date.now() - new Date(iso).getTime()) / 1000

    if (segundos > 30) {
        bolinha.className = "status-bolinha off"
        texto.innerText = "Offline · última leitura há " + Math.round(segundos / 60) + " min"
        return false
    } else {
        bolinha.className = "status-bolinha"
        texto.innerText = "Online · última leitura há " + Math.round(segundos) + " s"
        return true
    }
}


function statusSensoresDosDetalhes(id, valor, faixas) {
    const identidade = document.getElementById(id)
    const semDado = valor === null || valor === undefined

    if (semDado) {
        identidade.className = "detalhes-situacao off"
        identidade.innerHTML = "<i></i>Sem dado"
        return null
    }

    const faixa = classificar(valor, faixas)
    identidade.className = "detalhes-situacao " + faixa.nivel
    identidade.innerHTML = "<i></i>" + faixa.texto
    return faixa.nivel
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

function atualizarLeitura(leitura){
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
      const niveis = [
        statusSensoresDosDetalhes("situacao-temperatura", leitura.temperatura, FAIXAS.temperatura),
        statusSensoresDosDetalhes("situacao-pressao", leitura.pressao, FAIXAS.pressao),
        statusSensoresDosDetalhes("situacao-umidade", leitura.umidade, FAIXAS.umidade),
        statusSensoresDosDetalhes("situacao-luminosidade", leitura.luminosidade, FAIXAS.luminosidade),
        statusSensoresDosDetalhes("situacao-ar", leitura.valorAr, FAIXAS.ar),
        statusSensoresDosDetalhes("situacao-chuva", leitura.precipitacao, FAIXAS.chuva)
      ]

      const resumo = resumirAmbiente(niveis)
      document.getElementById("resumoAmbiente").className = "painelDetalhes-resultado " + resumo.classe
      document.getElementById("resumoTitulo").innerText = resumo.titulo
      document.getElementById("resumoTexto").innerText = resumo.texto
}

function resumirAmbiente(niveis) {
    const medidos = niveis.filter(n => n !== null)
    if (medidos.length === 0) {
        return { classe: "off", titulo: "Offline", texto: "Aguardando leitura" }
    }

    const alertas = medidos.filter(n => n === "alerta").length
    const atencoes = medidos.filter(n => n === "atencao").length

    if (alertas >= 3) {
        return { classe: "perigoso", titulo: "Perigoso", texto: "Vários aspectos do ambiente estão em nível perigoso." }
    }
    if (alertas === 2 || atencoes >= 2) {
        return { classe: "alerta", titulo: "Alerta", texto: "Alguns aspectos exigem atenção." }
    }
    return { classe: "ok", titulo: "Ok", texto: "O ambiente está bom." }
}

