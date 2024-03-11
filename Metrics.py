class Metrics:

    @staticmethod
    def cumulativeDirectionVolume(stock_data):
        stock_data['price_difference'] = stock_data['Close'] - stock_data['Open']
        stock_data['direction_volume'] = stock_data.apply(lambda row: -row['Volume'] if row['price_difference'] < 0 else row['Volume'], axis=1)
        stock_data['cumulative_volume'] = stock_data['direction_volume'].cumsum()

        return stock_data
