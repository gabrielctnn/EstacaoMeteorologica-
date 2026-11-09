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

   


/* ==================================
   MAPA INTERATIVO - ECOMAPA
   ================================== */

// Cria o mapa, inicialmente mostrando o Brasil
const mapa = L.map("mapa").setView(
    [-14.2350, -51.9253],
    4
);

// Adiciona o mapa do OpenStreetMap
L.tileLayer(
    "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
        attribution: '&copy; OpenStreetMap',
        maxZoom: 19
    }
).addTo(mapa);

// Elementos que mostram a localização
const textoLocalizacao =
    document.getElementById("texto-localizacao");

const coordenadasLocalizacao =
    document.getElementById("coordenadas-localizacao");

// Verifica se o navegador suporta localização
if (navigator.geolocation) {

    navigator.geolocation.getCurrentPosition(

        // Caso o usuário permita a localização
        function(posicao) {

            const latitude = posicao.coords.latitude;
            const longitude = posicao.coords.longitude;
            const precisao = posicao.coords.accuracy;

            // Centraliza o mapa no usuário
            mapa.setView(
                [latitude, longitude],
                15
            );

            // Adiciona o marcador
            L.marker([latitude, longitude])
                .addTo(mapa)
                .bindPopup("Você está aqui (aproximadamente)")
                .openPopup();

            // Atualiza os textos
            textoLocalizacao.textContent =
                "Sua localização aproximada";

            coordenadasLocalizacao.textContent =
                "Precisão estimada: " +
                Math.round(precisao) + " metros";

            // Atualiza o cabeçalho
            document.querySelector(".local-header")
                .textContent = "📍 Localização atual";
        },

        // Caso a localização falhe
        function(erro) {

            textoLocalizacao.textContent =
                "Localização indisponível";

            if (erro.code === 1) {
                coordenadasLocalizacao.textContent =
                    "Permissão de localização negada";
            } else {
                coordenadasLocalizacao.textContent =
                    "Não foi possível encontrar sua localização";
            }
        },

        {
            enableHighAccuracy: true,
            timeout: 15000,
            maximumAge: 60000
        }
    );

} else {

    textoLocalizacao.textContent =
        "Localização não suportada pelo navegador";
}
