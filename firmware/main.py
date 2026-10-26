import dht  # Importa biblioteca do sensor DHT22 (já vem no MicroPython)
from machine import Pin, ADC, time_pulse_us, I2C #importa a classe Pin, que controla os pinos GPIO do ESP32, e o ADC para o pino Analogico
import time, network, urequests 
#from bmp280 import BMP280 -> biblioteca pro BMP280

#conexão a rede
estacao = network.WLAN(network.STA_IF) #configura o wifi para modo de estação preparando para ligar em um router 
estacao.active(True) 
if not estacao.isconnected():
    estacao.connect("Wokwi-GUEST", "")
    print("Aguardando conexão...")
    while not estacao.isconnected():
        time.sleep(1)
print(f"Conexão estabelecida: {estacao.ifconfig()[0]}")


DHT = dht.DHT22(Pin(4)) # Cria o objeto do sensor, informando o modelo (DHT22) e o GPIO onde o fio de dados está ligado (GPIO 4).

MQ135 = ADC(Pin(34)) #cria a variavel que recebe os dados analogicos da porta ADC pelo pin34
MQ135.atten(ADC.ATTN_11DB)# Atenuação de 11 dB: amplia a faixa de tensão aceita para cerca de 0 a 3,3 V. Sem isso a faixa seria bem menor (cerca de 0 a 1 V). O ADC tem 12 bits de resolução: devolve valores de 0 a 4095.

LDR = ADC(Pin(32))
LDR.atten(ADC.ATTN_11DB)

hcTRIG = Pin(18, Pin.OUT)
hcECHO = Pin(19, Pin.IN)

#COMANDOS PARA COLOCAR QUANDO TIVER O BMP280 EM MÃOS
# Mapeia os pinos do barramento I2C do BMP280
# i2c = I2C(0, scl=Pin(22), sda=Pin(21))
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



while True:
  DHT.measure() #Inicializa o sensor
  time.sleep(2)
  print("DHT22 LIGADO - Recebendo dados\n")
  temperaturaDHT = DHT.temperature()
  umidadeDHT = DHT.humidity()
  time.sleep(3)
  print(f"DADOS DHT22: \nTemperatura: {temperaturaDHT}°C\nUmidade: {umidadeDHT}%\n")


  time.sleep(2)
  print("MQ135 LIGADO - Recebendo dados\n")
  valorAr = MQ135.read()
  time.sleep(3)
  print(f"DADOS MQ135: \nQualidade do ar(Quanto maior valor, mais poluído): {valorAr} / 4095 \n")

  time.sleep(2)
  print("LDR LIGADO - Recebendo dados\n")
  LDR.read()
  luminosidade = LDR.read()
  time.sleep(3)
  LIMITE_LUZ = 2000 #passou disso ta escuro
  if luminosidade > LIMITE_LUZ:
      ambiente = "ESCURO"
  else:
      ambiente = "CLARO"

  print(f"DADOS LDR: \nIntensidade da luz: {luminosidade} / 4095 - Ambiente: {ambiente}\n")

  time.sleep(2)
  print("HC-SR04 LIGADO - Recebendo dados\n")
  time.sleep(3)
  distancia = calculoDistancia() or 0.0
  if distancia is not None:
    print(f"DADOS HC-SR04: \nDistância: {distancia:.2f} cm\n")
  else:
    print("Fora de alcance ou erro na medição\n")
    time.sleep(1)
         
# COMANDOS DO BMP280 NO LOOP (DESCOMENTAR NO HARDWARE FÍSICO)
  # time.sleep(2)
  # print("BMP280 LIGADO - Recebendo dados\n")
  # time.sleep(3)
  # pressao = bmp.pressure
  # print(f"DADOS BMP280: \nPressão Atmosférica: {pressao:.2f} hPa\n")
  # #base JSON

  #pacote JSON com os DADOS
  dadosSensores = { 
        "temperaturaDHT": temperaturaDHT,
        "umidadeDHT": umidadeDHT,
        "valorAr": valorAr,
        "luminosidade": luminosidade,
        "distancia": distancia,
        "pressao": 1013.25 #Depois colocar a variavel quando tiver no sensor fisico
    }

#Eenvio dos dados pelo metodo POST DO HTTP
  envioDados = urequests.post("https://179.228.212.64:8000/sensors", json=dadosSensores)
  print(envioDados.text)
  envioDados.close()    