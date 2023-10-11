import requests, ast
from datetime import datetime, timedelta
import json
import pprint
import pandas as pd

TOKEN_URL = 'https://api.sigtrip.com.br/api/get/token'
ESCALA_URL = 'https://api.sigtrip.com.br/api/escalas/programacao/23/09/2023'
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
        return valor


def Extrai_Sigtrip():
    print('Extraindo dados do Sigtrip...')
    
    token_cleaning = json.loads(token_content.content.decode("utf-8"))
    token_cleaning = ast.literal_eval(token_cleaning["data"]["token"])
    print("Token Sigtrip gerado com sucesso.")
    token = token_cleaning['access_token']

    headers = {"Authorization": f"Bearer {token}"}
    dados = requests.get(url = ESCALA_URL, headers = headers)
    dados = json.loads(dados.content.decode('utf-8'))
    df_sigtrip = pd.DataFrame(dados['data']['index_data'])
    df_sigtrip['base'] = df_sigtrip['base'].apply(Padroniza_bases)
    return df_sigtrip