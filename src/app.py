from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Initialize the Dash app with Bootstrap CSS
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Read the CSV file
df = pd.read_csv('data/raw/HouseListings.csv', encoding='latin-1')

# Components
title = [html.H1('HomeScope', style={'color': '#2AAA8A', 'font-size': '3em', 'font-family': 'Arial', 'text-align': 'center'}), html.Br()]
province_dropdown = dcc.Dropdown(
    id='province-dropdown',
    options=[{'label': province, 'value': province} for province in sorted(df['Province'].unique())],
    value=sorted(df['Province'].unique())[0]
)
city_dropdown = dcc.Dropdown(id='city-dropdown')  # Options will be dynamically generated
price_range_slider = dcc.RangeSlider(
    id='price-range-slider',
    min=int(df['Price'].min()),
    max=int(df['Price'].max()),
    step=10000000,
    value=[int(df['Price'].min()), int(df['Price'].max())],
    updatemode='drag'
)
beds_slider = dcc.Slider(
    id='beds-slider',
    min=int(df['Number_Beds'].min()),
    max=int(df['Number_Beds'].max()),
    step=6,
    value=int(df['Number_Beds'].min()),
    updatemode='drag'
)
baths_slider = dcc.Slider(
    id='baths-slider',
    min=int(df['Number_Baths'].min()),
    max=int(df['Number_Baths'].max()),
    step=6,
    value=int(df['Number_Baths'].min()),
    updatemode='drag'
)
output_graph = dcc.Graph(id='output-graph')

# Assembling global widgets
global_widgets = [
    dbc.Label("Province"),
    province_dropdown,
    html.Br(),
    dbc.Label("City"),
    city_dropdown,
    html.Br(),
    dbc.Label("Price Range"),
    price_range_slider,
    html.Br(),
    dbc.Label("Number of Beds"),
    beds_slider,
    html.Br(),
    dbc.Label("Number of Baths"),
    baths_slider,
]

# Layout
app.layout = dbc.Container([
    dbc.Row(dbc.Col(title)),
    dbc.Row([
        dbc.Col(global_widgets, md=4),
        dbc.Col(output_graph, md=8),
    ])
], fluid=True)

# Callbacks
@app.callback(
    [Output('city-dropdown', 'options'),
     Output('city-dropdown', 'value')],
    [Input('province-dropdown', 'value')]
)
def update_city_dropdown(selected_province):
    # Get unique cities for the selected province
    unique_cities = sorted(df[df['Province'] == selected_province]['City'].unique())
    # Create a list of options for the dropdown
    city_options = [{'label': city, 'value': city} for city in unique_cities]
    # Set the default value to the first city in the list or None if list is empty
    city_value = unique_cities[0] if unique_cities else None
    return city_options, city_value

# Callback to update output graph based on selected filters
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





