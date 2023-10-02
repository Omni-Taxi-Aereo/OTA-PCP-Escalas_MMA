import send_to_blob
import requests, ast
from datetime import datetime, timedelta
import json
import pprint
import pandas as pd



TOKEN_URL = 'https://api.sigmec.com.br/api/get/token'
ESCALA_URL = 'https://api.sigmec.com.br/api/escala/grade/vencimentos'
ESCALA_URL_PESQUISA = 'https://api.sigmec.com.br/api/escala/grade/vencimentos/pesquisa'
CONTENT = {
    "username": 'srv_api_indicadores@omnibrasil.com.br', 
    "password": 'Omni@2022!', 
    "system": "sigmec"
    }
TOKEN_HEADERS = {"Content-Type": "application/json"}

#Define mes e ano seguinte e do mês seguinte da forma que fica escrito no Sigmec
data_atual = datetime.now()
mes_atual = str(data_atual.month).zfill(2)
ano = data_atual.year
mes_ano_atual = mes_atual + '/' + str(ano)
if mes_atual == '12':
    ano = data_atual.year + 1
    mes_seguinte = '01'
    mes_ano_seguinte = '01' + '/' + str(ano)
else:
    mes_seguinte = str(data_atual.month +1).zfill(2)
    mes_ano_seguinte = mes_seguinte  + '/' + str(ano)


def Gera_Token():
    
    token_content = requests.post(
        url = TOKEN_URL,
        json = CONTENT,
        headers=TOKEN_HEADERS
    )
    token_cleaning = json.loads(token_content.content.decode("utf-8"))
    token_cleaning = ast.literal_eval(token_cleaning["data"]["token"])
    token = token_cleaning['access_token']
    return token

token = Gera_Token()
headers = {"Authorization": f"Bearer {token}"}

def Cria_Lista_De_Pesquisa():
    # Acessa a API do Sigmec para pegar todos os parâmetros de pesquisa
    token = Gera_Token()
    print('Acessando API do Sigmec...')
    print("Token Sigmec gerado com sucesso...")
    headers = {"Authorization": f"Bearer {token}"}
    dados = requests.get(url = ESCALA_URL, headers = headers )
    lista_pesquisa = json.loads(dados.content)
    lista_pesquisa = lista_pesquisa['data']['schedule_grades_list']
    #Cria duas listas de dicionários, uma com as pesquisas do mês atual e a outra com o mês seguinte
    lista_mes_atual = []
    lista_mes_seguinte = []
    listas = []
    # Gera uma lista de pesquisa do mês atual e uma do mês seguinte
    for i in range(len(lista_pesquisa)):
        value = lista_pesquisa[i]['value']
        label = lista_pesquisa[i]['label']
        if label.startswith(mes_ano_atual):
            lista_mes_atual.append({'value': value, 'label': label})
        elif label.startswith(mes_ano_seguinte):
            lista_mes_seguinte.append({'value': value, 'label': label})
    listas.append(lista_mes_atual)
    listas.append(lista_mes_seguinte)
    return listas

def Extrai_Mes_atual():
    lista_mes_atual = Cria_Lista_De_Pesquisa()[0]
    df_geral_mes_atual = pd.DataFrame()
    # Acessa a API do Sigmec, da um request.post para todos itens da lista de mês atual, para que sejam
    # gerados todos df parciais, e então todos são unidos em um só df referente ao mês atual
    print('Extraindo escalas do mês atual....')
    for k in range(len(lista_mes_atual)):
        value = lista_mes_atual[k]['value']
        dados_mes_atual = requests.post(url = ESCALA_URL_PESQUISA, headers = headers, data = {'schedule_grade_id': value} )
        dados_mes_atual = json.loads(dados_mes_atual.content.decode('utf-8'))
        df_mes_atual = pd.DataFrame(dados_mes_atual['data']['schedule_grade_group_staffs'])

        # Identifica qual é a base, cria uma coluna com o nome da base em cada linha
        base = lista_mes_atual[k]['label'].split('/')[1]
        base = base.split('-')[1]
        df_mes_atual['Plataforma'] = base

        # Cria a coluna mês
        df_mes_atual['Mês'] = data_atual.month

        # Coloca a coluna mês e a coluna base no início
        colunas = df_mes_atual.columns.tolist()
        colunas = ['Mês'] + ['Plataforma'] + colunas [:-2]
        df_mes_atual = df_mes_atual[colunas]
        df_mes_atual = df_mes_atual.iloc[1: ]
        df_geral_mes_atual = pd.concat([df_geral_mes_atual,df_mes_atual], ignore_index=True)
    return df_geral_mes_atual

def Extrai_Mes_seguinte():
    lista_mes_seguinte = Cria_Lista_De_Pesquisa()[1]
    df_geral_mes_seguinte = pd.DataFrame()
    # Acessa a API do Sigmec, da um request.post para todos itens da lista de mês seguinte, para que sejam
    # gerados todos df parciais, e então todos são unidos em um só df referente ao mês seguinte
    print('Extraindo escalas do mês seguinte....')
    for k in range(len(lista_mes_seguinte)):
        value = lista_mes_seguinte[k]['value']
        dados_mes_seguinte = requests.post(url = ESCALA_URL_PESQUISA, headers = headers, data = {'schedule_grade_id': value} )
        dados_mes_seguinte = json.loads(dados_mes_seguinte.content.decode('utf-8'))
        df_mes_seguinte = pd.DataFrame(dados_mes_seguinte['data']['schedule_grade_group_staffs'])

        # Identifica qual é a base, cria uma coluna com o nome da base em cada linha
        base = lista_mes_seguinte[4]['label'].split('/')[1]
        base = base.split('-')[1]
        df_mes_seguinte['Plataforma'] = base

        # Cria a coluna mês
        df_mes_seguinte['Mês'] = mes_seguinte

        # Coloca a coluna mês e a coluna base no início
        colunas = df_mes_seguinte.columns.tolist()
        colunas = ['Mês'] + ['Plataforma'] + colunas [:-2]
        df_mes_seguinte = df_mes_seguinte[colunas]
        df_mes_seguinte = df_mes_seguinte.iloc[1: ]
        df_geral_mes_seguinte = pd.concat([df_geral_mes_seguinte,df_mes_seguinte], ignore_index=True)
    return df_geral_mes_seguinte

