import pandas as pd
from datetime import datetime
import time
import MetaTrader5 as mt5

#conecte-se ao MetaTrader5
if not mt5.initialize():
    print("initilize() falhou")
    mt5.shutdown()

#ativos = mt5.symbols_get()
# for i in range(10):
#     print(ativos[i].name)

#Obtendo Cotações
# frame = mt5.copy_rates_from_pos('WDOU20', mt5.TIMEFRAME_M1,0,1)
# print(frame)

def get_ohlc(ativo,timeframe, n=5):
    ativo = mt5.copy_rates_from_pos(ativo,timeframe,0,n)
    ativo = pd.DataFrame(ativo)
    ativo['time']=pd.to_datetime(ativo['time'], unit='s')
    ativo.set_index('time',inplace=True)
    return ativo

# print(get_ohlc('WIN$', mt5.TIMEFRAME_M1,))
tempo = time.time() + 10
while time.time() < tempo:
    tick = mt5.symbol_info_tick('WDOU20')
    print(f"WIN - last:{tick.last}, bid:{tick.bid}, ask:{tick.ask}", end='\r')
    time.sleep(0.5)