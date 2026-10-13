# 🌤️ Estação Meteorológica Inteligente com ESP32

![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow?style=for-the-badge)
![MicroPython](https://img.shields.io/badge/MicroPython-1.20+-blue?style=for-the-badge&logo=python)
![ESP32](https://img.shields.io/badge/Hardware-ESP32-black?style=for-the-badge&logo=espressif)

Um projeto acadêmico de monitoramento ambiental construído com **ESP32** e **MicroPython**. Desenvolvido como parte das atividades práticas do 2º semestre do curso de Ciência da Computação (UNIP), esta estação meteorológica coleta dados em tempo real sobre temperatura, umidade, qualidade do ar e luminosidade, além de possuir um sensor ultrassônico voltado para pluviometria. 

O projeto está estruturado em um ecossistema monorepo, preparado para evoluir e suportar uma futura integração com banco de dados e dashboard web.

---

## 🚀 Funcionalidades Atuais (Firmware)

- **Clima:** Leitura de temperatura e umidade relativa do ar.
- **Qualidade do Ar:** Medição analógica da concentração de gases e poluição.
- **Luminosidade:** Identificação de ambiente claro ou escuro com base em limites de intensidade da luz.
- **Pluviometria:** Medição do nível de água via ultrassom para estimativa de volume de chuva.

---

## 🛠️ Hardware Utilizado

A prototipagem física e simulada (via Wokwi) utiliza os seguintes componentes principais:

| Componente | Função |
| :--- | :--- |
| **ESP32** | Microcontrolador central |
| **DHT22** | Temperatura e Umidade |
| **MQ135** | Qualidade do Ar (Gás) |
| **LDR** | Luminosidade |
| **HC-SR04** | Ultrassônico para Pluviometria |

---

## 📂 Arquitetura do Repositório

O projeto adota uma estrutura monorepo para concentrar todo o ecossistema (IoT, backend e frontend) num único local.

```text
estacao-meteorologica/
├── firmware/            # Código do ESP32 (main.py) e circuito (diagram.json)
├── backend/             # [Futuro] API e lógica de base de dados
├── frontend/            # [Futuro] Dashboard web para visualização de dados
├── docs/                # Documentação técnica e relatórios do projeto
└── README.md            # Documentação central do repositório
