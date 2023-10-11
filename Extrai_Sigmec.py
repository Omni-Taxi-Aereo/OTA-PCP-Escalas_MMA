import send_to_blob
import requests, ast
from datetime import datetime, timedelta
import json
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

# quinzenas como são escritas no Sigmec, essas listas são utilizadas para padronização desses valores
quinzenas1 = ['Inspectors and leaders - 1st fortnight', 'Inspetores e Líderes - 1ª Quinzena', 'Mecânicos - 1ª Quinzena', 
 'Mechanics - 1st fortnight']
quinzenas2 =['Inspectors and leaders - 2st fortnight' , 'Inspetores e Líderes - 2ª Quinzena', 'Mecânicos - 2ª Quinzena',
             'Mechanics - 2st fortnight']
quinzenas_urucu = ['Equipe - 1ª Turma', 'Equipe - 2ª Turma']
quinzena_com = ['comercial']

#Turnos como são escritos no Sigmec, essas listas são utilizadas para padronização desses valores
diurno = [ 'Grupo1', 'Grupo2', 'Grupo3 ADM', 'Grupo Especial 1', 'Grupo1 ADM', 'Grupo Especial 2',
          'Grupo Especial 3', 'Grupo Especial 4', 'Grupo2 ADM', 'Group1', 'Group2']
noturno = ['Grupo3', 'Grupo4', 'Group3', 'Group4']
jpa2 = [ 'Hangar - Heavy Mnt (D)', 'Oficina - Laboratório de Aviônica (D)', 'Oficina de Salvatagem (D)',
        'Oficina de Capotaria - Comercial Diurno', 'Oficina de Salvatagem - Comercial Diurno', 'Hangar - Heavy Mnt (N)',
        'Oficina - Laboratório de Aviônica (N)', 'Oficina de Blades', 'Oficina de Solda / Rodas (C)', 'Oficina de Pintura (C)',
        'Oficina de NDT', 'Oficina de Hidrostática', 'Oficina de Fuel Nozzles', 'Oficina de Salvatagem', 
        'Oficina Manutenção R22 (C) Diurno', 'Oficina de NDT (D)', 'Oficina Manutenção R22 (D)',
        'Oficina de Pintura (D)', 'Oficina Manutenção R22 (C) Noturno']

# Padroniza nomes de aeronaves no formato: {'Nome no Sigmec': 'Nome no Sigtrip'}
aeronaves = {'AW139': 'AW-139', 'EC155 B1': 'H-155', 'EC225 LP': 'EC-225','S76-A': 'S76', 'S76-C+': 'S76', 'S76-C++': 'S76'}

# Colunas que são excluídas
colunas_para_excluir = ['staff_id', 'role_id', 'inscription', 'canac', 'date_of_birth', 'cel', 'gmp',
                        'avi', 'aircraft_models', 'aircraft_model_subtypes', 'dates', 'city']

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

# Padroniza a troca de saída (TS) e de entrada (X)
def substituir_T(row):
    for i, valor in enumerate(row):
        if valor == "T":
            if i <= len(row) -1 and row[i - 1] == "X":
                row[i] = "TS"
            elif i <= len(row) -1  and row[i - 1] == "":
                row[i] = "X"
    return row

def Arruma_bases(valor):
    valor = valor.strip()
    return valor

# Padroniza a coluna de turno do Sigmec
def Define_Turno (valor):
    if valor in diurno:
        return 'Diurno'
    elif valor in noturno:
        return 'Noturno'
    elif valor in jpa2:
        return 'JPA2'
    else:
        return valor
    
#Padroniza os nomes das aeronaves
def Padroniza_aeronaves(df):
    for coluna in df.columns:
        if coluna in aeronaves:
            novo_cabecalho = aeronaves[coluna]
            df.rename(columns={coluna: novo_cabecalho}, inplace=True)

def Define_Quinzena(valor):
    # Padriniza a forma como é escrito a quinzena
    if valor in quinzenas1:
        return '1ª Quinzena'
    elif valor in quinzenas2:
        return  '2ª Quinzena'
    elif valor == quinzenas_urucu[0]:
        return  'Urucu 1'
    elif valor == quinzenas_urucu[1]:
        return  'Urucu 2'
    elif valor in quinzena_com:
        return  'Comercial'
    elif valor == None:
        return 'Férias'

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
        df_mes_atual = df_mes_atual.iloc[0: ]
        df_geral_mes_atual = pd.concat([df_geral_mes_atual,df_mes_atual], ignore_index=True)
    print('Manipulando dados da planilha do mês atual...')
    #Padroniza as quinzenas
    df_geral_mes_atual['period'] = df_geral_mes_atual['period'].apply(Define_Quinzena)
    # Padroniza os turnos
    df_geral_mes_atual['group_name'] = df_geral_mes_atual['group_name'].apply(Define_Turno)
    #Padroniza nomes de aeronaves
    Padroniza_aeronaves(df_geral_mes_atual)
    #Exclui colunas desnecessárias
    df_geral_mes_atual.drop(columns=colunas_para_excluir, inplace=True)
    #Identifica T de entrada, muda para X e T de saída para TS
    df_geral_mes_atual = df_geral_mes_atual.apply(substituir_T, axis=1)
    #Retira espaços em branco no inicio de cada base
    df_geral_mes_atual ['Plataforma'] = df_geral_mes_atual['Plataforma'].apply(Arruma_bases)
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
        base = lista_mes_seguinte[k]['label'].split('/')[1]
        base = base.split('-')[1]
        df_mes_seguinte['Plataforma'] = base

        # Cria a coluna mês
        df_mes_seguinte['Mês'] = mes_seguinte

        # Coloca a coluna mês e a coluna base no início
        colunas = df_mes_seguinte.columns.tolist()
        colunas = ['Mês'] + ['Plataforma'] + colunas [:-2]
        df_mes_seguinte = df_mes_seguinte[colunas]
        df_mes_seguinte = df_mes_seguinte.iloc[0: ]

        #Junta a planilha parcial, com info da base, na planilha geral de todas as bases
        df_geral_mes_seguinte = pd.concat([df_geral_mes_seguinte,df_mes_seguinte], ignore_index=True)
    print('Manipulando dados da planilha do mês seguinte...')
    try:
        #Identifica T de entrada, muda para X e T de saída para TS
        df_geral_mes_seguinte = df_geral_mes_seguinte.apply(substituir_T, axis=1)
        #Padroniza as quinzenas
        df_geral_mes_seguinte['period'] = df_geral_mes_seguinte['period'].apply(Define_Quinzena)
        #Padroniza Turnos
        df_geral_mes_seguinte['group_name'] = df_geral_mes_seguinte['group_name'].apply(Define_Turno)
        #Padroniza nomes de aeronaves
        Padroniza_aeronaves(df_geral_mes_seguinte)
        #Exclui colunas desnecessárias
        df_geral_mes_seguinte.drop(columns=colunas_para_excluir, inplace=True)
        #Retira espaços em branco no inicio de cada base
        df_geral_mes_seguinte['Plataforma'] = df_geral_mes_seguinte['Plataforma'].apply(Arruma_bases)
    except KeyError:
        print('Não existem dados de escala para o mês seguinte')
    return df_geral_mes_seguinte
#


