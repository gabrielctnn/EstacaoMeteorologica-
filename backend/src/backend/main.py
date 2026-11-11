from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from models import LeituraSensorModel
from database import get_db, engine, Base
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI() #INSTÂNCIA DO SERVIDOR: Cria a aplicação base da nossa API.
app.add_middleware(
      CORSMiddleware,
      allow_origins=["*"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"]
)

class SensorsData(BaseModel): #classe que armazenará o pacote JSON que o ESP32 enviar, e com o basemodel tipando
      #Field permite embutir regras matematicas diretamente na classe. ge = maior ou igual a;le=menor ou igual a
      dispositivo_id: int
      temperaturaDHT: float | None = Field(ge=-40.0, le=100.0, description="°C")
      umidadeDHT: float | None = Field(ge=0.0, le=100.0, description="%")
      valorAr: int = Field(ge=0, le=4095, description="Valor bruto ADC (0-4095)")
      luminosidade: int = Field(ge=0, le=4095, description="Valor bruto ADC (0-4095)")
      precipitacao: float = Field(ge=0.0, description="mm")
      pressao: float = Field(ge=300.0, le=1100.0, description="hPa")

# Função normal Python (sem @property)
def classificar_qualidadeAr(valorAr: int) -> str:
    if valorAr <= 1200:
        return "BOM / Limpo"
    elif valorAr <= 2200:
        return "MODERADO / Aceitável"
    elif valorAr <= 3200:
        return "POLUÍDO / Cuidado"
    else:
        return "PÉSSIMO / Perigoso"
    
@app.get("/") #cria a rota(ENDPOINT)  da porta do servidor, get pois esta solicitando as info, "/" indica raiz do projeto
async def root():
    return {"message": "Hello World"} #basicamente diz q que quando bater na raiz do proejto devolver isso


@app.post("/sensors") #Endpoint com metodo POST criado para receber/escrever no endereço sensors
async def dataReceive (data: SensorsData, db: Session = Depends(get_db)): #db cria a sessão para abrir  armazenar os dados e fechar
        #Cria o registro usando o modelo do banco e os dados validados pelo SensorsData
        novo_registro = LeituraSensorModel(
            dispositivo_id=data.dispositivo_id,
            temperatura=data.temperaturaDHT,
            umidade=data.umidadeDHT,
            valorAr=data.valorAr,
            qualidadeArStatus=classificar_qualidadeAr(data.valorAr),
            luminosidade=data.luminosidade,
            precipitacao=data.precipitacao,
            pressao=data.pressao
        )   

        #Grava os dados no banco
        db.add(novo_registro)
        db.commit()

        #Atualiza o objeto para garantir o ID que o  banco gerou pro registro
        db.refresh(novo_registro)


        # Faz a inclusão do texto para Valor Ar Visualmente mais facil
        resposta = {
            "id": novo_registro.id,
            "dispositivo_id": novo_registro.dispositivo_id,
            "temperatura": novo_registro.temperatura,
            "umidade": novo_registro.umidade,
            "valorAr": novo_registro.valorAr,
            "qualidadeArStatus": classificar_qualidadeAr(novo_registro.valorAr),
            "luminosidade": novo_registro.luminosidade,
            "precipitacao": novo_registro.precipitacao,
            "pressao": novo_registro.pressao
        }

        return {"Mensagem": "Dados guardados com sucesso!", "dados": resposta }

@app.get("/sensors") #endpoint metodo GET criado para pegar os dados do db e mandar para o front
async def dataSend (db: Session = Depends(get_db)):
    envioFront = db.query(LeituraSensorModel).all() #busca as informações na sessão atual do db, no alvo LeituraSensorModel
    return {"Dados enviados com sucesso:": envioFront}

