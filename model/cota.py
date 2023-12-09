from sqlalchemy import Column, String, DateTime, ForeignKey,Float,Integer
from datetime import datetime
from typing import Union

from  model import Base


class Cota(Base):
    
    __tablename__ = 'cota'

    cnpj = Column(String(12),ForeignKey("fundo.cnpj"), nullable=False,primary_key=True)
    dt_comptc = Column(DateTime,primary_key=True)
    vl_cota = Column(Float(8))
    vl_patrim_liq = Column(Float(2))
    captc_dia = Column(Float(2))
    resg_dia = Column(Float(2))
    nr_cotst = Column(Integer)
    data_insercao = Column(DateTime, default=datetime.now())


    def __init__(self, cnpj:str, dt_comptc:DateTime,vl_cota:float,vl_patrim_liq:float,
                captc_dia:float,resg_dia:float,nr_cotst:int,
                data_insercao:Union[DateTime, None] = None):
        """
        Cadastra uma cota

        Arguments:
            cnpj: cnpj do fundo.
            dt_comptc: data da cota
            vl_cota: valor da cota do fundo para a data de referência
            vl_patrim_liq: valor do patrimônio líquido para a data de referência
            captc_dia: valor dos aportes para data de referência
            resg_dia: valor dos resgates para a data de referência
            nr_cotst: número de cotistas do fundo para a data de referência
            data_insercao: data de quando a cota foi inserida na base
        """
        self.cnpj = cnpj
        self.dt_comptc = dt_comptc
        self.vl_cota = vl_cota
        self.vl_patrim_liq = vl_patrim_liq
        self.captc_dia = captc_dia
        self.resg_dia = resg_dia
        self.nr_cotst = nr_cotst
        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao