WITH staging AS (
    SELECT * 
    FROM {{ ref('stg_cotacoes') }}
)

SELECT
    data_pregao,
    ticker,
    preco_abertura,
    preco_fechamento,
    ROUND((preco_fechamento - preco_abertura) / preco_abertura * 100, 2) AS variacao_diaria_pct,
    preco_maximo,
    preco_minimo,
    volume_negociado,
    data_ingestao
FROM staging