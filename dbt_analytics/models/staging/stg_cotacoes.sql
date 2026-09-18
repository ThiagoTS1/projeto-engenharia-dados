WITH fonte AS (
    SELECT * 
    FROM {{ source('raw_sources', 'cotacoes_acoes_raw') }}
)

SELECT
    SAFE_CAST(Date AS DATE) AS data_pregao,
    'PETR4.SA' AS ticker,
    ROUND(SAFE_CAST(Open AS NUMERIC), 2) AS preco_abertura,
    ROUND(SAFE_CAST(High AS NUMERIC), 2) AS preco_maximo,
    ROUND(SAFE_CAST(Low AS NUMERIC), 2) AS preco_minimo,
    ROUND(SAFE_CAST(Close AS NUMERIC), 2) AS preco_fechamento,
    SAFE_CAST(Volume AS INT64) AS volume_negociado,
    data_ingestao
FROM fonte
WHERE Date IS NOT NULL