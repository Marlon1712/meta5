# importando bibliotecas
import yfinance as yf
import pandas as pd
import numpy as np
import telegram
import warnings
import os
from dotenv import load_dotenv
import time
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots

load_dotenv()

token = os.getenv('MY_TOKEN')
chat_id = os.getenv('CHAT_ID')

warnings.filterwarnings('ignore')

ativoSelecionado = 'BOVA11'
empresa = 'bovespa'
ativoSelecionado1 = 'BOVA11.SA'



while True :
    
    ativo = yf.Ticker(ativoSelecionado1)
    ativo_mes = ativo.history(period='30d', interval='5m')
    ativo_mes = ativo_mes.Close
    df_ativo_mes = pd.DataFrame(ativo_mes)
    df_ativo_mes.reset_index(inplace=True)
    #Pegar ultimo valor negociado
    ativo_dia_ultimo_preco = df_ativo_mes
    #renomear as colunas
    ativo_dia_ultimo_preco.rename(columns={'Datetime': 'data_pregao', 'Close':'preco_fechamento'}, inplace=True)

    df_ativo_Ultimo_preco = pd.DataFrame(ativo_dia_ultimo_preco)

    #ajustar data
    df_ativo_Ultimo_preco['data_pregao'] = pd.to_datetime(df_ativo_Ultimo_preco['data_pregao'], utc=True).dt.date


    #calculo do macd
    rapidaMME = df_ativo_Ultimo_preco.preco_fechamento.ewm(span=12).mean()
    lentaMME = df_ativo_Ultimo_preco.preco_fechamento.ewm(span=26).mean()
    MACD = rapidaMME - lentaMME
    sinal = MACD.ewm(span=9).mean()
    df_ativo_Ultimo_preco['MACD'] = MACD
    df_ativo_Ultimo_preco['sinal'] = sinal

    #ajuste index e retira data pregao
    df_ativo_Ultimo_preco = df_ativo_Ultimo_preco.set_index(pd.DatetimeIndex(df_ativo_Ultimo_preco['data_pregao'].values))
    df_ativo_Ultimo_preco = df_ativo_Ultimo_preco.drop(columns='data_pregao')

    #Criar codigo para verificar a compra ou venda
    df_ativo_Ultimo_preco['flag'] =''
    df_ativo_Ultimo_preco['preco_compra']= np.nan
    df_ativo_Ultimo_preco['preco_venda'] = np.nan
    for i in range(1, len(df_ativo_Ultimo_preco.sinal)):
        if df_ativo_Ultimo_preco['MACD'][i] > df_ativo_Ultimo_preco['sinal'][i]:
            if df_ativo_Ultimo_preco['flag'][i-1] == 'C':
                df_ativo_Ultimo_preco['flag'][i] = 'C'
            else:
                df_ativo_Ultimo_preco['flag'][i] = 'C'
                df_ativo_Ultimo_preco['preco_compra'][i] = df_ativo_Ultimo_preco['preco_fechamento'][i]

        elif df_ativo_Ultimo_preco['MACD'][i] < df_ativo_Ultimo_preco['sinal'][i]:
            if df_ativo_Ultimo_preco['flag'][i-1] == 'V':
                df_ativo_Ultimo_preco['flag'][i] = 'V'
            else:
                df_ativo_Ultimo_preco['flag'][i] = 'V'
                df_ativo_Ultimo_preco['preco_venda'][i] = df_ativo_Ultimo_preco['preco_fechamento'][i]

        df_plot = df_ativo_Ultimo_preco
    fig =go.Figure()
    fig.add_trace(go.Scatter(x= df_plot.index,
                            y= df_plot['preco_fechamento'],
                            name= 'Preco fechamento',
                            line_color= '#FEC852'
                            ))
    fig.add_trace(go.Scatter(x= df_plot.index,
                            y= df_plot['preco_compra'],
                            name= 'Compra',
                            mode= 'markers',
                            marker= dict(
                                color='#00cc96',
                                size=10,
                                )
                            ))
    fig.add_trace(go.Scatter(x= df_plot.index,
                            y= df_plot['preco_venda'],
                            name= 'Venda',
                            mode= 'markers',
                            marker= dict(
                                color='#EF5538',
                                size=10,
                                )
                            ))

    #fig.show()

    def envia_mensagem(msg,chat_id, token ):
        bot = telegram.Bot(token= token)
        bot.sendMessage(chat_id = chat_id, text= msg)

    hoje = df_ativo_Ultimo_preco.flag[-1]
    ontem = df_ativo_Ultimo_preco.flag[-2]
    flag = hoje

    preco_fechamento = round(df_ativo_Ultimo_preco.preco_fechamento.tail(1)[-1],2)
    msg = f'{ativoSelecionado} ({empresa}), {flag} preço de fechamento : R${preco_fechamento}'

    if ontem != hoje:
        envia_mensagem(msg, chat_id, token)

    time.sleep(300)
