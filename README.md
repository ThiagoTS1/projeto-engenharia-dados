# 📈 Pipeline End-to-End de Dados Financeiros (ELT)

Pipeline de Engenharia de Dados desenvolvido para **ingestão automatizada, armazenamento em Data Warehouse e transformação de dados do mercado financeiro**, utilizando Python, Google BigQuery e dbt Core.

## 🏗️ Arquitetura da Solução

```text
[ Yahoo Finance / yfinance ]
            │
            ▼
[ Python + pandas ]
            │
            ▼
[ Apache Parquet ]
            │
            ▼
[ BigQuery: raw_data.cotacoes_acoes_raw ]
            │
            ▼
[ dbt Core — Staging ]
            │
            ▼
[ BigQuery: analytics.stg_cotacoes ]
            │
            ▼
[ dbt Core — Marts ]
            │
            ▼
[ BigQuery: analytics.fct_cotacoes_diarias ]
```

### Fluxo do pipeline

**1. Ingestão — Python**

Os dados de mercado são obtidos por meio da biblioteca `yfinance`, estruturados com `pandas` e armazenados em formato Apache Parquet antes da carga no BigQuery.

**2. Armazenamento — Google BigQuery**

Os dados são carregados em uma camada `raw_data`, mantendo uma separação entre os dados brutos e as estruturas utilizadas para análise.

**3. Transformação — dbt Core**

O dbt é utilizado para organizar e executar as transformações no BigQuery, seguindo uma arquitetura em camadas:

* **Staging (`stg_cotacoes`):** limpeza, padronização de tipos e tratamento dos dados provenientes da camada bruta.
* **Marts (`fct_cotacoes_diarias`):** construção de uma tabela analítica com métricas derivadas, incluindo a variação percentual diária dos preços.

**4. Qualidade dos dados**

São utilizados testes automatizados do dbt para validar regras de integridade, incluindo verificações `not_null` nas colunas definidas como obrigatórias.

**5. Linhagem dos dados**

O dbt gerencia as dependências entre os modelos, permitindo visualizar a linhagem do pipeline:

```text
raw_data.cotacoes_acoes_raw
            │
            ▼
analytics.stg_cotacoes
            │
            ▼
analytics.fct_cotacoes_diarias
```

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia                    | Utilização                                     |
| ----------------------------- | ---------------------------------------------- |
| **Python 3.12**               | Ingestão e preparação dos dados                |
| **pandas**                    | Manipulação e estruturação dos dados           |
| **yfinance**                  | Extração dos dados de mercado                  |
| **Apache Parquet**            | Armazenamento intermediário em formato colunar |
| **Google BigQuery**           | Data Warehouse                                 |
| **dbt Core**                  | Transformação, modelagem e testes              |
| **GCP IAM / Service Account** | Autenticação e controle de acesso              |

---

## 📂 Estrutura do Repositório

```text
projeto-engenharia-dados/
│
├── dbt_analytics/
│   ├── models/
│   │   ├── staging/
│   │   │   ├── stg_cotacoes.sql
│   │   │   └── schema.yml
│   │   │
│   │   ├── marts/
│   │   │   └── fct_cotacoes_diarias.sql
│   │   │
│   │   └── sources.yml
│   │
│   ├── dbt_project.yml
│   └── profiles.yml
│
├── extract.py
├── README.md
└── .gitignore
```

### Principais componentes

**`extract.py`**
Responsável pela extração, preparação e carga dos dados no BigQuery.

**`stg_cotacoes.sql`**
Modelo de staging responsável pela limpeza e padronização dos dados.

**`fct_cotacoes_diarias.sql`**
Modelo analítico responsável pela consolidação das cotações e cálculo de métricas derivadas.

**`schema.yml`**
Define os testes de qualidade aplicados aos modelos.

**`sources.yml`**
Configura as fontes de dados utilizadas pelo projeto.

---

## 🚀 Como Executar

### Pré-requisitos

* Python 3.10+
* Projeto configurado no Google Cloud Platform
* BigQuery habilitado
* Credenciais de acesso configuradas para o ambiente local
* dbt Core com adaptador para BigQuery

### 1. Clone o repositório

```bash
git clone https://github.com/SEU_USUARIO/projeto-engenharia-dados.git
cd projeto-engenharia-dados
```

### 2. Crie um ambiente virtual

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Instale as dependências

```bash
pip install pandas yfinance google-cloud-bigquery dbt-bigquery
```

### 4. Execute a ingestão

```bash
python extract.py
```

### 5. Execute as transformações

```bash
cd dbt_analytics
dbt run
```

### 6. Execute os testes de qualidade

```bash
dbt test
```

### 7. Gere a documentação do dbt

```bash
dbt docs generate
dbt docs serve
```

---

## 🎯 Objetivos Técnicos Demonstrados

Este projeto demonstra a implementação de conceitos fundamentais de Engenharia de Dados:

* Pipeline de ingestão utilizando Python;
* Arquitetura ELT;
* Data Warehouse em cloud;
* Processamento e armazenamento em formato Parquet;
* Transformação de dados com SQL e dbt;
* Organização em camadas `raw`, `staging` e `marts`;
* Testes automatizados de qualidade;
* Modelagem de dados para análise;
* Linhagem e documentação dos modelos;
* Autenticação e controle de acesso no GCP.
