import Extrai_Sigmec
from Extrai_Sigtrip import Extrai_Sigtrip
import send_to_blob
import pandas
import send_to_googlesheet

mes_atual = Extrai_Sigmec.Extrai_Mes_atual()
mes_seguinte = Extrai_Sigmec.Extrai_Mes_seguinte()
sig_trip = Extrai_Sigtrip()

# Como é necessário que o Daniel Fumian edite algumas informações depois que os dados são extraídos
# Os Dataframes serão armazenados em google sheet até que o projeto Sigmec 4.0 seja finalizado e
# os dados extraidos via API não tenham mais a necessidade de serem manipulados pelo Daniel

# print('Exportando dados para o banco de dados...')
# send_to_blob.export_dataframe_to_blob(mes_atual, 'escalas-mma', 'Entrada/Excel/Sigmec_mes_atual.xlsx')
# send_to_blob.export_dataframe_to_blob(mes_seguinte, 'escalas-mma', 'Entrada/Excel/Sigmec_mes_seguinte.xlsx')
# send_to_blob.export_dataframe_to_blob(sig_trip, 'escalas-mma', 'Entrada/Excel/Sigtrip.xlsx')

sig_trip_cabecalho = [sig_trip.columns.tolist()]
sig_trip_valores = sig_trip.values.tolist()
send_to_googlesheet.EscreveValores('Sigtrip!A2', sig_trip_cabecalho)
send_to_googlesheet.EscreveValores('Sigtrip!A3', sig_trip_valores)

mes_atual_cabecalho = [mes_atual.columns.tolist()]
mes_atual_valores = mes_atual.values.tolist()
send_to_googlesheet.EscreveValores('Sigmec_mes_atual!A2', mes_atual_cabecalho)
send_to_googlesheet.EscreveValores('Sigmec_mes_atual!A3', mes_atual_valores)


mes_seguinte_cabecalho = [mes_seguinte.columns.tolist()]
mes_seguinte_valores = mes_seguinte.values.tolist()
send_to_googlesheet.EscreveValores('Sigmec_mes_seguinte!A2', mes_seguinte_cabecalho)
send_to_googlesheet.EscreveValores('Sigmec_mes_atual!A3', mes_seguinte_valores)


print('Execução finalizada')
