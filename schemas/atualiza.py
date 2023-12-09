from unicodedata import category
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class AtualizaSchema(BaseModel):
    datainicial: datetime = datetime(2023,1,1)
    datafinal: datetime = datetime(2023,7,1)
    tarefa: str = "Todos"


class AtualizaViewSchema(BaseModel):
    nome_tarefa: str = "Dados Cadastrais de Fundos"
    status: str = "OK"
    qtd_arquivos: int = 1

def resultado_atualizacao(resultado_tarefa):
     
    return {
       
        "tarefa": resultado_tarefa[0],
        "status": resultado_tarefa[1],
        "qtd_arquivos": resultado_tarefa[2]
    }
