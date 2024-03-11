'''
The purpose of this class is provide numerous static metric calculations
'''

import pandas as pd

class Metrics:

    @staticmethod
    def cumulativeDirectionVolume(stock_data):
        stock_data['price_difference'] = stock_data['Close'] - stock_data['Open']
        stock_data['direction_volume'] = stock_data.apply(lambda row: -row['Volume'] if row['price_difference'] < 0 else row['Volume'], axis=1)
        stock_data['cumulative_volume'] = stock_data['direction_volume'].cumsum()

        return stock_data

    @staticmethod
    def pivotPoints(stock_data):

        # Store calculated values
        calculated_values = []

        # Initialize inputs needed to calculate metrics
        start_point = stock_data['Open'].iloc[0]
        start_date = stock_data.iloc[0].index
        prev_direct = 1 if (stock_data['Close'].iloc[0] - stock_data['Open'].iloc[0]) >= 0 else -1

        # Calculated and Append POI
        for index, row in stock_data.iloc[1:].iterrows():
            curr_range = abs(row['Close'] - start_point)
            curr_direct = 1 if row['Close'] - row['Open'] >= 0 else -1
            if (curr_direct == prev_direct):
                continue
            elif (curr_direct != prev_direct):
                end_date = index
                calculated_values.append({'datetime':start_date,'poi':start_point,'range':curr_range})
                calculated_values.append({'datetime':end_date,'poi':row['Close'],'range':curr_range})
                prev_direct = curr_direct
                start_point = row['Open']
                start_date = index

        # Convert calculated POI list into dataframe
        calculated_df = pd.DataFrame(calculated_values)
        calculated_df.set_index('datetime',inplace=True)

        # Filter for POI that are 2 Standard Deviations above average
        filtered_calculated_df = calculated_df[calculated_df['range'] >= (calculated_df['range'].mean() + 4*calculated_df['range'].std())]

        return filtered_calculated_df
    
    # Mark points of signficiant cumulative direction volume changes