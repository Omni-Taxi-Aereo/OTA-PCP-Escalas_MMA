# import send_to_blob
import requests, ast
from datetime import datetime
import json
import pandas as pd
import Send_email
import os
from send_to_googlesheet import LerValores
import sys



TOKEN_URL = 'https://api.sigmec.com.br/api/get/token'
ESCALA_URL = 'https://api.sigmec.com.br/api/escala/grade/vencimentos'
ESCALA_URL_PESQUISA = 'https://api.sigmec.com.br/api/escala/grade/vencimentos/pesquisa'
USERNAME = os.environ.get('SIG_USER')
PASSWORD = os.environ.get('SIG_PASSWORD')

USERNAME = os.environ.get('SIG_USER')
PASSWORD = os.environ.get('SIG_PASSWORD')

CONTENT = {
    "username": USERNAME, 
    "password": PASSWORD, 
    "system": "sigmec"
}


TOKEN_HEADERS = {"Content-Type": "application/json"}

# quinzenas como são escritas no Sigmec, essas listas são utilizadas para padronização desses valores

L_quinzena_1 = LerValores(('Bases!F1:F100'))
quinzenas1 = []

for i in range(len(L_quinzena_1)):
    quinzenas1.append(L_quinzena_1[i][0])

print ('\n Lista de 1ª Quinzenas: ', quinzenas1)

#------------------------------------------------------

L_quinzena_2 = LerValores(('Bases!G1:G100'))
quinzenas2 = []

for i in range(len(L_quinzena_2)):
    quinzenas2.append(L_quinzena_2[i][0])

print ('\nLista de 2ª Quinzenas: ', quinzenas2)

#------------------------------------------------------

L_quinzena_urucu_1 = LerValores(('Bases!H1:H100'))
quinzenas_urucu_1 = []

for i in range(len(L_quinzena_urucu_1)):
    quinzenas_urucu_1.append(L_quinzena_urucu_1[i][0])

print ('\nLista de Quinzenas de Urucu: ', quinzenas_urucu_1)

#------------------------------------------------------

L_quinzena_urucu_2 = LerValores(('Bases!I1:I100'))
quinzenas_urucu_2 = []

for i in range(len(L_quinzena_urucu_2)):
    quinzenas_urucu_2.append(L_quinzena_urucu_2[i][0])

print ('\nLista de Quinzenas de Urucu: ', quinzenas_urucu_2)


#------------------------------------------------------
    
L_quinzena_com = LerValores(('Bases!J1:J100'))
quinzena_com = []

for i in range(len(L_quinzena_com)):
    quinzena_com.append(L_quinzena_com[i][0])

print ('\nLista de Quinzenas de Urucu: ', quinzena_com)

#------------------------------------------------------
#Turnos como são escritos no Sigmec, essas listas são utilizadas para padronização desses valores

L_diurno = LerValores(('Bases!K1:K100'))
diurno = []

for i in range(len(L_diurno)):
    diurno.append(L_diurno[i][0])

print ('\nLista de grupos de diurno: ', diurno)

#------------------------------------------------------
    
L_noturno = LerValores(('Bases!L1:L100'))
noturno = []

for i in range(len(L_noturno)):
    noturno.append(L_noturno[i][0])

print ('\nLista de grupos de noturno: ', noturno)

#------------------------------------------------------
# Padroniza nomes de aeronaves no formato: {'Nome no Sigmec': 'Nome no Sigtrip'}

C_aeronaves = LerValores(('Bases!M1:M100'))
V_aeronaves = LerValores(('Bases!N1:N100'))
aeronaves = {}

try:
    for i in range(len(C_aeronaves)):
        aeronaves[C_aeronaves[i][0]] = V_aeronaves[i][0]

    print ('\nDicionário de aeronaves no formato {segmec:sigtrip}: ', aeronaves)
except Exception as e:
    corpo = 'A lista de aeronaves Sigtrip e Sigmec não estão com o mesmo tamanho'
    print(corpo)
    Send_email.send_email(corpo)
    sys.exit()

#------------------------------------------------------


# quinzenas1 = ['Inspectors and leaders - 1st fortnight',
#               'Inspetores e Líderes - 1ª Quinzena',
#               'Mecânicos - 1ª Quinzena',
#               'Mechanics - 1st fortnight'
#               ]
# quinzenas2 =['Inspectors and leaders - 2st fortnight' ,
#              'Inspetores e Líderes - 2ª Quinzena',
#              'Mecânicos - 2ª Quinzena',
#              'Mechanics - 2st fortnight'
#              ]
# quinzenas_urucu = ['Equipe - 1ª Turma',
#                    'Equipe - 2ª Turma',
#                    '1ª Turma',
#                    '2ª Turma',
#                    '2ª Turma'
#                    ]
# quinzena_com = ['Comercial']

