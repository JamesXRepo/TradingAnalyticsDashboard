-- Tables to store 15min, 1hr, and 1day index data
CREATE TABLE IF NOT EXISTS stg_tradinganalytics_sch.index_data_15m_stg (
    datetime TIMESTAMP,
    open VARCHAR,
    high VARCHAR,
    low VARCHAR,
    close VARCHAR,
    volume VARCHAR,
    ticker VARCHAR
);

CREATE TABLE IF NOT EXISTS stg_tradinganalytics_sch.index_data_1h_stg (
    datetime TIMESTAMP,
    open VARCHAR,
    high VARCHAR,
    low VARCHAR,
    close VARCHAR,
    volume VARCHAR,
    ticker VARCHAR
);

CREATE TABLE IF NOT EXISTS stg_tradinganalytics_sch.index_data_1d_stg (
    datetime TIMESTAMP,
    open VARCHAR,
    high VARCHAR,
    low VARCHAR,
    close VARCHAR,
    volume VARCHAR,
    ticker VARCHAR
);

-- Tables to store 15min, 1hr, and 1day etf data
CREATE TABLE IF NOT EXISTS stg_tradinganalytics_sch.etf_data_15m_stg (
    datetime TIMESTAMP,
    open VARCHAR,
    high VARCHAR,
    low VARCHAR,
    close VARCHAR,
    volume VARCHAR,
    ticker VARCHAR
);

CREATE TABLE IF NOT EXISTS stg_tradinganalytics_sch.etf_data_1h_stg (
    datetime TIMESTAMP,
    open VARCHAR,
    high VARCHAR,
    low VARCHAR,
    close VARCHAR,
    volume VARCHAR,
    ticker VARCHAR
);

CREATE TABLE IF NOT EXISTS stg_tradinganalytics_sch.etf_data_1d_stg (
    datetime TIMESTAMP,
    open VARCHAR,
    high VARCHAR,
    low VARCHAR,
    close VARCHAR,
    volume VARCHAR,
    ticker VARCHAR
);