from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import dash_daq as daq
import plotly.graph_objects as go

# Initialize the Dash app with Bootstrap CSS
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Read the CSV file
df = pd.read_csv('data/raw/HouseListings.csv', encoding='latin-1')

# Dropdown options for variable1 and variable2
variable_options = [{'label': col, 'value': col} for col in ['Price', 'Number_Beds', 'Number_Baths', 'Population', 'Median_Family_Income']]

# Components
title = html.H1('HomeScope', style={'color': '#2AAA8A', 'font-size': '3em', 'font-family': 'Arial', 'text-align': 'center'})
province_dropdown = dcc.Dropdown(id='province-dropdown', options=[{'label': province, 'value': province} for province in sorted(df['Province'].unique())], value='British Columbia')
city_dropdown = dcc.Dropdown(id='city-dropdown', multi=True)
price_range_slider = dcc.RangeSlider(id='price-range-slider', min=int(df['Price'].min()), max=int(df['Price'].max()), step=10000000, value=[int(df['Price'].min()), int(df['Price'].max())], updatemode='drag')
beds_numeric_input = daq.NumericInput(id='beds-numeric-input', label='Number of Beds', labelPosition='top', min=0, max=109, value=3)
baths_numeric_input = daq.NumericInput(id='baths-numeric-input', label='Number of Baths', labelPosition='top', min=0, max=59, value=2)
variable1_dropdown = dcc.Dropdown(id='variable1-dropdown', options=['Price', 'Population', 'Median_Family_Income'], value='Price')
variable2_dropdown = dcc.Dropdown(id='variable2-dropdown', options=['Price', 'Population', 'Median_Family_Income'], value='Median_Family_Income')

output_histogram = dcc.Graph(id='output-histogram')
# Card for displaying the average, min and max price dynamically
card_avg_price = dbc.Card(id='card-avg-price', children=[
    dbc.CardBody([
        html.P("Select a province to see the average price", className="card-text")
    ])
], style={"marginTop": "20px"})
card_min_price = dbc.Card(id='card-min-price', children=[
    dbc.CardBody([
        html.P("Select a province to see the minimum price", className="card-text")
    ])
], style={"marginTop": "20px", "marginRight": "10px"})
card_max_price = dbc.Card(id='card-max-price', children=[
    dbc.CardBody([
        html.P("Select a province to see the maximum price", className="card-text")
    ])
], style={"marginTop": "20px", "marginLeft": "10px"})

# Assemble the widget layout
widget_layout = dbc.Row([
    dbc.Col(province_dropdown, width=3),
    dbc.Col(city_dropdown, width=3),
    dbc.Col(price_range_slider, width=6),
    dbc.Col(beds_numeric_input, width=2),
    dbc.Col(baths_numeric_input, width=2),
    dbc.Col(variable1_dropdown, width=2),
    dbc.Col(variable2_dropdown, width=2),
], className="mb-4")

# Define the layout with a cleaner structure
app.layout = dbc.Container(fluid=True, children=[
    html.Div([title]),
    dbc.Row([
        dbc.Col(card_avg_price, md=4, style={"marginBottom": "10px"}),
        dbc.Col(card_min_price, md=4, style={"marginBottom": "10px"}),
        dbc.Col(card_max_price, md=4, style={"marginBottom": "10px"})
    ]),

    widget_layout,
    dbc.Row([
        dbc.Col(dcc.Graph(id='output-graph-beds'), md=6),
        dbc.Col(dcc.Graph(id='output-graph-baths'), md=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='bar-graph'), md=12)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='map-graph'), md=12)
    ])
])

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

# Callbacks for updating plots
# Update beds scatter plot
@app.callback(
     Output('output-graph-beds', 'figure'),
    [Input('province-dropdown', 'value'),
     Input('city-dropdown', 'value'),
     Input('price-range-slider', 'value'),
     Input('beds-numeric-input', 'value')]
)

def update_beds_plot(province, cities, price_range, beds):
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
        (df['Number_Beds'] >= beds) 
    ]

    # If the filtered dataframe is empty, show an informative message
    if filtered_df.empty:
        return px.scatter(title="No listings match the selected criteria.")

    fig = px.scatter(
        filtered_df,
        x='Price',
        y='Number_Beds',
        color='City',
        hover_name='Address',
        log_x=True
    )
   
    return fig

# Update baths scatter plot
@app.callback(
     Output('output-graph-baths', 'figure'),
    [Input('province-dropdown', 'value'),
     Input('city-dropdown', 'value'),
     Input('price-range-slider', 'value'),
     Input('baths-numeric-input', 'value')]
)

def update_baths_plot(province, cities, price_range, baths):
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
        (df['Number_Baths'] >= baths)
    ]

    # If the filtered dataframe is empty, show an informative message
    if filtered_df.empty:
        return px.scatter(title="No listings match the selected criteria.")

    fig = px.scatter(
        filtered_df,
        x='Price',
        y='Number_Baths',
        color='City',
        hover_name='Address',
        log_x=True
    )
   
    return fig

# Update bar graph
@app.callback(
    Output('bar-graph', 'figure'),
    [Input('province-dropdown', 'value'),
     Input('city-dropdown', 'value'),
     Input('variable1-dropdown', 'value'),
     Input('variable2-dropdown', 'value')]
)


def update_bar_chart(province, cities, var1, var2):
    # If no city is selected, return an empty figure with a message
    if not cities:
        return {
            'layout': {
                'title': 'Please select at least one city.'
            }
        }

    # Ensure cities is always a list
    if isinstance(cities, str):
        cities = [cities]

    # Filter the DataFrame based on the province and cities selected
    df_filtered = df[(df['Province'] == province) & (df['City'].isin(cities))]

    # Group the data by City and calculate the mean of the selected variables
    df_grouped = df_filtered.groupby('City').agg({var1: 'mean'}).reset_index()

    # Create the bar chart
    fig = go.Figure()

    if var1 == var2:
        # If the two variables are the same, plot only one set of bars
        fig.add_trace(go.Bar(
            x=df_grouped['City'],
            y=df_grouped[var1],
            name=var1
        ))
    else:
        # If the two variables are different, plot two sets of bars
        df_grouped[var2] = df_filtered.groupby('City')[var2].mean().reset_index()[var2]
        fig.add_trace(go.Bar(
            x=df_grouped['City'],
            y=df_grouped[var1],
            name=var1
        ))
        fig.add_trace(go.Bar(
            x=df_grouped['City'],
            y=df_grouped[var2],
            name=var2
        ))

    # Update the layout of the bar chart
    fig.update_layout(
        title_text='Comparison of Variables',
        barmode='group',
        legend_title_text='Variable',
        xaxis_title='City',
        yaxis_title='Value',
        template='plotly_white'
    )

    return fig

# Update map graph
@app.callback(
    Output('map-graph', 'figure'),
    [Input('province-dropdown', 'value'),
     Input('city-dropdown', 'value')]
)

def update_map(province, cities):
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
    app.run_server(debug=True, host='127.0.0.1')
