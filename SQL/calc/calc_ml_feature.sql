DROP FUNCTION IF EXISTS dw_tradinganalytics_sch.CalcFeatures(character varying, character varying);

CREATE OR REPLACE FUNCTION dw_tradinganalytics_sch.CalcFeatures(
    ticker_param VARCHAR,
    table_name_param VARCHAR
) 
RETURNS TABLE (
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
        stock_data_with_direction_volume AS (
            SELECT
                stock_data.close::NUMERIC,
                stock_data.high::NUMERIC,
                stock_data.low::NUMERIC,
                stock_data.datetime::TIMESTAMP,
                stock_data.ticker::VARCHAR,
                (close - open)::NUMERIC AS open_close_diff,
                (high - low)::NUMERIC AS high_low_diff,
                stock_data.volume::NUMERIC,
                direction_volume_calc.direction_volume::NUMERIC,
                SUM(direction_volume) OVER (ORDER BY stock_data.datetime ASC)::NUMERIC AS cumulative_volume
            FROM
                dw_tradinganalytics_sch.%I as stock_data
            JOIN direction_volume_calc 
                ON direction_volume_calc.datetime = stock_data.datetime
                AND direction_volume_calc.ticker = stock_data.ticker
            WHERE
                stock_data.ticker = %L
        )
        SELECT * FROM stock_data_with_direction_volume',
        table_name_param, table_name_param, ticker_param);

END;
$$ LANGUAGE plpgsql;