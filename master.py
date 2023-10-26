import Extrai_Sigmec
from Extrai_Sigtrip import Extrai_Sigtrip
import send_to_blob
import send_to_googlesheet
import datetime
import Send_email


mes_atual = Extrai_Sigmec.Extrai_Mes_atual()
mes_seguinte = Extrai_Sigmec.Extrai_Mes_seguinte()
sig_trip = Extrai_Sigtrip()

agora = datetime.datetime.now()
data_formatada = agora.strftime("%d/%m/%Y %H:%M")

# Como é necessário que o Daniel Fumian edite algumas informações depois que os dados são extraídos
# Os Dataframes serão armazenados em google sheet até que o projeto Sigmec 4.0 seja finalizado e
# os dados extraidos via API não tenham mais a necessidade de serem manipulados pelo Daniel

# print('Exportando dados para o banco de dados...')
# send_to_blob.export_dataframe_to_blob(mes_atual, 'escalas-mma', 'Entrada/Excel/Sigmec_mes_atual.xlsx')
# send_to_blob.export_dataframe_to_blob(mes_seguinte, 'escalas-mma', 'Entrada/Excel/Sigmec_mes_seguinte.xlsx')
# send_to_blob.export_dataframe_to_blob(sig_trip, 'escalas-mma', 'Entrada/Excel/Sigtrip.xlsx')


# -------------------------------------------------------------------------------------------------------------
# Upa dados do Sigtrip

sig_trip_cabecalho = [sig_trip.columns.tolist()]
sig_trip_valores = sig_trip.values.tolist()

send_to_googlesheet.LimpaIntervalo('Sigtrip!A3:Z100') #Limpa aba Sigtrip
send_to_googlesheet.EscreveValores('Sigtrip!A3', sig_trip_cabecalho)
send_to_googlesheet.EscreveValores('Sigtrip!A4', sig_trip_valores)

# -------------------------------------------------------------------------------------------------------------
# Upa mes atual sigmec
mes_atual_cabecalho = mes_atual.columns.tolist()
mes_atual_valores = mes_atual.values.tolist()

# Envia para o google sheet
send_to_googlesheet.LimpaIntervalo('Sigmec_mes_atual!A1:BA700')
send_to_googlesheet.EscreveValores('Sigmec_mes_atual!A2', [mes_atual_cabecalho])
send_to_googlesheet.EscreveValores('Sigmec_mes_atual!A3', mes_atual_valores)

# -------------------------------------------------------------------------------------------------------------
# Upa data e hora da atualização na aba Data_atualização
send_to_googlesheet.EscreveValores('Data_atualização!A1', [[data_formatada]])

#--------------------------------------------------------------------------------------------------------------
#Upa mes seguinte

mes_seguinte_cabecalho = mes_seguinte.columns.tolist()
mes_seguinte_valores = mes_seguinte.values.tolist()

# Envia para o google sheet
send_to_googlesheet.LimpaIntervalo('Sigmec_mes_seguinte!A1:BA700')
send_to_googlesheet.EscreveValores('Sigmec_mes_seguinte!A2', [mes_seguinte_cabecalho])
send_to_googlesheet.EscreveValores('Sigmec_mes_seguinte!A3', mes_seguinte_valores)

#--------------------------------------------------------------------------------------------------------------

print('Execução finalizada')

#Envio de Email com alerta de atualização e instruções

assunto_PCP = 'Dados extraidos do Sigmec e Sigtrip com sucesso!  \n \
A planilha google sheet foi atualizada, agora é necessário que sejam preenchidas na aba sigtrip \
as informações de quais aeronaves estão em São Paulo e quais aeronaves estão em Jacarepaguá 2  \n \n \
\
Google Sheett: https://docs.google.com/spreadsheets/d/1nHGybLOw55ppI3_j7lIH85R5QmaCstNROe8duF-svVw/edit#gid=0 \n \n \
\
Dashboard: https://app.powerbi.com/groups/55575cfc-e998-4e8c-9e4b-416dbab85f8c/reports/38fd6815-fc09-4582-9c52-d0abf25ddcbe/ReportSectionc70709175071ccdc2342?experience=power-bi \n \n \
\
Contato de suporte: alan.chagas@omnibrasil.com.br \n \n \
\
\
Att, \n \
Equipe TI Digital'

destinatarios = ['alan.chagas@omnibrasil.com.br','daniel.fumian@omnibrasil.com.br', 'karen.ribeiro@omnibrasil.com.br' ]

Send_email.send_email_assunto_destinatarios('Dados de escala MMA atualizados com sucesso', destinatarios ,assunto_PCP)