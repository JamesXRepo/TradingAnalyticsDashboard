CREATE VIEW dm_tradinganalytics_sch.view_ml_training_data AS
SELECT *
FROM dw_tradinganalytics_sch.CalcFeatures('AMD', 'ml_data_1m_dw')
WHERE EXTRACT(HOUR FROM datetime) >= 9
  AND EXTRACT(HOUR FROM datetime) < 16
  AND EXTRACT(MINUTE FROM datetime) >= 30
ORDER BY datetime ASC;

CREATE VIEW dm_tradinganalytics_sch.view_ml_training_data_5m AS
SELECT *
FROM dw_tradinganalytics_sch.CalcFeatures('AMD', 'ml_data_5m_dw')
WHERE EXTRACT(HOUR FROM datetime) >= 9
  AND EXTRACT(HOUR FROM datetime) < 16
  AND EXTRACT(MINUTE FROM datetime) >= 30
ORDER BY datetime ASC;