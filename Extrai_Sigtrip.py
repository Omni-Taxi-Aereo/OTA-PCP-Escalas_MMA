import requests, ast
from datetime import datetime, timedelta
import json
import pprint
import pandas as pd
import Send_email
import datetime

agora = datetime.datetime.now()
data_formatada = agora.strftime("%d/%m/%Y")

TOKEN_URL = 'https://api.sigtrip.com.br/api/get/token'
ESCALA_URL = 'https://api.sigtrip.com.br/api/escalas/programacao/' + str(data_formatada)
CONTENT = {
    "username": 'srv_api_indicadores@omnibrasil.com.br', 
    "password": 'Omni@2022!', 
    "system": "sigtrip"
    }
TOKEN_HEADERS = {"Content-Type": "application/json"}

token_content = requests.post(
    url = TOKEN_URL,
    json = CONTENT,
    headers=TOKEN_HEADERS
)
#dic para padronizar nome de bases com o Sigmec, formato: {'Nome no Sigmec' : 'Nome no Sigtrip'}
bases = {'Porto Urucu': 'Porto Urucu', 'Tomé': 'Tomé', 'Campos dos Goytacazes': 'Campos', 'Maricá': 'Maricá', 'Vitória': 'Vitória',
 'Jacarepaguá': 'Jacarepaguá', 'Cabo Frio': 'Cabo Frio', 'Aeroporto Internacional Eugene F. Correia': 'Guyana', 'Macaé': 'Macaé',
  'Galeão': 'Galeao', 'São Paulo': 'São Paulo', 'Navegantes': 'Navegantes', 'Cubatão': 'Cubatão'}

# Padroniza as o nome das plataformas, usando como base dados do Sigmec
def Padroniza_bases(valor):
    if valor in bases:
        return bases[valor]
    else:
        corpo = 'Parece que algum nome de aeronave no sigtrip foi modificado ou adicionado e não está na lista  de aeronaves do script Extrai_Sigtrip' + str(valor)
        Send_email.send_email(corpo)
        print(corpo)
        raise IndexError

def Padroniza_disponibilidade (elem):
    if elem == 1:
        return 'Disponível'
    else:
        return 'Indisponível'


def Extrai_Sigtrip():
    print('Extraindo dados do Sigtrip...')
    try:
        token_cleaning = json.loads(token_content.content.decode("utf-8"))
        token_cleaning = ast.literal_eval(token_cleaning["data"]["token"])
        print("Token Sigtrip gerado com sucesso.")
    except Exception as e:
        print('Erro ao gerar o Token da APi Sigtrip')
        Send_email.send_email ('Erro ao gerar o Token da APi Sigtrip')
        raise e
    try:
        token = token_cleaning['access_token']
        headers = {"Authorization": f"Bearer {token}"}
        dados = requests.get(url = ESCALA_URL, headers = headers)
        dados = json.loads(dados.content.decode('utf-8'))
        df_sigtrip = pd.DataFrame(dados['data']['index_data'])
        #Padroniza bases comparando com as do sigmec
        df_sigtrip['base'] = df_sigtrip['base'].apply(Padroniza_bases)
        #Padroniza disponibilidade
        df_sigtrip['availability'] = df_sigtrip['availability'].apply(Padroniza_disponibilidade)
        return df_sigtrip
    except Exception as e:
        print('Erro ao Extrair dados do Sigtrip')
        Send_email.send_email('Erro ao Extrair dados do Sigtrip')
        raise e
