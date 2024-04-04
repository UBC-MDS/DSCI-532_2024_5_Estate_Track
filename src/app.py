from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Initialize the Dash app with Bootstrap CSS
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Read the CSV file
df = pd.read_csv('data/raw/HouseListings.csv', encoding='latin-1')

# Define layout
app.layout = html.Div([
    html.Div([
        html.H1('HomeScope', style={'color': '#2AAA8A', 'font-size': '3em', 'font-family': 'Arial', 'text-align': 'center'})
    ]),
    dbc.Row([
        dbc.Col([
            html.Label("Province"),
            dcc.Dropdown(
                id='province-dropdown',
                options=[{'label': province, 'value': province} for province in sorted(df['Province'].unique())],
                value=sorted(df['Province'].unique())[0]
            ),
            html.Label("City"),
            dcc.Dropdown(
                id='city-dropdown'
                # The initial options and value will be set by the callback
            ),
            html.Label("Price Range"),
            dcc.RangeSlider(
                id='price-range-slider',
                min=int(df['Price'].min()),
                max=int(df['Price'].max()),
                step=10000000,  # A step size more appropriate for house prices
                value=[int(df['Price'].min()), int(df['Price'].max())],
                updatemode='drag'
            ),
            html.Label("Number of Beds"),
            dcc.Slider(
                id='beds-slider',
                min=int(df['Number_Beds'].min()),
                max=int(df['Number_Beds'].max()),
                step=6,
                value=int(df['Number_Beds'].min()),
                updatemode='drag'
            ),
            html.Label("Number of Baths"),
            dcc.Slider(
                id='baths-slider',
                min=int(df['Number_Baths'].min()),
                max=int(df['Number_Baths'].max()),
                step=6,
                value=int(df['Number_Baths'].min()),
                updatemode='drag'
            )
        ], md=3),
        dbc.Col([
            dcc.Graph(id='output-graph')
        ], md=9)
    ])
])

# Callback for city-dropdown options based on selected province
@app.callback(
    [Output('city-dropdown', 'options'),
     Output('city-dropdown', 'value')],
    [Input('province-dropdown', 'value')]
)
def set_city_options(selected_province):
    cities = sorted(df[df['Province'] == selected_province]['City'].unique())
    if cities:
        return [{'label': city, 'value': city} for city in cities], cities[0]
    else:
        return [], None

# Define callback to update output graph
@app.callback(
    Output('output-graph', 'figure'),
    [Input('province-dropdown', 'value'),
     Input('city-dropdown', 'value'),
     Input('price-range-slider', 'value'),
     Input('beds-slider', 'value'),
     Input('baths-slider', 'value')]
)
def update_output_graph(province, city, price_range, beds, baths):
    filtered_df = df[
        (df['Province'] == province) & 
        (df['City'] == city) & 
        (df['Price'] >= price_range[0]) & 
        (df['Price'] <= price_range[1]) & 
        (df['Number_Beds'] >= beds) & 
        (df['Number_Baths'] >= baths)
    ]
    fig = px.scatter(
        filtered_df, 
        x='Price', 
        y='Number_Beds', 
        size='Number_Baths', 
        color='City', 
        hover_name='Address', 
        log_x=True, 
        size_max=15
    )
    return fig

# Run the Dash application
if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1')




