CREATE TABLE IF NOT EXISTS dm_tradinganalytics_sch.index_data_15m_dm (
    datetime TIMESTAMP,
    price NUMERIC,
    volume NUMERIC,
    ticker VARCHAR
);

CREATE TABLE IF NOT EXISTS dm_tradinganalytics_sch.index_data_1h_dm (
    datetime TIMESTAMP,
    price NUMERIC,
    volume NUMERIC,
    ticker VARCHAR
);

CREATE TABLE IF NOT EXISTS dm_tradinganalytics_sch.index_data_1d_dm (
    datetime TIMESTAMP,
    price NUMERIC,
    volume NUMERIC,
    ticker VARCHAR
);

CREATE TABLE IF NOT EXISTS dm_tradinganalytics_sch.etf_data_15m_dm (
    datetime TIMESTAMP,
    price NUMERIC,
    volume NUMERIC,
    ticker VARCHAR
);

CREATE TABLE IF NOT EXISTS dm_tradinganalytics_sch.etf_data_1h_dm (
    datetime TIMESTAMP,
    price NUMERIC,
    volume NUMERIC,
    ticker VARCHAR
);

CREATE TABLE IF NOT EXISTS dm_tradinganalytics_sch.etf_data_1d_dm (
    datetime TIMESTAMP,
    price NUMERIC,
    volume NUMERIC,
    ticker VARCHAR
);