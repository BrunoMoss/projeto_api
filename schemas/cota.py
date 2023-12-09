from unicodedata import category
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class BuscaCotaSchema(BaseModel):
    lista_cnpj: List[str] = None
    data_inicial: datetime = None
    data_final: datetime = None
    


class CotaViewSchema(BaseModel):
    dt_comptc: datetime = datetime(2023,1,1)
    vl_cota:  float = 0.0
    captc_dia:  float = 0.0
    resg_dia: float = 0.0
    nr_cotst: int = 0
    vl_patrim_liq: float=0.0

class CotaFundoViewSchema(BaseModel):
    razao_social: str = "BRAM H FUNDO DE INVESTIMENTO AÇÕES INSTITUCIONAL"
    cotas:List[CotaViewSchema]

class CotasFundosViewSchema(BaseModel):
    portfolios : List[CotaFundoViewSchema]

def apresenta_cota(fundo_cotas):
     
    return {
        "razao_social": fundo_cotas.razao_social,
        "cotas":[
                    {
                        "dt_comptc": cota.dt_comptc,
                        "vl_cota": cota.vl_cota,
                        "captc_dia": cota.captc_dia,
                        "resg_dia": cota.resg_dia,
                        "nr_cotst": cota.nr_cotst,
                        "vl_patrim_liq": cota.vl_patrim_liq
                    } for cota in fundo_cotas.cota
                ]
    } 


class CotaListaViewSchema(BaseModel):
    cotas: List[CotaViewSchema]


def apresenta_lista_cotas(fundos_cotas):
    result = []
    for fundo_cota in fundos_cotas:
        result.append(apresenta_cota(fundo_cota))
    return {"cotas_fundos": result}
