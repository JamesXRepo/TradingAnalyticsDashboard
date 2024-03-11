'''
The purpose of this class is to create the dashboard to display various metrics, graphs, and etc... using Plotly
'''

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
from dash import Dash, html, dcc, Input, Output, State, callback_context, ctx
import dash_bootstrap_components as dbc
import warnings
warnings.simplefilter('ignore')
import math

from Metrics import Metrics
from Load import Load

graph_background_color = "#0f1014"
background_color = "#0d1116"
text_color = "#f5f6fa"
gridline_color = "#1b1f33"
bar_color = "#0b5978"
input_bg_color = "#24242e"
hover_color = "#1a1929"

current_ticker = 'AAPL'
current_interval = '5m'

event_count = 0

# Initialize the app
app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

# App Layout
app.layout = dbc.Container ([
    dbc.Row([
        dbc.Col(
            html.H1("Trading Analytics"),
            width=12,
            style={'backgroundColor': background_color ,'color' : text_color}
            )
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Input(id='input-ticker', placeholder='Enter ticker symbol', type='text', value=current_ticker,
                      className='mt-1 input-group-sm', 
                      style={
                          'width': '100%',
                          'background-color': input_bg_color, 
                          'color': text_color,
                          'border': '2px solid #0d1116'
                          },
                      ),
                      width=2,
                      style= {
                           'margin-top': '2px'
                      }
        ),
        dbc.Col(
            dcc.Dropdown(
                className="dropdown-item-text",
                id='dropdown-menu',
                options=[
                    {'label': '5min', 'value': '5m'},
                    {'label': '15min', 'value': '15m'},
                    {'label': '30min', 'value': '30m'},
                    {'label': '1hr', 'value': '1h'},
                    {'label': '1d', 'value': '1d'},
                    # Add more options as needed
                ],
                value=current_interval, # Set default value,
                style={
                    'background-color': hover_color,
                    'border-radius': '20px',  # Apply border-radius to give rounded corners
                    'border': '2px solid #0d1116',
                },
                clearable=False
            ),
            width=2,
            style={
                'width': '10%',  # Change width to 100% to fill the column
                'background-color': background_color,
            }
        )
    ],justify='start',
    style={'backgroundColor': background_color}),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='stock-graph',
                      style={'width': '100%', 
                             'height': '90vh'
                             })
        ])
    ],style={'backgroundColor': background_color,'border': '2px solid #0d1116'}) 
],fluid=True)

poi_visible = False  # Initially, set POI visibility to False

