#importando as bibliotecas
import pandas as pd
from sklearn.feature_selection import SelectKBest
from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from math import floor
import sys
import argparse

def previsaozinha(ativo) -> None:
    #lendo o arquivo de ações 
    #lendo csv
    df = pd.read_csv("./notebooks/b3/all_bovespa.csv", delimiter=',')
    ativo_analise = ativo
    #Ativo
    df_ativo = df[df['sigla_acao'] == ativo_analise]

    #Mudar o tipo data
    df_ativo['data_pregao'] = pd.to_datetime(df_ativo['data_pregao'], format= '%Y-%m-%d')

    #craindo novos campos de medias móveis
    df_ativo['mm5d'] = df_ativo['preco_fechamento'].rolling(8).mean()
    df_ativo['mm21d'] = df_ativo['preco_fechamento'].rolling(21).mean()

    #Empurrando para frente os valores das ações
    df_ativo['preco_fechamento'] = df_ativo['preco_fechamento'].shift(-1)

    #retirando os dados nulos
    df_ativo.dropna(inplace=True)

    #verificando quantidade de linhas
    qtd_linhas = len(df_ativo)
    qtd_linhas_treino = floor(qtd_linhas * 0.25)
    qtd_linhas_teste = qtd_linhas - 15

    qtd_linhas_validadcao = qtd_linhas_treino - qtd_linhas_teste

    info = (
        f"linhas treino= 0:{qtd_linhas_treino} "
        f"linhas teste= {qtd_linhas_treino}:{qtd_linhas_teste} "
        f"linhas validação= {qtd_linhas_teste}:{qtd_linhas}"
    )
    print(info)

    #reindexando o data frame
    df_ativo = df_ativo.reset_index(drop=True)

    #separando as features e labels
    features = df_ativo.drop(['sigla_acao', 'nome_acao', 'data_pregao', 'preco_fechamento'], 1)
    labels = df_ativo['preco_fechamento']

    #Escolendo as melhores features com kbest

    features_list = ('preco_abertura','qtd_negocios','volume_negocios','mm5d','mm21d')

    k_best_features = SelectKBest(k='all')
    k_best_features.fit_transform(features,labels)
    k_best_features_scores = k_best_features.scores_
    raw_pairs = zip(features_list[1:], k_best_features_scores)
    ordered_pairs = list(reversed(sorted(raw_pairs, key=lambda x: x[1])))

    k_best_features_final = dict(ordered_pairs[:15])
    best_features = k_best_features_final.keys()
    print('')
    print("Melhores features:")
    print(k_best_features_final)

    #separando as features escolhidas
    features = df_ativo.drop(columns=['sigla_acao','nome_acao','data_pregao','preco_fechamento','preco_abertura','mm21d'])

    #Normalizando os dados de entrada(features)

    #Gerando o novo padrão
    scaler = MinMaxScaler().fit(features)
    features_scale = scaler.transform(features)

    #Separa os dados de treino teste e validação
    x_train = features_scale[:qtd_linhas_treino]
    x_test = features_scale[qtd_linhas_treino:qtd_linhas_teste]

    y_train = labels[:qtd_linhas_treino]
    y_test = labels[qtd_linhas_treino:qtd_linhas_teste]

    #treinamento usando regressão linear
    lr = linear_model.LinearRegression()
    lr.fit(x_train,y_train)
    pred = lr.predict(x_test)
    cd = r2_score(y_test,pred)

    print(f'Coeficiente de determinação: {cd * 100:.2f}')

    #executando a previsão

    previsao = features_scale[qtd_linhas_teste:qtd_linhas]

    data_pregao_full = df_ativo['data_pregao']
    data_pregao = data_pregao_full[qtd_linhas_teste:qtd_linhas]

    res_full = df_ativo['preco_fechamento']
    res = res_full[qtd_linhas_teste:qtd_linhas]

    pred = lr.predict(previsao)

    df = pd.DataFrame({'data_pregao': data_pregao, 'real': res, 'previsao': pred})
    df['real'] = df['real'].shift(+1) # Retornando valores 

    df.set_index('data_pregao', inplace=True)
    #print(df)
    #grafico
    plt.figure(figsize=(8,4))
    plt.title(f'Preço das ações {ativo_analise}')
    plt.plot(df['real'],label='real', color='blue', marker='o')
    plt.plot(df['previsao'],label='previsao', color='red', marker='o')
    plt.xlabel('Data pregão')
    plt.ylabel('Preço de Fechamento')
    plt.legend()
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='teste arg')  # (1)
    parser.add_argument('--ativo', '-a',required=True,help= "Informe o Código de Negociação do ativo na B3")  #(2)
     
    args = parser.parse_args() #(3)
     
    print("Ativo= {}".format(args.ativo)) # (4)
    previsaozinha(args.ativo)

    return 0
 
if __name__ == '__main__':
    sys.exit(main())