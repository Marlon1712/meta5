# importando bibliotecas
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
import telegram
import warnings

warnings.filterwarnings('ignore')
df = pd.read_csv("./notebooks/b3/all_bovespa.csv", delimiter=',')

#Ativo
ativoSelecionado = 'NUBR33'
ativoSelecionado1 = 'NUBR33.SA'
df_ativo = df[df['sigla_acao'] == ativoSelecionado]
df_ativo = df_ativo[['data_pregao','preco_fechamento']]
#Mudar o tipo data
df_ativo['data_pregao'] = pd.to_datetime(df_ativo['data_pregao'], format= '%Y-%m-%d')
#escolher uma ação
itub = yf.Ticker(ativoSelecionado1)
#escolher intervalo de dados
itub_dia = itub.history(period='id', interval='5m')
#Pegar preço de fechamento
itub_dia = itub_dia.Close
#transforma em df
df_itub_dia = pd.DataFrame(itub_dia)
#reset index
df_itub_dia.reset_index(inplace=True)
#Pegar ultimo valor negociado
itub_dia_ultimo_preco = df_itub_dia.tail(1)
#renomear as colunas
itub_dia_ultimo_preco.rename(columns={'Datetime': 'data_pregao', 'Close':'preco_fechamento'}, inplace=True)
#remove a ultima data
df_remove = df_ativo.loc[(df_ativo['data_pregao'] == pd.to_datetime('today').normalize())]
df_ativo = df_ativo.drop(df_remove.index )
#append data atual
df_itub_total = df_ativo.append(itub_dia_ultimo_preco)
#ajustar data
df_itub_total['data_pregao'] = pd.to_datetime(df_itub_total['data_pregao'], utc=True).dt.date
#calculo do macd
rapidaMME = df_itub_total.preco_fechamento.ewm(span=12).mean()
lentaMME = df_itub_total.preco_fechamento.ewm(span=26).mean()
MACD = rapidaMME - lentaMME
sinal = MACD.ewm(span=9).mean()
df_itub_total['MACD'] = MACD
df_itub_total['sinal'] = sinal
#ajuste index e retira data pregao
df_itub_total = df_itub_total.set_index(pd.DatetimeIndex(df_itub_total['data_pregao'].values))
df_itub_total = df_itub_total.drop(columns='data_pregao')
#Criar codigo para verificar a compra ou venda
df_itub_total['flag'] =''
df_itub_total['preco_compra']= np.nan
df_itub_total['preco_venda'] = np.nan
for i in range(1, len(df_itub_total.sinal)):
    if df_itub_total['MACD'][i] > df_itub_total['sinal'][i]:
        if df_itub_total['flag'][i-1] == 'C':
            df_itub_total['flag'][i] = 'C'
        else:
            df_itub_total['flag'][i] = 'C'
            df_itub_total['preco_compra'][i] = df_itub_total['preco_fechamento'][i]

    elif df_itub_total['MACD'][i] < df_itub_total['sinal'][i]:
        if df_itub_total['flag'][i-1] == 'V':
            df_itub_total['flag'][i] = 'V'
        else:
            df_itub_total['flag'][i] = 'V'
            df_itub_total['preco_venda'][i] = df_itub_total['preco_fechamento'][i]

df_plot = df_itub_total
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

fig.show()

my_token = '5057104135:AAFgQkI4cxDZufLWm7RdUfspaBmJcd0lTrw'
chat_id = '-641638826'

def envia_mensagem(msg,chat_id, token = my_token):
    bot = telegram.Bot(token= token)
    bot.sendMessage(chat_id = chat_id, text= msg)

hoje = df_itub_total.flag[-1]
ontem = df_itub_total.flag[-2]
flag = hoje

preco_fechamento = round(df_itub_total.preco_fechamento.tail(1)[-1],2)
msg = f'{ativoSelecionado}, {flag} preço de fechamento : R${preco_fechamento}'

if ontem != hoje:
    envia_mensagem(msg, chat_id, my_token)
