from data_tests import run_tests
from functions import connect_database,close_database
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

conn = connect_database(r'..\database\dabase.db')

# Carregar os dados da planilha
file_path = r'..\src\Planilha_case_dados.xlsx'
data_plan1 = pd.read_excel(file_path, sheet_name='Plan1')
data_plan3 = pd.read_excel(file_path, sheet_name='Plan3')

# Capturando UFs
data_plan1['uf'] = data_plan1['UF - LOJA'].str.split('-').str[0].str.strip() + ' - Brasil'
data_plan1['regiao'] = data_plan1['UF - LOJA'].str.split('(').str[0].str.strip() + ' - Brasil'

data_plan1['UF - LOJA'] =  data_plan1['UF - LOJA'].str.split('(').str[1].str.replace(')','').str.strip()

data_plan3['uf'] =  'Indefinido'
data_plan3['regiao'] =  'Indefinido'

data_plan3.columns = data_plan1.columns
data_concatenated = pd.concat([data_plan1,data_plan3])

# Verificar e renomear colunas para padronização (caso necessário)
data_concatenated.columns = [col.strip().lower().replace(' ', '_') for col in data_concatenated.columns]

data_plan1.to_sql('raw_case_data_plan1', conn, if_exists='replace', index=False)
data_plan3.to_sql('raw_case_data_plan3', conn, if_exists='replace', index=False)

data_concatenated.to_sql('trusted_case_data', conn, if_exists='replace', index=False)
data_concatenated.to_excel(r'..\data_results\trusted\case_data.xlsx',sheet_name='case_data',index=False)

# Realizando teste de qualidade
run_tests(r'..\ge',data_concatenated)

# # data_concatenated = read_table_sqlite(conn,'trusted_case_data')

# # Remover entradas com valores inválidos (0 em valor total ou pesagem total)
# data_concatenated = data_concatenated[(data_concatenated['valor_total_geral_(r$)'] > 0) & (data_concatenated['pesagem_real_total_(kg)'] > 0)]

# # Cálculo da eficiência por fornecedor (custo por kg descartado)
# data_concatenated['custo_por_kg'] = data_concatenated['valor_total_geral_(r$)'] / data_concatenated['pesagem_real_total_(kg)']


# # ========================= Agrupar por fornecedor para calcular a média de custo por kg, peso total e eficiência =========================
# fornecedor_efficiency = data_concatenated.groupby('fornecedor').agg(
#     peso_total=('pesagem_real_total_(kg)', 'sum'),
#     valor_total=('valor_total_geral_(r$)', 'sum'),
#     custo_medio_por_kg=('custo_por_kg', 'mean'),
#     num_transacoes=('fornecedor', 'count')
# ).reset_index()

# # Calcular a métrica de eficiência geral (custo médio ponderado pelo peso total)
# fornecedor_efficiency['eficiencia_geral'] = fornecedor_efficiency['valor_total'] / fornecedor_efficiency['peso_total']

# # Ordenar pela eficiência (menor custo médio por kg e menor eficiência geral)
# fornecedor_efficiency = fornecedor_efficiency.sort_values(by=['eficiencia_geral', 'custo_medio_por_kg'])

# # Adicionar um ranking de eficiência
# fornecedor_efficiency['ranking'] = fornecedor_efficiency['custo_medio_por_kg'].rank(method='min')

# # Ordenar o DataFrame pelo ranking
# fornecedor_efficiency = fornecedor_efficiency.sort_values(by='ranking')

# # Salvando no banco de dados
# fornecedor_efficiency.to_sql('conformed_eficiencia_fornecedor', conn, if_exists='replace', index=False)
# fornecedor_efficiency.to_excel(r'..\data_results\conformed\eficiencia_fornecedor.xlsx',sheet_name='eficiencia_fornecedor',index=False)

# # ========================= Ranking de lojas por custo por kg =========================
# loja_ranking = data_concatenated.groupby('uf_-_loja').agg(
#     peso_total=('pesagem_real_total_(kg)', 'sum'),
#     valor_total=('valor_total_geral_(r$)', 'sum'),
#     custo_medio_por_kg=('custo_por_kg', 'mean')
# ).reset_index()

# # Ordenar por maior custo médio por kg
# loja_ranking = loja_ranking.sort_values(by='custo_medio_por_kg', ascending=False)

# # Salvando no banco de dados
# loja_ranking.to_sql('conformed_ranking_loja', conn, if_exists='replace', index=False)
# loja_ranking.to_excel(r'..\data_results\conformed\ranking_loja.xlsx',sheet_name='ranking_loja',index=False)

# Fechando conexão com banco
conn = close_database(conn)