## (Currently in development)

# Trading Analytics Dashboard
- The purpose of this analytics dashboard is to provide ability to identify day trading opportunities by leveraging custom metrics to identify supply and demand imbalances.
- Furthermore, custom metrics and other features are leveraged to traing LSTM model to predict next day price action.
- To provide users with a holistic view of the market, dashboard also provides broad view of index and etf metrics along with ability to analyze price correlation between user selected etf and index

## Technology
- Local (Designed for rapid development)
    - Postgresql
    - Python
    - Tensorflow / Keras
- Cloud (Designed to contain up-to-date data and full tested features)
    - Aurora (Postgresql)
    - Python
    - Sagemaker (Tensorflow / Keras)
    - Ec2
    - Elastic Beanstalk for ease of web app deployment

## General Data Architecture
- The database is split into three schemas: staging, datawarehouse, and datamarts
    - Staging: Stores raw data with all varchar datatype
    - Datawarhouse: Stores minimial transformed data with accurate datatypes
    - Datamarts: Stores tailored data to be utilized by dashboard for distinctly purposed displays and usage
- Various procedures and functions are incorporated to automate data reconciliation, data transformations, and table creations

## Usage
- The code stored in this repo is not designed to be downloaded and ran on personal machine
