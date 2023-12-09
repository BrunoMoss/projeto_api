import pandas as pd
from  pandas.tseries.offsets import BMonthEnd
from pandas.tseries.holiday import AbstractHolidayCalendar,Holiday
from datetime import timedelta

class DiaUtil(AbstractHolidayCalendar):

    def __init__(self):
        df= pd.read_excel(r'projeto-api\database\feriados_nacionais.xlsx',header=0)
        df['Feriados'] = pd.to_datetime(df['Feriados'])
        self.rules = [Holiday('Feriado',month=feriado.month,day=feriado.day,year=feriado.year) for feriado in df['Feriados']]

    def diautilmesanterior(self,dt):
        #data = pd.to_datetime('2023-10-25')
        # Obtenha o último dia útil do mês anterior, considerando feriados
        ultimo_dia_util = pd.bdate_range(end=dt - BMonthEnd(1), periods=1,freq='C', holidays=self.rules).date[0]

        return ultimo_dia_util
    
    def calculadiautil(self,dt,n):
        if n == 0 :
            dia_util = pd.bdate_range(end=dt, periods=1,freq='C' ,holidays=self.rules).date[0]
        elif n > 0:
            dia_util = pd.bdate_range(dt + timedelta(days=1), periods=n,freq='C' ,holidays=self.rules).date[0]
        else:
            dia_util = pd.bdate_range(end=dt + timedelta(days=-1), periods=abs(n),freq='C' ,holidays=self.rules).date[0]
        return dia_util

