# Trading Analytics Dashboard
- The purpose of this analytics dashboard is to provide ability to identify day trading opportunities by leveraging custom metrics to identify supply and demand imbalances.
- Furthermore, custom metrics and other features are leveraged to traing LSTM model to predict next day price action.
- To provide users with a holistic view of the market, dashboard also provides broad view of index and etf metrics along with ability to analyze price correlation between user selected etf and index

## Architecture and Technology
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
