import Extrai_Sigmec
from Extrai_Sigtrip import Extrai_Sigtrip
import send_to_blob
import send_to_googlesheet
import datetime
import Send_email

try:
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

    send_to_googlesheet.LimpaIntervalo('Sigtrip!A1:Z100') #Limpa aba Sigtrip
    send_to_googlesheet.EscreveValores('Sigtrip!A2', sig_trip_cabecalho)
    send_to_googlesheet.EscreveValores('Sigtrip!A3', sig_trip_valores)

    # -------------------------------------------------------------------------------------------------------------
    # Upa mes atual
    mes_atual_cabecalho = mes_atual.columns.tolist()

    cabecalho_corrigidos_atual = []
    # retira mês e ano do cabeçalho, para que o BI não crash quando mudar o mês
    for i in range(len(mes_atual_cabecalho)):
        if mes_atual_cabecalho[i-1] == 'PT6B-37A': # renomeia a coluna referente ao mês passado
            cabecalho_corrigidos_atual.append('mês ant.')
        else:
            mes_atual_cabecalho[i] = mes_atual_cabecalho[i].split('/')[0]
            cabecalho_corrigidos_atual.append (mes_atual_cabecalho[i])

    mes_atual_valores = mes_atual.values.tolist()

    # Envia para o google sheet
    send_to_googlesheet.LimpaIntervalo('Sigmec_mes_atual!A1:BA700')
    send_to_googlesheet.EscreveValores('Sigmec_mes_atual!A2', [cabecalho_corrigidos_atual])
    send_to_googlesheet.EscreveValores('Sigmec_mes_atual!A3', mes_atual_valores)

    # -------------------------------------------------------------------------------------------------------------
    # Upa data e hora da atualização na aba Data_atualização
    send_to_googlesheet.EscreveValores('Data_atualização!A1', [[data_formatada]])

    #--------------------------------------------------------------------------------------------------------------
    #Upa mes seguinte
    mes_seguinte_cabecalho = mes_seguinte.columns.tolist()

    cabecalho_corrigidos_seguinte = []
    # retira mês e ano do cabeçalho, para que o BI não crash quando mudar o mês
    for i in range(len(mes_seguinte_cabecalho)):
        if mes_seguinte_cabecalho[i-1] == 'PT6B-37A': # renomeia a coluna referente ao mês passado
            cabecalho_corrigidos_seguinte.append('mês ant.')
        else:
            mes_seguinte_cabecalho[i] = mes_seguinte_cabecalho[i].split('/')[0]
            cabecalho_corrigidos_seguinte.append (mes_seguinte_cabecalho[i])

    mes_seguinte_valores = mes_seguinte.values.tolist()
    # Envia para o google sheet
    send_to_googlesheet.LimpaIntervalo('Sigmec_mes_seguinte!A1:BA700')
    send_to_googlesheet.EscreveValores('Sigmec_mes_seguinte!A2', [cabecalho_corrigidos_seguinte])
    send_to_googlesheet.EscreveValores('Sigmec_mes_atual!A3', mes_seguinte_valores)


    print('Execução finalizada')
    Send_email.send_email_assunto('ETL de Escalas MMA realizada com sucesso', 'Só alegria')
except Exception as e:
    print('Erro no script master')
    Send_email.send_email('Erro no script master')