#Turnos como são escritos no Sigmec, essas listas são utilizadas para padronização desses valores
# diurno = [ 'Grupo1',
#           'Grupo2',
#           'Grupo3 ADM',
#           'Grupo Especial 1',
#           'Grupo1 ADM',
#           'Grupo Especial 2',
#           'Grupo Especial 3',
#           'Grupo Especial 4',
#           'Grupo2 ADM',
#           'Group1',
#           'Group2',
#           "Hangar - Heavy Mnt (D)",
#           "Oficina - Laboratório de Aviônica (D)",
#           "Oficina de Estruturas Compostas",
#           "Grupo1 ADM",
#           "Grupo2 ADM",
#           "Oficina de Salvatagem (D)",
#           "Oficina de Componentes",
#           "Manutenção de Hangar - Pintura (D)",
#           "Oficina de Capotaria - Comercial Diurno",
#           "Oficina de motores",
#           "Oficina de Exhaust",
#           "Oficina de Exhaust - Componentes",
#           "Oficina Manutenção R22 (D)",
#           "Oficina de Salvatagem - Comercial Diurno",
#           "Oficina de Solda / Rodas",
#           'Oficina de Solda / Rodas (C)',
#           "Oficina de Blades", "Oficina de Solda / Rodas(C)",
#           "Oficina de Pintura (C)",
#           "Oficina de NDT",
#           "Mnt Hangar e Pista R22",
#           "Oficina de Fuel Nozzles",
#           "Oficina de Hidrostática",
#           "Grupo Especial 1",
#           "Grupo Especial 2",
#           "Oficina de Fuel Nozzles",
#           "Oficina de Pintura (D)",
#           "Oficina de Salvatagem",
#           "Oficina Manutenção R22 (C) Diurno",
#           "Oficina de NDT (D)"
#           ]

# noturno = ['Grupo3',
#            'Grupo4',
#            'Group3',
#            'Group4',
#            "Oficina Manutenção R22 (C) Noturno",
#            "Oficina - Laboratório de Aviônica (N)",
#            "Hangar - Heavy Mnt (N)",
#            "Oficina de Salvatagem - Comercial Noturno",
#            "Oficina de Pintura (N)"
#            ]


# Padroniza nomes de aeronaves no formato: {'Nome no Sigmec': 'Nome no Sigtrip'}
# aeronaves = {'AW139': 'AW-139',
#              'EC155 B1': 'H-155',
#              'EC225 LP': 'EC-225',
#              'S76-A': 'S76',
#              'S76-C+': 'S76',
#              'S76-C++': 'S76'
#              }

# Colunas que são excluídas
colunas_para_excluir = ['staff_id', 'role_id',
                        'inscription', 'canac',
                        'date_of_birth',
                        'cel',
                        'gmp',
                        'avi',
                        'aircraft_models',
                        'aircraft_model_subtypes',
                        'dates',
                        'city'
                        ]

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
    '''Gera Token da API de acesso ao Sigmec'''
    try:
        token_content = requests.post(
            url = TOKEN_URL,
            json = CONTENT,
            headers=TOKEN_HEADERS
        )
        token_cleaning = json.loads(token_content.content.decode("utf-8"))
        token_cleaning = ast.literal_eval(token_cleaning["data"]["token"])
        token = token_cleaning['access_token']
        return token
    except Exception as e:
        Send_email.send_email('Erro ao gerar Token API Sigmec')
        print('Erro ao gerar Token API Sigmec')
        sys.exit()

token = Gera_Token()
headers = {"Authorization": f"Bearer {token}"}

Gera_Token()

def Cria_Lista_De_Pesquisa():
    # Acessa a API do Sigmec para pegar todos os parâmetros de pesquisa
    token = Gera_Token()
    print('Acessando API do Sigmec...')
    print("Token Sigmec gerado com sucesso...")
    try:
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
    except Exception as e:
        Send_email.send_email('Erro ao gerar Lista de Pesquisa Sigmec')
        print('Erro ao gerar Lista de Pesquisa Sigmec')
        sys.exit()
# Padroniza a troca de saída (TS) e de entrada (X)
def substituir_T(row):
    try:
        for i, valor in enumerate(row):
            if valor == "T":
                if i <= len(row) -1 and row[i - 1] == "X":
                    row[i] = "TS"
                elif i <= len(row) -1  and row[i - 1] == "":
                    row[i] = "X"
                elif i <= len(row) -1 and row[i - 1] == "F":
                    row[i] = "X"
        return row
    except Exception as e:
        Send_email.send_email('Erro ao substituir T nos dados do Sigmec')
        print('Erro ao substituir T nos dados do Sigmec')
        sys.exit()

def Arruma_bases(valor):
    valor = valor.strip()
    return valor

