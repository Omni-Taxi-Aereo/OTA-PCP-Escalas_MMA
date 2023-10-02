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
    return df_sigtrip