import pyodbc
import os
from dotenv import load_dotenv

import pandas as pd

load_dotenv()

# df_trp = pd.read_csv("./src/Transporte.csv", delimiter=',')
# df_trp['Data_Hora'] = pd.to_datetime(df_trp['Data_Hora'], format= '%Y-%m-%d')
# df_ativo = df_trp[df_trp['Sku'] == 2]
# print(df_ativo)

server   = os.getenv('SERVER')
database = os.getenv('DATABASE')
username = os.getenv('USER')
password = os.getenv('PWD')

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)
coursor = cnxn.cursor()

query = "SELECT Data_Hora, Sku, DPL_cont, UIP_cont, Ech1_cont, Ech2_cont, Rt1_cont, Rt2_cont, Epc1_cont, Pal_cont FROM [UB].[Packaging].[L541_trp] WHERE CONVERT(date, Data_Hora) = CONVERT(date , CURRENT_TIMESTAMP) ORDER BY Data_Hora ASC"
df = pd.read_sql(query,cnxn)
print(df.head(20))
