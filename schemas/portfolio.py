from unicodedata import category
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from collections import defaultdict
from sqlalchemy.inspection import inspect
import pandas as pd

class BuscaPortfolioSchema(BaseModel):
    lista_cnpj: List[str] = None
    data_referencia: datetime = None
   

class PortfolioViewSchema(BaseModel):
    cd_ativo: str = "PETR4"
    qtd_negociada:  float = 0.0
    vl_negociado: float = 0.0
    qt_pos_final: float = 0.0
    vl_merc_pos_final: float = 0.0
    dt_comptc_ant : float = 0.0
    vl_merc_pos_final_ant: float = 0.0
    vl_resultado: float = 0.0
    PnL: float = 0.0

class PortfolioFundoViewSchema(BaseModel):
    razao_social: str = "BRAM H FUNDO DE INVESTIMENTO AÇÕES INSTITUCIONAL"
    dt_comptc: datetime = datetime(2023,1,1)
    portfolio: List[PortfolioViewSchema]

class PortfolioFundosViewSchema(BaseModel):
    portfolios : List[PortfolioFundoViewSchema]

def apresenta_portfolio(portfoliofundo):
    return {
        "razao_social": portfoliofundo["razao_social"],
        "dt_comptc": portfoliofundo["dt_comptc"],
        "portfolio":
                    [
                        {
                            "cd_ativo": p["cd_ativo"],
                            "qtd_negociada": p["qtd_negociada"],
                            "vl_negociado": p["vl_negociado"],
                            "qt_pos_final": p["qt_pos_final"],
                            "vl_merc_pos_final": p["vl_merc_pos_final"],
                            "dt_comptc_ant": p["dt_comptc_ant"],
                            "vl_merc_pos_final_ant": p["vl_merc_pos_final_ant"],
                            "vl_resultado": p["vl_resultado"],
                            "PnL": p["PnL"]
                        } for p in portfoliofundo["portfolio"]
                    ]
    }

def query_to_dict(rset):
    result = defaultdict(list)
    for obj in rset:
        instance = inspect(obj)
        for key, x in instance.attrs.items():
            result[key].append(x.value)
    return result

def apresenta_lista_portfolio(df):
    
    result = []

    # Dicionário temporário para agrupar por CNPJ e dt_comptc
    temp_dict = defaultdict(list)

    # Agrupamento dos itens no dicionário temporário
    for index,item in df.iterrows():
        key = (item['razao_social'], item['dt_comptc'])
        temp_dict[key].append({
            "cd_ativo": item['cd_ativo'],
            "qtd_negociada": item['qtd_negociada'],
            "vl_negociado": item['vl_negociado'],
            "qt_pos_final": item['qt_pos_final'],
            "vl_merc_pos_final": item['vl_merc_pos_final'],
            "dt_comptc_ant": item['dt_comptc_ant'],
            "vl_merc_pos_final_ant": item['vl_merc_pos_final_ant'],
            "vl_resultado":item['vl_resultado'],
            "PnL":item['PnL']
        })

    # Transformação para a segunda estrutura
    lista_transformada = [
        {
            "razao_social": razao_social,
            "dt_comptc": dt_comptc,
            "portfolio": portifolio
        }
        for (razao_social, dt_comptc), portifolio in temp_dict.items()
    ]
    for portfoliofundo in lista_transformada:
        result.append(apresenta_portfolio(portfoliofundo))

    return {"portfoliosFundos": result}
