from sqlalchemy import Column, String, DateTime, ForeignKey,Float
from datetime import datetime
from typing import Union

from  model import Base


class Portfolio(Base):
    
    __tablename__ = 'portfolio'

    cnpj = Column(String(12),ForeignKey("fundo.cnpj"), nullable=False,primary_key=True)
    dt_comptc = Column(DateTime,primary_key=True)
    cd_ativo = Column(String(100),primary_key=True)
    #ds_ativo = Column(String(100))
    cd_isin = Column(String(12))
    #tp_aplic = Column(String(150))
    #tp_ativo = Column(String(150))
    #tp_negoc = Column(String(24))
    qtd_negociada = Column(Float(6))
    vl_negociado = Column(Float(2))
    qt_pos_final = Column(Float(6))
    vl_merc_pos_final = Column(Float(2))
    data_insercao = Column(DateTime, default=datetime.now())


    def __init__(self, cnpj:str, dt_comptc:DateTime, cd_ativo:str,
                 cd_isin:str,qtd_negociada:float,vl_negociado:float,
                 qt_pos_final:float,vl_merc_pos_final:float,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cadastra um fundo

        Arguments:
            cnpj: cnpj do fundo.
            dt_comptc: data de competência
            cd_ativo: código do ativo
            cd_isin: código ISIN
            qt_venda_negoc: quantidade vendida no mês de competência
            vl_venda_negoc: valor das vendas no mês de competência
            qt_aquis_negoc: quantidade comprada no mês de competência
            vl_aquis_negoc: valor das compras no mês de competência
            qt_pos_final: quatidade total no fechamento do mês de referência
            vl_merc_pos_final:valor de mercado total no fechamento do mês de referência
            data_insercao: data de quando o fundo foi inserido à base
        """
        self.cnpj = cnpj
        self.dt_comptc = dt_comptc
        self.cd_ativo = cd_ativo
        self.cd_isin = cd_isin
        self.qtd_negociada = qtd_negociada
        self.vl_negociado = vl_negociado
        self.qt_pos_final = qt_pos_final
        self.vl_merc_pos_final = vl_merc_pos_final
        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao