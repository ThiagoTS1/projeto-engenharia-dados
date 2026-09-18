import os
import yfinance as yf
import pandas as pd
from datetime import datetime
from google.cloud import bigquery
from google.oauth2 import service_account

#Autenticação no Google BigQuery via Chave JSON
CAMINHO_CHAVE = "chave_gcp.json"

if not os.path.exists(CAMINHO_CHAVE):
    raise FileNotFoundError(f"Arquivo de chave '{CAMINHO_CHAVE}' não encontrado na pasta do projeto!")

credentials = service_account.Credentials.from_service_account_file(CAMINHO_CHAVE)

#Configurações do BigQuery
PROJECT_ID = "engenharia-dados-portfolio"
DATASET_ID = "raw_data"
TABELA_NOME = "cotacoes_acoes_raw"
ID_TABELA_COMPLETO = f"{PROJECT_ID}.{DATASET_ID}.{TABELA_NOME}"

client = bigquery.Client(credentials=credentials, project=PROJECT_ID)

#Extração dos dados com yfinance
TICKER = "PETR4.SA"
print(f"1. Buscando dados atualizados para {TICKER}...")

dados = yf.download(TICKER, period="5d", interval="1d")
dados = dados.reset_index()

#Garantindo que os nomes das colunas fiquem simples e sem espaços para o BigQuery
if isinstance(dados.columns, pd.MultiIndex):
    dados.columns = [col[0] for col in dados.columns]

#Adiciona uma coluna de metadado informando quando o dado foi ingerido
dados["data_ingestao"] = datetime.now()

#Salvar arquivo Parquet localmente (Data Lake Local)
nome_arquivo_local = f"dados_{TICKER.replace('.', '_')}_{datetime.now().strftime('%Y%m%d')}.parquet"
dados.to_parquet(nome_arquivo_local)
print(f"2. Arquivo bruto salvo localmente: {nome_arquivo_local}")

#Carga dos dados no BigQuery (Carregamento / Load)
print(f"3. Enviando dados para a tabela {ID_TABELA_COMPLETO} no BigQuery...")

job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.PARQUET,
    # WRITE_TRUNCATE sobrescreve a tabela inteira na carga. 
    # Para apenas anexar novos registros sem apagar os antigos, usa-se WRITE_APPEND.
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
)

with open(nome_arquivo_local, "rb") as source_file:
    job = client.load_table_from_file(source_file, ID_TABELA_COMPLETO, job_config=job_config)

job.result()  # Aguarda a conclusão da carga no BigQuery

print("SUCESSO! Dados carregados com sucesso no Google BigQuery!")