import dht  # Importa biblioteca do sensor DHT22 (já vem no MicroPython)
from machine import Pin, ADC, time_pulse_us, I2C #importa a classe Pin, que controla os pinos GPIO do ESP32, e o ADC para o pino Analogico
import time, network, urequests 
import config
#from bmp280 import BMP280 -> biblioteca pro BMP280

estacao = network.WLAN(network.STA_IF) #configura o wifi para modo de estação preparando para ligar em um router 
estacao.active(False)
time.sleep(1)
estacao.active(True)
time.sleep(2)

#conexão a rede
def conexaoRede():
    if not estacao.isconnected():
        estacao.connect(config.WIFI_SSID, config.WIFI_SENHA) #trocar isso pelo wifi e as aspas vazia pela senha quando tiver o esquema montado
        print("Aguardando conexão...")
        tentativas = 0
        while not estacao.isconnected() and tentativas < 20:
            time.sleep(1)
            tentativas+=1

    if estacao.isconnected():
        print(f"Conexão estabelecida: {estacao.ifconfig()[0]}")
    else :
        print("Falha ao conectar a placa ao WIFI!")


DHT = dht.DHT22(Pin(15)) # Cria o objeto do sensor, informando o modelo (DHT22) e o GPIO onde o fio de dados está ligado (TROCAR PARA A IGUAL DO FISICO).

MQ135 = ADC(Pin(34)) #cria a variavel que recebe os dados analogicos da porta ADC (TROCAR PARA A IGUAL DO FISICO)
MQ135.atten(ADC.ATTN_11DB)# Atenuação de 11 dB: amplia a faixa de tensão aceita para cerca de 0 a 3,3 V. Sem isso a faixa seria bem menor (cerca de 0 a 1 V). O ADC tem 12 bits de resolução: devolve valores de 0 a 4095.

LDR = ADC(Pin(32)) #(TROCAR PARA A IGUAL DO FISICO)
LDR.atten(ADC.ATTN_11DB)

#hcTRIG = Pin(18, Pin.OUT) #(TROCAR PARA A IGUAL DO FISICO)
#hcECHO = Pin(19, Pin.IN)#(TROCAR PARA A IGUAL DO FISICO)

#COMANDOS PARA COLOCAR QUANDO TIVER O BMP280 EM MÃOS
# Mapeia os pinos do barramento I2C do BMP280
# i2c = I2C(0, scl=Pin(22), sda=Pin(21)) (TROCAR PARA A IGUAL DO FISICO)
# Inicializa o sensor (Se der erro ETIMEDOUT no hardware real, alterar o addr para 0x76)
# bmp = BMP280(i2c, addr=0x77)


def calculoDistancia():
    hcTRIG.value(0) # TRIG em 0 para começar limpo
    time.sleep_us(2)
    
    # Envia o pulso de 10 microsegundos para acionar o sensor
    hcTRIG.value(1)
    time.sleep_us(10)
    hcTRIG.value(0)
    
    # mede por quanto tempo  o ECHO fica em HIGH; desiste após 30000 
    duracao = time_pulse_us(hcECHO, 1, 30000)
    
    # Se o sensor ultrapassar o tempo limite (sem obstáculo), retorna None
    if duracao < 0:
        return None
        
    # o som anda 0,0343 cm por microsegundos; divide por 2 porque o tempo é de ida e volta
    distancia = (duracao * 0.0343) / 2
    return distancia


conexaoRede()
while True:
  try:
    DHT.measure() #Inicializa o sensor
    temperaturaDHT = DHT.temperature()
    umidadeDHT = DHT.humidity()
    print(f"DADOS DHT22: \nTemperatura: {temperaturaDHT}°C\nUmidade: {umidadeDHT}%\n")
  except OSError:
      print("Erro na leitura do DHT22\n")
      temperaturaDHT = None
      umidadeDHT = None


  valorAr = MQ135.read()
  
  print(f"DADOS MQ135: \nQualidade do ar(Quanto maior valor, mais poluído): {valorAr} / 4095 \n")


  luminosidade = LDR.read()
  LIMITE_LUZ = 400 #passou disso ta escuro
  if luminosidade < LIMITE_LUZ:
      ambiente = "ESCURO"
  else:
      ambiente = "CLARO"
  print(f"DADOS LDR: \nIntensidade da luz: {luminosidade} / 4095 - Ambiente: {ambiente}\n")

 # alturaRecipiente = 20.0 #Trocar pela altura do recipiente escolhido, no caso atual 20cm

 # distancia = calculoDistancia()
  #if distancia is not None:
 #   #A diferença é a altura da agua no recipiente que esta em CM
   # nivelChuva = alturaRecipiente - distancia

    #if nivelChuva < 0: 
     #   nivelChuva = 0.0

    #nivelChuva *= 10 #Converte para mm
    #print(f"DADOS HC-SR04: \nDistância: {nivelChuva:.2f} mm\n")
   # nivelChuva_json = nivelChuva
  #else:
    #print("Fora de alcance ou erro na medição\n")
    #nivelChuva_json = None

         
# COMANDOS DO BMP280 NO LOOP (DESCOMENTAR NO HARDWARE FÍSICO)
  # pressao = bmp.pressure
  # print(f"DADOS BMP280: \nPressão Atmosférica: {pressao:.2f} hPa\n")

  #pacote JSON com os DADOS
  dadosSensores = { 
        "dispositivo_id": 1,
        "temperaturaDHT": temperaturaDHT,
        "umidadeDHT": umidadeDHT,
        "valorAr": valorAr,
        "luminosidade": luminosidade,
        "precipitacao": None, #nivelChuva_json,
        "pressao": None #Depois colocar a variavel quando tiver no sensor fisico
  }
    #Try/catch para envio dos dados pelo metodo POST DO HTTP
  if not estacao.isconnected():
    conexaoRede()
  try:
        envioDados = urequests.post(config.API_URL, json=dadosSensores,
        timeout=10)
        print("Resposta API:", envioDados.text)
        envioDados.close() 
  except Exception as e:
        print("Erro ao enviar os dados para a API:", e)

  time.sleep(10)