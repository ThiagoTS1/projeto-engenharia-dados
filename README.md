# 📈 Pipeline End-to-End de Dados Financeiros (ELT)

Pipeline moderno de Engenharia de Dados desenvolvido para extração automatizada, carga em Data Warehouse e transformação de dados de mercado financeiro em tempo real.

---

## 🏗️ Arquitetura da Solução

```text
[ API yfinance ] 
       │
       ▼ (Python - pandas / parquet)
[ Google BigQuery: raw_data.cotacoes_acoes_raw ]
       │
       ▼ (dbt Core - Staging Layer)
[ Google BigQuery: analytics.stg_cotacoes ]
       │
       ▼ (dbt Core - Marts Layer)
[ Google BigQuery: analytics.fct_cotacoes_diarias ]
```

1. **Ingestão (Python):** Extração de dados via API `yfinance`, estruturação colunar com `pandas`, serialização em formato `.parquet` e carga em lote no **Google BigQuery** (Dataset: `raw_data`).
2. **Data Warehouse (GCP BigQuery):** Armazenamento em nuvem estruturado em arquitetura de camadas (`raw_data` e `analytics`).
3. **Transformação & Governança (dbt Core):** 
   - **Staging Layer (`stg_cotacoes`):** Limpeza de registros nulos, padronização de tipos de dados (`SAFE_CAST`) e saneamento das colunas da camada bruta.
   - **Marts Layer (`fct_cotacoes_diarias`):** Modelagem dimensional de negócio com cálculo de métricas financeiras (variação percentual diária do preço).
   - **Data Quality:** Testes automatizados de integridade de dados (`not_null`).
   - **Linhagem (DAG):** Documentação técnica interativa e rastreabilidade total do fluxo de dados.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.12
- **Data Warehouse:** Google Cloud BigQuery
- **Transformação & Testes:** dbt Core (v1.12)
- **Segurança & Acessos:** GCP IAM & Service Account (`sa-pipeline-dados`)
- **Formato de Armazenamento:** Apache Parquet

---

## 📊 Linhagem dos Dados (DAG)

O fluxo de dependência entre as camadas do pipeline é gerenciado nativamente pelo dbt Core:

`raw_data.cotacoes_acoes_raw` ➔ `analytics.stg_cotacoes` ➔ `analytics.fct_cotacoes_diarias`

---

## 📂 Estrutura do Repositório

```text
projeto-engenharia-dados/
├── dbt_analytics/              # Projeto dbt Core
│   ├── models/
│   │   ├── staging/           # Modelos de limpeza e padronização (Views)
│   │   │   ├── stg_cotacoes.sql
│   │   │   └── schema.yml
│   │   ├── marts/             # Modelos de negócio/fatos (Tables)
│   │   │   └── fct_cotacoes_diarias.sql
│   │   └── sources.yml        # Mapeamento de fontes brutas do BigQuery
│   ├── dbt_project.yml        # Configurações do projeto dbt
│   └── profiles.yml           # Configuração de conexões com BigQuery
├── extract.py                 # Script Python de ingestão de dados
├── README.md                  # Documentação do projeto
└── .gitignore                 # Arquivos ignorados pelo Git (chaves e venv)
```

---

## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos
- Python 3.10+
- Conta ativa no Google Cloud Platform (GCP) com um projeto configurado
- Chave de Conta de Serviço (`JSON`) com permissões de leitura/escrita no BigQuery

### Passos de Execução

1. **Clonar o repositório:**
   ```bash
   git clone https://github.com/SEU_USUARIO/projeto-engenharia-dados.git
   cd projeto-engenharia-dados
   ```

2. **Criar e ativar o ambiente virtual:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1  # Windows PowerShell
   ```

3. **Instalar as dependências:**
   ```bash
   pip install pandas yfinance google-cloud-bigquery dbt-bigquery
   ```

4. **Executar a ingestão de dados em Python:**
   ```bash
   python extract.py
   ```

5. **Executar as transformações e testes no dbt:**
   ```bash
   cd dbt_analytics
   dbt run
   dbt test
   ```

6. **Visualizar a documentação e o gráfico de linhagem (DAG):**
   ```bash
   dbt docs generate
   dbt docs serve
   ```