# Callback to update the graph based on input ticker and date range slider
@app.callback(
    Output('stock-graph', 'figure'),
    [Input('input-ticker', 'value'),
    Input('dropdown-menu','value'),
    Input('stock-graph','relayoutData'),
    Input('input-ticker', 'n_submit')],
    [State('input-ticker', 'id'),  # Add State to capture the ID of the triggering input
     State('dropdown-menu', 'id'),
     State('stock-graph', 'id')] 
)
def select_graph(ticker,interval,relayoutData,n_submit,input_id, dropdown_id, graph_id):


    # Check which input triggered the callback
    triggered_input = callback_context.triggered[0]['prop_id'].split('.')[0]

    current_ticker = ticker
    current_interval = interval

        # Calculate period based on selected interval
    if current_interval == '5m':
        period = '60d'
    elif current_interval == '15m':
        period = '60d'
    elif current_interval == '30m':
        period = '60d'
    elif current_interval == '1h':
        period = '1y'  # Approximately 2 years
    elif current_interval == '1d':
        period = '5y'

    global event_count
    global poi_visible

    if triggered_input == input_id and n_submit > event_count:
        # input-ticker triggered the callback
        event_count += 1

        # Fetch stock data and calculate points of interest
        temp_data = Load.yf_LoadData(current_ticker,period,current_interval)
        temp_index = temp_data.copy()
        temp_index.index = temp_index.index.date
        num_days = temp_index.index.nunique()
        # Get current time in the "America/New_York" timezone
        current_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-5)))  # Adjust UTC offset for "America/New_York"

        # Filter stock data based on selected date range
        start_date = current_time - datetime.timedelta(days=num_days)
        end_date = current_time

        stock_data = Metrics.cumulativeDirectionVolume(temp_data.loc[start_date:end_date])
        x_low = 0
        x_upper = len(stock_data)-1
    elif triggered_input == dropdown_id:
        # dropdown-menu triggered the callback

        # Fetch stock data and calculate points of interest
        temp_data = Load.yf_LoadData(current_ticker,period,current_interval)
        temp_index = temp_data.copy()
        temp_index.index = temp_index.index.date
        num_days = temp_index.index.nunique()
        # Get current time in the "America/New_York" timezone
        current_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-5)))  # Adjust UTC offset for "America/New_York"

        # Filter stock data based on selected date range
        start_date = current_time - datetime.timedelta(days=num_days)
        end_date = current_time

        stock_data = Metrics.cumulativeDirectionVolume(temp_data.loc[start_date:end_date])
        x_low = 0
        x_upper = len(stock_data)-1

    elif triggered_input == graph_id:
        # stock-graph triggered the callback

        # Fetch stock data and calculate points of interest
        temp_data = Load.yf_LoadData(current_ticker,period,current_interval)
        temp_index = temp_data.copy()
        temp_index.index = temp_index.index.date
        num_days = temp_index.index.nunique()
        # Get current time in the "America/New_York" timezone
        current_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-5)))  # Adjust UTC offset for "America/New_York"

        # Filter stock data based on selected date range
        start_date = current_time - datetime.timedelta(days=num_days)
        end_date = current_time
        
        stock_data = Metrics.cumulativeDirectionVolume(temp_data.loc[start_date:end_date])

        if 'xaxis2.range[0]' in relayoutData:
            x_low = math.floor(relayoutData['xaxis2.range[0]'])
        else:
            x_low = 0

        if 'xaxis2.range[1]' in relayoutData:
            x_upper = math.floor(relayoutData['xaxis2.range[1]'])
        else:
            x_upper = len(stock_data)-1
    

    # Create subplot
    fig1 = make_subplots(rows=2, cols=1, shared_xaxes=True,row_heights=[0.7, 0.3], vertical_spacing=0.05)

    # Plot candlestick chart
    fig1.add_trace(go.Candlestick(x=stock_data.index,
                    open=stock_data['Open'],
                    high=stock_data['High'],
                    low=stock_data['Low'],
                    close=stock_data['Close'], showlegend=False), row=1, col=1)
    
    supportAndResistanceLine = Metrics.pivotPoints(stock_data)
    pivot_trace = go.Scatter(x=supportAndResistanceLine.index, y=supportAndResistanceLine['poi'],
                            mode='markers', marker=dict(size=8),marker_color='#4bebd3',name='poi',showlegend=False,visible=False)
    
    fig1.add_trace(pivot_trace,row=1,col=1)
    fig1.add_trace(go.Bar(x=stock_data.index,y=stock_data['cumulative_volume'], name = 'Cumlative Direction Volume',marker_color=bar_color, showlegend=False), row=2, col=1)

    # Define button for toggling visibility
    pivot_button = dict(
        label='Pivot Point',
        method='update',
        args=[{'visible': [True,True,True]}]
    )

    none_button = dict(
        label='None',
        method='update',
        args=[{'visible': [True,False,True]}]
    )

    # Set layout
    fig1.update_layout(
            updatemenus=[
            dict(
                buttons=[none_button,pivot_button],
                direction='right',
                showactive=True,
                x=0,
                xanchor='left',
                y=1.1,
                yanchor='top',
                bordercolor = gridline_color,
                font=dict(color='white'),
                bgcolor= hover_color,
            )
        ],
        yaxis_title='Price',
        xaxis_rangeslider_visible=False,
        hovermode='x',
        paper_bgcolor=graph_background_color,
        plot_bgcolor=graph_background_color,
        hoverlabel=dict(namelength=0),
        yaxis=dict(
            title='Price',  # Set y-axis label for row 1, col 1
            title_font=dict(color=text_color),  # Set y-axis label color for row 1, col 1
            tickfont=dict(color=text_color),  # Set y-axis tick labels color for row 1, col 1
        ),
        yaxis2=dict(
            title='Cum. Direct. Vol.',  # Set y-axis label for row 2, col 1
            title_font=dict(color=text_color),  # Set y-axis label color for row 2, col 1
            tickfont=dict(color=text_color),  # Set y-axis tick labels color for row 2, col 1
        )
    )

    upper_range_stock = stock_data.iloc[x_low:x_upper]['Open'].max() + 2
    lower_range_stock = stock_data.iloc[x_low:x_upper]['Open'].min() - 2

    upper_range_cuml_vol = stock_data.iloc[x_low:x_upper]['cumulative_volume'].max()
    lower_range_cuml_vol = stock_data.iloc[x_low:x_upper]['cumulative_volume'].min()


    # Update x-axis for individual subplots
    fig1.update_xaxes(type='category', showgrid=False,range=[x_low,x_upper],showticklabels=False, row=1, col=1)
    fig1.update_xaxes(type='category', range=[x_low,x_upper],showticklabels=False, row=2, col=1)

    # Update y-axis layout for individual subplots to enable autorange
    fig1.update_yaxes(range=[lower_range_stock,upper_range_stock], gridwidth=1, gridcolor=gridline_color, row=1, col=1)
    fig1.update_yaxes(range=[lower_range_cuml_vol,upper_range_cuml_vol], gridwidth=1, gridcolor=gridline_color,row=2, col=1)

    return fig1

if __name__ == "__main__":
    app.run_server(debug=True)
