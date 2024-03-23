CREATE OR REPLACE PROCEDURE stg_tradinganalytics_sch.migration_stg_dw_ml_data() AS
$$
BEGIN
    INSERT INTO dw_tradinganalytics_sch.ml_data_5m_dw (datetime, open, high, low, close, volume, ticker)
    SELECT datetime::TIMESTAMP,
           open::NUMERIC,
           high::NUMERIC,
           low::NUMERIC,
           close::NUMERIC,
           volume::INTEGER,
           ticker::VARCHAR
    FROM stg_tradinganalytics_sch.ml_data_5m_dw;
END;
$$
LANGUAGE plpgsql;