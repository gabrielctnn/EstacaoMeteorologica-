from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from models import LeituraSensorModel
from database import get_db, engine, Base
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI() #INSTÂNCIA DO SERVIDOR: Cria a aplicação base da nossa API.
Base.metadata.create_all(bind=engine) #instrução que obriga o SQLAlchemy a criar fisicamente as tabelas dentro do teu banco de dados.
app.add_middleware(
      CORSMiddleware,
      allow_origins=["*"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"]
)

class SensorsData(BaseModel): #classe que armazenará o pacote JSON que o ESP32 enviar, e com o basemodel tipando
      #Field permite embutir regras matematicas diretamente na classe. ge = maior ou igual a;le=menor ou igual a
      temperaturaDHT: float = Field(ge=-40.0, le=100.0, description="°C")
      umidadeDHT: float = Field(ge=0.0, le=100.0, description="%")
      valorAr: int = Field(ge=0, le=4095, description="Valor bruto ADC (0-4095)")
      luminosidade: int = Field(ge=0, le=4095, description="Valor bruto ADC (0-4095)")
      distancia: float = Field(ge=0.0, description="cm")
      pressao: float = Field(ge=300.0, le=1100.0, description="hPa")


@app.get("/") #cria a rota(ENDPOINT)  da porta do servidor, get pois esta solicitando as info, "/" indica raiz do projeto
async def root():
    return {"message": "Hello World"} #basicamente diz q que quando bater na raiz do proejto devolver isso


@app.post("/sensors") #Endpoint criado para receber/escrever no endereço sensors
async def dataReceive (data: SensorsData, db: Session = Depends(get_db)): #db cria a sessão para abrir  armazenar os dados e fechar
        #Cria o registro usando o modelo do banco e os dados validados pelo SensorsData
        novo_registro = LeituraSensorModel(
            temperatura=data.temperaturaDHT,
            umidade=data.umidadeDHT,
            valorAr=data.valorAr,
            luminosidade=data.luminosidade,
            distancia=data.distancia,
            pressao=data.pressao
        )   

        #Grava os dados no banco
        db.add(novo_registro)
        db.commit()

        #Atualiza o objeto para garantir o ID que o  banco gerou pro registro
        db.refresh(novo_registro)


        return {"Mensagem": "Dados guardados com sucesso!", "dados": novo_registro }

@app.get("/sensors") #endpoint criado para pegar os dados do db e mandar para o front
async def dataSend (db: Session = Depends(get_db)):
    envioFront = db.query(LeituraSensorModel).all() #busca as informações na sessão atual do db, no alvo LeituraSensorModel
    return {"Dados enviados com sucesso:": envioFront}