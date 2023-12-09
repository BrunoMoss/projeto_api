from sqlalchemy import Column, String, DateTime
from datetime import datetime
from typing import Union
from sqlalchemy.orm import relationship

from  model import Base


class Fundo(Base):

    __tablename__ = 'fundo'

    cnpj = Column(String(12), primary_key=True)
    razao_social = Column(String(100))
    gestor = Column(String(50))
    administrador = Column(String(50))
    classe_fundo = Column(String(50))
    tipo_fundo = Column(String(50))
    data_insercao = Column(DateTime, default=datetime.now())

    portfolio = relationship("Portfolio")
    cota = relationship("Cota")

    def __init__(self, cnpj:str, razao_social:str, gestor:str,
                 administrador:str,classe_fundo:str,tipo_fundo:str,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cadastra um fundo

        Arguments:
            cnpj: cnpj do fundo.
            razao_social: nome do fundo
            gestor: gestor do fundo
            classe_fundo: classe do fundo
            tipo_fundo: tipo do fundo
            data_insercao: data de quando o fundo foi inserido à base
        """
        self.cnpj = cnpj
        self.razao_social = razao_social
        self.gestor = gestor
        self.administrador = administrador
        self.classe_fundo = classe_fundo
        self.tipo_fundo = tipo_fundo

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao