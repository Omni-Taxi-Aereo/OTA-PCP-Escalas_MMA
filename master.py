import Extrai_Sigmec
from Extrai_Sigtrip import Extrai_Sigtrip
import send_to_blob
import pandas

mes_atual = Extrai_Sigmec.Extrai_Mes_atual()
mes_seguinte = Extrai_Sigmec.Extrai_Mes_seguinte()
sig_trip = Extrai_Sigtrip()

print('Exportando dados para o banco de dados...')
send_to_blob.export_dataframe_to_blob(mes_atual, 'escalas-mma', 'Entrada/Processar/CSV/Sigmec_mes_atual.csv')
send_to_blob.export_dataframe_to_blob(mes_seguinte, 'escalas-mma', 'Entrada/Processar/CSV/Sigmec_mes_seguinte.csv')
send_to_blob.export_dataframe_to_blob(sig_trip, 'escalas-mma', 'Entrada/Processar/CSV/Sigtrip.csv')

print('Execução finalizada')
