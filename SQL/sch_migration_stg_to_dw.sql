CREATE OR REPLACE PROCEDURE stg_tradinganalytics_sch.schema_migration_stg_to_dw() AS
$$
BEGIN
    INSERT INTO dw_tradinganalytics_sch.index_data_15m_dw (datetime, open, high, low, close, volume, ticker)
    SELECT datetime::TIMESTAMP,
           open::NUMERIC,
           high::NUMERIC,
           low::NUMERIC,
           close::NUMERIC,
           volume::INTEGER,
           ticker::VARCHAR
    FROM stg_tradinganalytics_sch.index_data_15m_stg;

    INSERT INTO dw_tradinganalytics_sch.index_data_1h_dw (datetime, open, high, low, close, volume, ticker)
    SELECT datetime::TIMESTAMP,
           open::NUMERIC,
           high::NUMERIC,
           low::NUMERIC,
           close::NUMERIC,
           volume::INTEGER,
           ticker::VARCHAR
    FROM stg_tradinganalytics_sch.index_data_1h_stg;

    INSERT INTO dw_tradinganalytics_sch.etf_data_15m_dw (datetime, open, high, low, close, volume, ticker)
    SELECT datetime::TIMESTAMP,
           open::NUMERIC,
           high::NUMERIC,
           low::NUMERIC,
           close::NUMERIC,
           volume::INTEGER,
           ticker::VARCHAR
    FROM stg_tradinganalytics_sch.etf_data_15m_stg;

    INSERT INTO dw_tradinganalytics_sch.etf_data_1h_dw (datetime, open, high, low, close, volume, ticker)
    SELECT datetime::TIMESTAMP,
           open::NUMERIC,
           high::NUMERIC,
           low::NUMERIC,
           close::NUMERIC,
           volume::INTEGER,
           ticker::VARCHAR
    FROM stg_tradinganalytics_sch.etf_data_1h_stg;
END;
$$
LANGUAGE plpgsql;



