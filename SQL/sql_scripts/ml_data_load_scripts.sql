CREATE OR REPLACE PROCEDURE stg_tradinganalytics_sch.migration_stg_dw_ml_data() AS
$$
BEGIN
INSERT INTO dw_tradinganalytics_sch.ml_data_5m_dw(datetime, open, high, low, close, volume, ticker, transaction_cnt)
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

CALL stg_tradinganalytics_sch.migration_stg_dw_ml_data();

DROP FUNCTION IF EXISTS dw_tradinganalytics_sch.CalcFeatures(character varying, character varying);

CREATE OR REPLACE FUNCTION dw_tradinganalytics_sch.CalcFeatures(
    ticker_param VARCHAR,
    table_name_param VARCHAR
) 
RETURNS TABLE (
	transaction_cnt NUMERIC,
    close NUMERIC,
    high NUMERIC,
    low NUMERIC,
    datetime TIMESTAMP,
    ticker VARCHAR,
    open_close_diff NUMERIC,
    high_low_diff NUMERIC,
    volume NUMERIC,
    direction_volume NUMERIC,
    cumulative_volume NUMERIC
)
AS $$
BEGIN
    RETURN QUERY EXECUTE format('
        WITH direction_volume_calc AS (
            SELECT
                datetime,
                ticker,
                CASE
                    WHEN (close - open) > 0 THEN volume
                    WHEN (close - open) < 0 THEN -volume
                    ELSE volume
                END AS direction_volume
            FROM
                dw_tradinganalytics_sch.%I
        ),
        polygon_data_with_direction_volume AS (
            SELECT
				polygon_data.transaction_cnt::NUMERIC,
                polygon_data.close::NUMERIC,
                polygon_data.high::NUMERIC,
                polygon_data.low::NUMERIC,
                polygon_data.datetime::TIMESTAMP,
                polygon_data.ticker::VARCHAR,
                (close - open)::NUMERIC AS open_close_diff,
                (high - low)::NUMERIC AS high_low_diff,
                polygon_data.volume::NUMERIC,
                direction_volume_calc.direction_volume::NUMERIC,
                SUM(direction_volume) OVER (ORDER BY polygon_data.datetime ASC)::NUMERIC AS cumulative_volume
            FROM
                dw_tradinganalytics_sch.%I as polygon_data
            JOIN direction_volume_calc 
                ON direction_volume_calc.datetime = polygon_data.datetime
                AND direction_volume_calc.ticker = polygon_data.ticker
            WHERE
                polygon_data.ticker = %L
        )
        SELECT * FROM polygon_data_with_direction_volume',
        table_name_param, table_name_param, ticker_param);

END;
$$ LANGUAGE plpgsql;