# Padroniza a coluna de turno do Sigmec
def Define_Turno (valor):
    if valor in diurno:
        return 'Diurno'
    elif valor in noturno:
        return 'Noturno'
    elif valor == 'Férias':
        return 'Férias'
    else:
        corpo = 'Parece que algum turno novo foi criado e não está na lista no Script do Sigmec. Nome do turno com problema: ' + str(valor)
        Send_email.send_email(corpo)
        print(corpo)
        sys.exit()
    
#Padroniza os nomes das aeronaves
def Padroniza_aeronaves(df):
    for coluna in df.columns:
        if coluna in aeronaves:
            novo_cabecalho = aeronaves[coluna]
            df.rename(columns={coluna: novo_cabecalho}, inplace=True)

def Padroniza_mes_ant (cols):
    new_cols = []
    for i in range(len(cols)):
        if cols[i] == '01':
            new_cols[i-1] = 'mês ant.'
            new_cols.append(cols[i])
        else:
            new_cols.append(cols[i])
    return new_cols

#Coloca uma coluna chamada '31' ao fim da planilha caso o mês não tenha 31 dias, pois o BI precisa de 31 colunas de dias
def Padroniza_dia_31 (df):
    cols = df.columns
    if '31' not in cols [35:]:
        df['31'] = ''
    return df


def Padroniza_datas(cols):
    cols_corrigidos = []
    #retira mês e ano do cabeçalho, para que o BI não crash quando mudar o mês
    for i in range(len(cols)):
        col = cols[i].split('/')[0]
        cols_corrigidos.append (col)        
    return cols_corrigidos 

def Define_Quinzena(valor):
    # Padriniza a forma como é escrito a quinzena
    if valor in quinzenas1:
        return '1ª Quinzena'
    elif valor in quinzenas2:
        return  '2ª Quinzena'
    elif valor in quinzenas_urucu_1:
        return  'Urucu 1'
    elif valor in quinzenas_urucu_2:
        return  'Urucu 2'
    elif valor in quinzena_com:
        return  'Comercial'
    elif valor == None:
        return 'Férias'
    else:
        corpo = 'Parece que alguma nomenclatura nova foi criada para quinzena e não está na lista. Nome com problema: ' + valor
        Send_email.send_email(corpo)
        sys.exit()
        

def Extrai_Mes_atual():
    lista_mes_atual = Cria_Lista_De_Pesquisa()[0]
    df_geral_mes_atual = pd.DataFrame()
    # Acessa a API do Sigmec, da um request.post para todos itens da lista de mês atual, para que sejam
    # gerados todos df parciais, e então todos são unidos em um só df referente ao mês atual
    print('Extraindo escalas do mês atual....')
    try:
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
        #Padroniza datas, retirando mês e ano
        df_geral_mes_atual.columns = Padroniza_datas(df_geral_mes_atual.columns)
        #Renomeia o dia do mês anterior para 'Mês ant."
        df_geral_mes_atual.columns = Padroniza_mes_ant(df_geral_mes_atual.columns)
        #Adiciona o dia 31 com todas linhas em branco caso ele não exista no mês em quetão, pois o BI precisa de uma coluna chamada 31
        df_geral_mes_atual = Padroniza_dia_31(df_geral_mes_atual)
        
        return df_geral_mes_atual
    except Exception as e:
        Send_email.send_email(f'Erro ao Extrair dados do mês atual do Sigmec \n ERROR: {e}')
        print('Erro ao Extrair dados do mês atual do Sigmec\n Error: ',e)
        sys.exit()


def Extrai_Mes_seguinte():
    lista_mes_seguinte = Cria_Lista_De_Pesquisa()[1]
    df_geral_mes_seguinte = pd.DataFrame()
    # Acessa a API do Sigmec, da um request.post para todos itens da lista de mês seguinte, para que sejam
    # gerados todos df parciais, e então todos são unidos em um só df referente ao mês seguinte
    print('Extraindo escalas do mês seguinte....')
    try:
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
    except Exception as e:
        Send_email.send_email(f'Erro ao Extrair dados do mês atual do Sigmec \n ERROR: {e}')
        print('Erro ao Extrair dados do mês seguinte do Sigmec')
        raise e
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
        #Padroniza datas, retirando mês e ano
        df_geral_mes_seguinte.columns = Padroniza_datas(df_geral_mes_seguinte.columns)
        #Renomeia o dia do mês anterior para 'Mês ant."
        df_geral_mes_seguinte.columns = Padroniza_mes_ant(df_geral_mes_seguinte.columns)
        #Adiciona o dia 31 com todas linhas em branco caso ele não exista no mês em quetão, pois o BI precisa de uma coluna chamada 31
        df_geral_mes_seguinte = Padroniza_dia_31(df_geral_mes_seguinte)
    except Exception as e:
        print('Não existem dados de escala para o mês seguinte')
    return df_geral_mes_seguinte
