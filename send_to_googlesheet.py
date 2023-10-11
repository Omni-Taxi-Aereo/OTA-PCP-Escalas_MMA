from __future__ import print_function

import os.path
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
sheetId = '1nHGybLOw55ppI3_j7lIH85R5QmaCstNROe8duF-svVw'

def Autentica():
    # Credenciais começam vazias
    creds = None
    # Verifica se existe token.json
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # Verifica se as credenciais não existem ou não são válidas
    if not creds or not creds.valid:
        # Verifica se existe o refresh_token, caso exista, significa que já foi efetuada a conexão em outro momento
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Acessa a credencial, abre o navegador para que seja autorizado o login
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Salva token para uso futuro
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # V4 é a versão do google sheet atual
    service = build('sheets', 'v4', credentials=creds)
    # Chama a API
    sheet = service.spreadsheets()
    return sheet

# Deve ser utilizada no seguinte formado: LerValores('Sigtrip!A1:B6')
def LerValores (intervalo):
    sheet = Autentica()
    valores = sheet.values().get(spreadsheetId = sheetId, range= intervalo).execute()
    linhas = valores.get('values')
    return linhas


def EscreveValores(intervalo,valores):
        sheet = Autentica()
        valores = sheet.values().update(spreadsheetId=sheetId, range = intervalo, valueInputOption='USER_ENTERED', body ={'values': valores}).execute()


# data = {'Coluna_1': [1, 2, 3],
#         'Coluna_2': [4, 5, 6]}

# data = pd.DataFrame(data)

# data = data.values.tolist()
# EscreveValores('Sigtrip!A2', data)
