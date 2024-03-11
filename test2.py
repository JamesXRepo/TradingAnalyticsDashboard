import plotly.graph_objects as go

# Your existing code...

# Create subplot
fig1 = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.7, 0.3], vertical_spacing=0.05)

# Plot candlestick chart
fig1.add_trace(go.Candlestick(x=stock_data.index,
                open=stock_data['Open'],
                high=stock_data['High'],
                low=stock_data['Low'],
                close=stock_data['Close'], showlegend=False), row=1, col=1)

fig1.add_trace(go.Bar(x=stock_data.index,y=stock_data['cumulative_volume'], name='Cumulative Direction Volume', marker_color=bar_color, showlegend=False), row=2, col=1)

# Update x-axis for individual subplots
fig1.update_xaxes(type='category', showgrid=False, range=[x_low, x_upper], showticklabels=False, row=1, col=1)
fig1.update_xaxes(type='category', range=[x_low, x_upper], showticklabels=False, row=2, col=1)

# Add support and resistance points trace
poi_trace = go.Scatter(x=supportAndResistanceLine.index, y=supportAndResistanceLine['poi'],
                    mode='markers', marker=dict(size=8), marker_color='blue', name='POI', visible=True)

# Add the trace to the figure
fig1.add_trace(poi_trace, row=1, col=1)

# Define button for toggling visibility
toggle_button = dict(
    label='Toggle POI',
    method='update',
    args=[{'visible': [True, False]}, {'title': 'POI'}]
)

# Update layout with the toggle button
fig1.update_layout(
    updatemenus=[
        dict(
            buttons=[toggle_button],
            direction='down',
            showactive=True,
            x=0.1,
            xanchor='left',
            y=1.1,
            yanchor='top'
        ),
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

# Update y-axis layout for individual subplots to enable autorange
fig1.update_yaxes(range=[lower_range_stock, upper_range_stock], gridwidth=1, gridcolor=gridline_color, row=1, col=1)
fig1.update_yaxes(range=[lower_range_cuml_vol, upper_range_cuml_vol], gridwidth=1, gridcolor=gridline_color, row=2, col=1)

# Your existing code...

# Return the figure
return fig1
