import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, dcc, html, Input, Output

# Load and preprocess data
print("Attempting to load NFLX.csv...")
df = pd.read_csv("NFLX.csv")
print("Data loaded successfully:", df.head())

df['Date'] = pd.to_datetime(df['Date'])
df['day'] = df['Date'].dt.day
df['month'] = df['Date'].dt.month
df['year'] = df['Date'].dt.year

# Initialize Dash app
app = Dash(__name__)
server=app.server

# Set a dark theme for the dashboard layout
app.layout = html.Div(
    style={'backgroundColor': '#000000', 'color': '#E50914', 'padding': '20px', 'font-family': 'Arial'},
    children=[
        html.H1("Netflix Stock Dashboard", style={'text-align': 'center', 'color': '#E50914'}),
        
        # Dropdown for stock metrics
        html.Label("Select Stock Metric:", style={'color': '#E50914'}),
        dcc.Dropdown(
            id='metric-dropdown',
            options=[
                {'label': 'Volume', 'value': 'Volume'},
                {'label': 'Open', 'value': 'Open'},
                {'label': 'High', 'value': 'High'},
                {'label': 'Low', 'value': 'Low'},
                {'label': 'Close', 'value': 'Close'}
            ],
            value='Volume',
            style={'backgroundColor': '#333', 'color': '#E50914'}
        ),
        
        # Line Chart
        dcc.Graph(id='line-chart'),
        
        # Subplots for Volume by day, month, and year
        html.H2("Volume Subplots by Day, Month, and Year", style={'text-align': 'center', 'color': '#E50914'}),
        dcc.Graph(id='volume-subplots'),
        
        # Dropdown for Top 5 Stock Prices (High/Low)
        html.Label("Select Top 5 Stock Prices:", style={'color': '#E50914'}),
        dcc.Dropdown(
            id='top-5-dropdown',
            options=[
                {'label': 'Top 5 Highest Stock Prices', 'value': 'High'},
                {'label': 'Top 5 Lowest Stock Prices', 'value': 'Low'}
            ],
            value='High',
            style={'backgroundColor': '#333', 'color': '#E50914'}
        ),
    
        # Top 5 Dates with Highest/Lowest Stock Price
        html.H2("Top 5 Dates with Highest/Lowest Stock Price", style={'color': '#E50914'}),
        dcc.Graph(id='top-5-bar')
    ]
)

# Callback to update line chart
@app.callback(
    Output('line-chart', 'figure'),
    Input('metric-dropdown', 'value')
)
def update_line_chart(metric):
    line_color = 'blue'  # Default color
    if metric == 'High':
        line_color = 'green'
    elif metric == 'Low':
        line_color = 'red'
    
    fig = px.line(df, x='Date', y=metric, title=f"Netflix {metric} over Time")
    fig.update_traces(line=dict(color=line_color))
    
    # Set dark theme for the figure
    fig.update_layout(
        plot_bgcolor='#000000',
        paper_bgcolor='#000000',
        font=dict(color='#E50914'),
        title_font=dict(size=24, color='#E50914'),
        xaxis=dict(showgrid=False, color='#E50914'),
        yaxis=dict(showgrid=False, color='#E50914')
    )
    return fig

# Callback for volume subplots by day, month, and year
@app.callback(
    Output('volume-subplots', 'figure'),
    Input('metric-dropdown', 'value')  # Placeholder input to trigger callback
)
def update_volume_subplots(_):
    fig = make_subplots(rows=1, cols=3, subplot_titles=("Volume by Day", "Volume by Month", "Volume by Year"))
    
    # Add traces with different line colors for each subplot
    fig.add_trace(go.Scatter(x=df["day"], y=df['Volume'], mode='lines', name="Day", line=dict(color='blue')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['month'], y=df['Volume'], mode="lines", name="Month", line=dict(color='red')), row=1, col=2)
    fig.add_trace(go.Scatter(x=df['year'], y=df['Volume'], mode='lines', name="Year", line=dict(color='green')), row=1, col=3)
    
    # Set dark theme and remove grid lines for each subplot axis
    fig.update_layout(
        plot_bgcolor='#000000',
        paper_bgcolor='#000000',
        font=dict(color='#E50914'),
        title_font=dict(size=18, color='#E50914')
    )
    
    fig.update_xaxes(showgrid=False, color='#E50914')
    fig.update_yaxes(showgrid=False, color='#E50914')

    return fig

# Callback to display top 5 dates with highest or lowest stock price
@app.callback(
    Output('top-5-bar', 'figure'),
    Input('top-5-dropdown', 'value')  # Use 'top-5-dropdown' to trigger callback
)
def update_top_5_chart(metric):
    if metric == 'High':
        top_5_df = df.sort_values(by='High', ascending=False).head(5)
        fig = px.bar(top_5_df, x='Date', y='High', title="Top 5 Dates with Highest Stock Price")
    elif metric == 'Low':
        top_5_df = df.sort_values(by='Low', ascending=True).head(5)
        fig = px.bar(top_5_df, x='Date', y='Low', title="Top 5 Dates with Lowest Stock Price")
    else:
        fig = go.Figure()
    
    # Set dark theme for the figure
    fig.update_layout(
        plot_bgcolor='#000000',
        paper_bgcolor='#000000',
        font=dict(color='#E50914'),
        title_font=dict(size=18, color='#E50914'),
        xaxis=dict(showgrid=False, color='#E50914'),
        yaxis=dict(showgrid=False, color='#E50914'),
        bargap=0.2
    )
    fig.update_traces(marker_color='#E50914')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
