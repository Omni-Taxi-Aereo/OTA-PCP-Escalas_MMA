# OTA-PCP-Escalas_MMA

1- O script master acessa o sistema Sitrip e Sigmec via API e extrai os seguites dados:
  Sigmec -> Informações da mão de obra e suas escalas de presença e férias do mês atual e seguinte
  Sigtrip -> Localização de cada aeronáve e suas disponibilidades

2 - Trata os dados com foco em montar um Dashboard em BI:
  Padronização de nome de bases (com base no Sigmec)
  Padronização de modelos de aeronaves (Com base no Sigtrip)
  Identifica Trocas de entrada e de saída de mão de obra
  Padroniza Turnos
  Padroniza Quinzenas
  Garante que sempre tenham 31 colunas de dias (para fevereiro e meses com 30 dias)

3 - Atualiza os dados em google sheet para que de lá sejam importados pelo Power BI e alimentem o dashboard
