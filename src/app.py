from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Initialize the Dash app with Bootstrap CSS
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Read the CSV file
df = pd.read_csv('data/raw/HouseListings.csv', encoding='latin-1')

# Components
title = [html.H1('HomeScope', style={'color': '#2AAA8A', 'font-size': '3em', 'font-family': 'Arial', 'text-align': 'center'}), html.Br()]
province_dropdown = dcc.Dropdown(
    id='province-dropdown',
    options=[{'label': province, 'value': province} for province in sorted(df['Province'].unique())],
    value='British Columbia'  # Changed from sorted(df['Province'].unique())[0]
)

city_dropdown = dcc.Dropdown(
    id='city-dropdown',
    multi = True
)  # Options will be dynamically generated
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
map_graph = dcc.Graph(id='map-graph')

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
        dbc.Col(map_graph,md=8)
    ])
], fluid=True)

# Callback to update city-dropdown options and values based on selected province
@app.callback(
    [Output('city-dropdown', 'options'),
     Output('city-dropdown', 'value')],
    [Input('province-dropdown', 'value')]
)
def update_city_dropdown(selected_province):
    unique_cities = sorted(df[df['Province'] == selected_province]['City'].unique())
    city_options = [{'label': city, 'value': city} for city in unique_cities]
    
    # Pre-select Vancouver if British Columbia is selected
    if unique_cities:
        city_value = unique_cities[0]
    else:
        city_value = []  # No cities are pre-selected if not British Columbia

    return city_options, city_value


# Callback to update output graph based on selected filters
@app.callback(
    Output('output-graph', 'figure'),
    #  Output('map-graph', 'figure')],
    [Input('province-dropdown', 'value'),
     Input('city-dropdown', 'value'),
     Input('price-range-slider', 'value'),
     Input('beds-slider', 'value'),
     Input('baths-slider', 'value')]
)
def update_output_graph(province, cities, price_range, beds, baths):
    # Handle the case where cities might be a string (single selection) or None
    if not cities:  # This checks both for None and for an empty list
        return px.scatter(title="Please select at least one city.")
    
    if isinstance(cities, str):
        cities = [cities]  # Wrap string in list if it's not a list already

    filtered_df = df[
        (df['Province'] == province) &
        (df['City'].isin(cities)) &
        (df['Price'] >= price_range[0]) &
        (df['Price'] <= price_range[1]) &
        (df['Number_Beds'] >= beds) &
        (df['Number_Baths'] >= baths)
    ]

    # If the filtered dataframe is empty, show an informative message
    if filtered_df.empty:
        return px.scatter(title="No listings match the selected criteria.")

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

@app.callback(
   
     Output('map-graph', 'figure'),
    [Input('province-dropdown', 'value'),
     Input('city-dropdown', 'value')]
)
def update_map_graph(province, cities):
    # Selecting the province and setting up latitude and longitudes

    province_df = df[df['Province'] == province]

    avg_lat = province_df['Latitude'].mean()
    avg_lon = province_df['Longitude'].mean()

    # Calculate the average price for each city within the selected province
    city_avg_prices = province_df.groupby('City').agg({'Price': 'mean'}).reset_index()

    # Merge the average prices with the city locations
    city_avg_prices = city_avg_prices.merge(province_df[['City', 'Latitude', 'Longitude','Median_Family_Income']].drop_duplicates(),
                                            on='City', 
                                            how='left')
    city_avg_prices.rename(columns={'Price': 'Avg_Price', "Median_Family_Income":"Median_Income"}, inplace=True)
    # Geospatial map for housing data
    map_fig = px.scatter_mapbox(city_avg_prices, 
                                lat="Latitude", 
                                lon="Longitude", 
                                color = "City" ,
                                hover_data={"City": True, 
                                            "Latitude": False,
                                            "Longitude":False,
                                            "Avg_Price":':.2f',
                                            "Median_Income":True}, 
                                zoom=10,
                                center={"lat": avg_lat, "lon": avg_lon})
    map_fig.update_layout(mapbox_style="open-street-map")
    map_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    return map_fig



# Run the Dash application
if __name__ == '__main__':
    app.run_server(debug=False, host='127.0.0.1')
