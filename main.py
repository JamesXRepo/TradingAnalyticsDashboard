from dash import Dash, html, dcc, Input, Output
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots


def test_func(ticker):
    aapl = yf.Ticker(ticker)
    stock_data = aapl.history(period='1y',interval='60m')
    stock_data.head()

    # Store calculated values
    calculated_values = []

    # Initialize inputs needed to calculate metrics
    start_point = stock_data['Open'].iloc[0]
    start_date = stock_data.iloc[0].index
    date = stock_data.index[0]
    prev_direct = 1 if (stock_data['Close'].iloc[0] - stock_data['Open'].iloc[0]) >= 0 else -1
    prev_range = abs(stock_data['Close'].iloc[0] - stock_data['Open'].iloc[0])

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
            poi = row['Open']

    # Convert calculated POI list into dataframe
    calculated_df = pd.DataFrame(calculated_values)
    calculated_df.set_index('datetime',inplace=True)

    # Filter for POI that are 2 Standard Deviations above average
    filtered_calculated_df = calculated_df[calculated_df['range'] >= calculated_df['range'].mean() + 2*calculated_df['range'].std()]
    return filtered_calculated_df, stock_data

# Initialize the app
app = Dash(__name__)

# App Layout
app.layout = html.Div(children=[
    dcc.Input(id='input-ticker', placeholder='Enter ticker symbol', type='text', value='AAPL'),
    dcc.Graph(id='my-graph', style={'width': '100%', 'height': '100vh'})
])


# Callback to update the graph based on input ticker
@app.callback(
    Output('my-graph', 'figure'),
    [Input('input-ticker', 'value')]
)
def update_graph(selected_ticker):
    metrics, stock_data = test_func(selected_ticker)

    # Create subplot ----------------------
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True, vertical_spacing=0.02)

    # Plot candlestick chart
    fig.add_trace(go.Candlestick(x=stock_data.index,
                    open=stock_data['Open'],
                    high=stock_data['High'],
                    low=stock_data['Low'],
                    close=stock_data['Close'],showlegend=False),row=1,col=1)

    # Add scatter markers for filtered calculated data
    fig.add_trace(go.Scatter(x=metrics.index, y=metrics['poi'],
                            mode='markers', marker=dict(size=8),marker_color='blue',name='poi',showlegend=False),row=1,col=1)

    # Add horizontal lines for each point of interest
    for datetime, poi in metrics.iterrows():
        fig.add_trace(go.Scatter(x=[stock_data.index.min(), stock_data.index.max()], y=[poi['poi'], poi['poi']],
                                mode='lines', line=dict(color="red", width=1),
                                name=f"POI at {datetime}", showlegend=False),row=1,col=1)

    # Set layout
    fig.update_layout(
        yaxis_title='Price'
    )

    fig.update_layout(
        yaxis_title='Price',
        xaxis_rangeslider_visible=False,
        xaxis=dict(
            type='category',
            showticklabels=False
        )
    )
    return fig


if __name__ == "__main__":
    app.run(debug=False)

