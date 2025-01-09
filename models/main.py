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

# Fechando conexão com banco
conn = close_database(conn)