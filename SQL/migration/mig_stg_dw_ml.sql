CREATE OR REPLACE PROCEDURE stg_tradinganalytics_sch.migration_stg_dw_ml_data() AS
$$
BEGIN
INSERT INTO dw_tradinganalytics_sch.ml_data_1m_dw(datetime, open, high, low, close, volume, ticker, transaction_cnt)
SELECT  TO_TIMESTAMP(t::NUMERIC/1000.0) AT TIME ZONE 'UTC' AS datetime,
        o::NUMERIC,
        h::NUMERIC,
        l::NUMERIC,
        c::NUMERIC,
        v::NUMERIC,
        ticker::VARCHAR,
        n::INTEGER
FROM stg_tradinganalytics_sch.ml_data_1m_stg;
END;
$$
LANGUAGE plpgsql;