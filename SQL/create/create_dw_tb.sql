CREATE TABLE IF NOT EXISTS dw_tradinganalytics_sch.index_data_15m_dw (
    datetime TIMESTAMP,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    volume INTEGER,
    ticker VARCHAR
);

CREATE TABLE IF NOT EXISTS dw_tradinganalytics_sch.index_data_1h_dw (
    datetime TIMESTAMP,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    volume INTEGER,
    ticker VARCHAR
);

CREATE TABLE IF NOT EXISTS dw_tradinganalytics_sch.index_data_1d_dw (
    datetime TIMESTAMP,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    volume INTEGER,
    ticker VARCHAR
);

CREATE TABLE IF NOT EXISTS dw_tradinganalytics_sch.etf_data_15m_dw (
    datetime TIMESTAMP,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    volume INTEGER,
    ticker VARCHAR
);

CREATE TABLE IF NOT EXISTS dw_tradinganalytics_sch.etf_data_1h_dw (
    datetime TIMESTAMP,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    volume INTEGER,
    ticker VARCHAR
);

CREATE TABLE IF NOT EXISTS dw_tradinganalytics_sch.etf_data_1d_dw (
    datetime TIMESTAMP,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    volume INTEGER,
    ticker VARCHAR
);

CREATE TABLE IF NOT EXISTS dw_tradinganalytics_sch.market_watchlist (
    ticker VARCHAR PRIMARY KEY,
    name VARCHAR,
    type VARCHAR 
)

CREATE TABLE IF NOT EXISTS dw_tradinganalytics_sch.ml_data_dw (
    datetime TIMESTAMP,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    volume INTEGER,
    ticker VARCHAR
);