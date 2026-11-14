# 🌤️ Estação Meteorológica Inteligente com ESP32

[![MicroPython](https://img.shields.io/badge/MicroPython-1.20+-blue.svg)]()
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-%23009688.svg)]()
[![Hardware](https://img.shields.io/badge/HARDWARE-ESP32-orange.svg)]()

Projeto acadêmico de monitoramento ambiental de ponta a ponta construído com **ESP32** e **MicroPython**. Desenvolvido como parte das atividades práticas do curso de Ciência da Computação (UNIP), esta estação realiza a coleta contínua de dados ambientais em tempo real, validando-os através de um backend robusto, persistindo as informações em banco de dados e disponibilizando-as em um dashboard web interativo.

---

## 🔄 Fluxo de Funcionamento

O sistema opera de forma integrada através das seguintes etapas:

1. **Coleta no Firmware:** O **ESP32** executa scripts em **MicroPython** capturando os dados brutos de todos os sensores conectados:
   - **DHT22:** Realiza a leitura de temperatura e umidade relativa do ar.
   - **MQ135:** Captura a medição analógica da concentração de gases e poluição no ar.
   - **LDR:** Identifica o nível de luminosidade para classificar o ambiente entre claro ou escuro.
   - **HC-SR04:** Executa a medição do nível de água via ultrassom para a estimativa de volume de chuva (pluviometria).
   - **BMP280:** Realiza a leitura barométrica da pressão atmosférica (em hPa) via barramento I2C.
2. **Validação e Processamento (Backend):** Os dados coletados pelo firmware são transmitidos via rede para a API em **FastAPI**, que recebe o payload, executa as validações de integridade e regra de negócio.
3. **Persistência:** O backend processa as informações e utiliza o **SQLAlchemy ORM** para salvar o histórico completo das métricas coletadas no banco de dados relacional.
4. **Visualização (Frontend):** Os dados persistidos são consumidos e exibidos em tempo real no dashboard web, permitindo o acompanhamento gráfico e visual do monitoramento ambiental.

---

## 🛠️ Hardware Utilizado

A prototipagem física e simulada (via Wokwi) utiliza os seguintes componentes principais:

| Componente | Função | Pino/Interface |
| :--- | :--- | :--- |
| **ESP32** | Microcontrolador central com Wi-Fi/BLE | Core do Sistema |
| **DHT22** | Temperatura e Umidade do Ar | Digital / GPIO |
| **MQ135** | Qualidade do Ar (Gases) | Entrada Analógica (ADC) |
| **LDR** | Luminosidade | Entrada Analógica (ADC) |
| **HC-SR04** | Ultrassônico para Pluviometria | Trigger / Echo (GPIO) |
| **BMP280** | Pressão Atmosférica | I2C (SDA/SCL - GPIO 21/22) |

---

## 📁 Arquitetura do Repositório

O projeto adota uma estrutura **monorepo** organizada para desacoplar as camadas de hardware, lógica de servidores, interface do usuário e documentação:

```text
estacao-meteorologica/
├── firmware/       # Códigos em MicroPython para o ESP32 (main.py) e simulação (diagram.json)
├── backend/        # API desenvolvida em FastAPI, rotas, modelos e integração via SQLAlchemy
├── frontend/       # Dashboard web para visualização em tempo real das métricas ambientais
├── docs/           # Documentação técnica, diagramas e relatórios do projeto acadêmico
└── README.md       # Documentação central e guia do repositório
```
