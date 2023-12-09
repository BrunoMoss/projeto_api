from unicodedata import category
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class BuscaFundoSchema(BaseModel):
    cnpj: Optional[str]  = None
    razao_social: Optional[str] = "BRAM H FUNDO DE INVESTIMENTO AÇÕES INSTITUCIONAL"

class BuscaTopFiveSchema(BaseModel):
    classe: str = None
    data_inicial: datetime = None
    data_final: datetime = None

class FundoViewSchema(BaseModel):
    cnpj: str = "01.496.940/0001-86"
    razao_social: str = "BRAM H FUNDO DE INVESTIMENTO AÇÕES INSTITUCIONAL"
    gestor: str = "BRAM - BRADESCO ASSET MANAGEMENT S.A. DISTRIBUIDORA DE TITULOS E VALORES MOBILIARIOS" 
    administrador: str = "BEM - DISTRIBUIDORA DE TITULOS E VALORES MOBILIARIOS LTDA."
    classe_fundo: str = "Ações Índice Ativo"
    tipo_fundo: str = "Fundo de Ações"

def apresenta_fundo(fundo):
     
    return {
        "cnpj": fundo.cnpj,
        "razao_social": fundo.razao_social,
        "gestor": fundo.gestor,
        "administrador": fundo.administrador,
        "classe_fundo": fundo.classe_fundo,
        "tipo_fundo": fundo.tipo_fundo
    }


class FundoListaViewSchema(BaseModel):
    fundos: List[FundoViewSchema]


def apresenta_lista_fundos(fundos):
    result = []
    for fundo in fundos:
        result.append(apresenta_fundo(fundo))
    return {"fundos": result}
