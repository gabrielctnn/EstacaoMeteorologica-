from fastapi import FastAPI #importando o framework 
from pydantic import BaseModel, Field

app = FastAPI() #INSTÂNCIA DO SERVIDOR: Cria a aplicação base da nossa API.
class SensorsData(BaseModel): #classe que armazenará o pacote JSON que o ESP32 enviar, e com o basemodel tipando
      #Field permite embutir regras matematicas diretamente na classe. ge = maior ou igual a;le=menor ou igual a
      temperaturaDHT: float = Field(ge=-40.0, le=100.0, description="°C")
      umidadeDHT: float = Field(ge=0.0, le=100.0, description="%")
      valorAr: int = Field(ge=0, le=4095, description="Valor bruto ADC (0-4095)")
      intensidadeLuz: int = Field(ge=0, le=4095, description="Valor bruto ADC (0-4095)")
      distancia: float = Field(ge=0.0, description="cm")
      pressao: float = Field(ge=300.0, le=1100.0, description="hPa")

@app.get("/") #cria a rota(ENDPOINT)  da porta do servidor, get pois esta solicitando as info, "/" indica raiz do projeto
async def root():
    return {"message": "Hello World"} #basicamente diz q que quando bater na raiz do proejto devolver isso

@app.post("/sensors") #Endpoint criado para receber/escrever no endereço sensors
async def dataReceive (data: SensorsData):
        return data #fastapi pega o JSON recebido, valida com a classe SensorsData e salva em "data"