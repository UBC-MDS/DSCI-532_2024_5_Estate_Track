from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import dash_daq as daq
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Initialize the Dash app with Bootstrap CSS
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Read the CSV file
df = pd.read_csv('data/raw/HouseListings.csv', encoding='latin-1')
df.rename(columns={'Number_Beds': 'Bedrooms', 
                    'Number_Baths': 'Bathrooms',
                    'Median_Family_Income': 'Median Family Income'}, inplace=True)

# Dropdown options for variable1 and variable2
variable_options = [{'label': col, 'value': col} for col in ['Price', 'Bathrooms', 'Bedrooms', 'Population', 'Median Family Income']]

# Components with added labels using dbc.Row and dbc.Col
title = html.H1('HomeScope', style={'color': '#2AAA8A', 'font-size': '3em', 'font-family': 'Arial', 'text-align': 'center'})

province_dropdown = dbc.Row([
    dbc.Col(html.Label("Province", className='form-label'), width=2),
    dbc.Col(dcc.Dropdown(
        id='province-dropdown',
        options=[{'label': province, 'value': province} for province in sorted(df['Province'].unique())],
        value='British Columbia'
    ), width=10)
], className="mb-3")

city_dropdown = dbc.Row([
    dbc.Col(html.Label("City", className='form-label'), width=2),
    dbc.Col(dcc.Dropdown(
        id='city-dropdown',
        multi=True
    ), width=10)
], className="mb-3")

price_range_slider = dbc.Row([
    dbc.Col(html.Label("Price Range", className='form-label'), width=2),
    dbc.Col(dcc.RangeSlider(
        id='price-range-slider',
        min=int(df['Price'].min()),
        max=int(df['Price'].max()),
        step=10000000,
        value=[int(df['Price'].min()), int(df['Price'].max())],
        updatemode='drag'
    ), width=10)
], className="mb-3")

beds_numeric_input = daq.NumericInput(id='beds-numeric-input', label='Number of Beds', labelPosition='top', min=0, max=109, value=3,style={'justify':'left'})
baths_numeric_input = daq.NumericInput(id='baths-numeric-input', label='Number of Baths', labelPosition='top', min=0, max=59, value=2)

variable1_dropdown = dbc.Row([
    dbc.Col(html.Label("Bar Plot First Variable", className='form-label'), width=2),
    dbc.Col(dcc.Dropdown(
        id='variable1-dropdown',
        options=[feature for feature in df[['Price','Bedrooms', 'Bathrooms','Population','Median Family Income' ]]],
        value='Price'
    ), width=10)
], className="mb-3")

variable2_dropdown = dbc.Row([
    dbc.Col(html.Label("Bar Plot Second Variable", className='form-label'), width=2),
    dbc.Col(dcc.Dropdown(
        id='variable2-dropdown',
        options=[feature for feature in df[['Price','Bedrooms', 'Bathrooms','Population','Median Family Income'  ]]],
        value='Median Family Income'
    ), width=10)
], className="mb-3")

variable3_dropdown = dbc.Row([
    dbc.Col(html.Label("Bar Plot Third Variable", className='form-label'), width=2),
    dbc.Col(dcc.Dropdown(
        id='variable3-dropdown',
        options=[feature for feature in df[['Bedrooms', 'Bathrooms']]],
        value='Bedrooms'
    ), width=10)
], className="mb-3")

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
    # Title centered and styled
    dbc.Row(dbc.Col(html.H1("HomeScope", style={'color': '#2AAA8A', 'textAlign': 'center'}), md=12)),

    # Two-column layout
    dbc.Row([
        # Left Column for filters and map with added spacing
        dbc.Col([
            # Province and City dropdowns with additional vertical space
            dbc.Row([
                dbc.Col(province_dropdown, md=12, className="mb-4"),  # Increase bottom margin for spacing
                dbc.Col(city_dropdown, md=12, className="mb-4")  # Increase bottom margin for spacing
            ]),
            
            # Price Range Slider with more vertical space
            dbc.Row(dbc.Col(price_range_slider, md=12, className="mb-4")),

            # Numeric Inputs for Beds and Baths in separate rows for more space
            dbc.Row([
                dbc.Col(beds_numeric_input, md=6, className="mb-4"),  # Adjusted to half-width columns within the same row
                dbc.Col(baths_numeric_input, md=6, className="mb-4")   # Adjusted to half-width columns within the same row
            ]),

            # Variable Dropdowns in separate rows for more spacing
            dbc.Row(dbc.Col(variable1_dropdown, md=12, className="mb-4")),
            dbc.Row(dbc.Col(variable2_dropdown, md=12, className="mb-4")),
            dbc.Row(dbc.Col(variable3_dropdown, md=12, className="mb-4")),

            # Map Graph spans full width of the column with additional space
            dbc.Row(dbc.Col(dcc.Graph(id='map-graph'), md=12, className="mb-4")),
        ], md=4),  
        
        # Right Column for cards and graphs
        dbc.Col([
            # Row for Cards
            dbc.Row([
                dbc.Col(card_avg_price, md=4),
                dbc.Col(card_min_price, md=4),
                dbc.Col(card_max_price, md=4)
            ], className="mb-3"),  # Add margin at the bottom of the row
            
            # Row for Scatter Plots
            dbc.Row([
                dbc.Col(dcc.Graph(id='output-graph-beds'), md=6),
                dbc.Col(dcc.Graph(id='output-graph-baths'), md=6)
            ], className="mb-5"),
            
            # Row for Bar Graph and Histogram
            dbc.Row([
                dbc.Col(dcc.Graph(id='bar-graph-1'), md=6),
                dbc.Col(output_histogram, md=6)
            ], className="mb-3"),
            dbc.Row(dcc.Graph(id='bar-graph-2'))
        ], md=8),  # Adjust the width as per your design
    ], className="mb-5"),  # Add margin at the bottom of the row
], className="mt-5")  # Add margin at the top of the container




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
        title = 'Price-Bedroom Correlation',
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
        (df['Bathrooms'] >= baths)
    ]

    # If the filtered dataframe is empty, show an informative message
    if filtered_df.empty:
        return px.scatter(title="No listings match the selected criteria.")

    fig = px.scatter(
        filtered_df,
        title = 'Price-Bathroom Correlation',
        x='Price',
        y='Bathrooms',
        color='City',
        hover_name='Address',
        log_x=True
    )
   
    return fig

# Update bar graph
@app.callback(
    Output('bar-graph-1', 'figure'),
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
    df_grouped = df_filtered.groupby('City')[[var1,var2]].mean()

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    if var1 == var2:
        # If the two variables are the same, plot only one set of bars
        fig.add_trace(go.Bar(
            x=df_grouped.index,
            y=df_grouped[var1],
            text=df_grouped[var1],                # Add the income values as text
            textposition='auto',              # Position the text automatically
            texttemplate='%{text:.2s}',
            name=f'{var1}',
            marker_color='#F3797E'))
    else:
        # If the two variables are different, plot two sets of bars
        fig.add_trace(go.Bar(
            x=df_grouped.index,
            y=df_grouped[var1],
            text=df_grouped[var1],                # Add the income values as text
            textposition='auto',              # Position the text automatically
            texttemplate='%{text:.2s}',
            name=f'{var1}',
            marker_color='#F3797E',
            offsetgroup=1),
            secondary_y=False
        )
    
        # Add bar 2 for var 2
        fig.add_trace(go.Bar(
            x=df_grouped.index,
            y=df_grouped[var2],
            text=df_grouped[var2],  
            textposition='auto',             
            texttemplate='%{text:.2s}',
            name=f'{var2}',
            marker_color='#7978E9',
            offsetgroup=2),
            secondary_y=True,
        )

    # Update the layout of the bar chart
    fig.update_layout(title_text=f'Comparison of {var1} and {var2}',
                     barmode='group')
    fig.update_yaxes(title_text=f'{var1}', secondary_y=False)
    fig.update_yaxes(title_text=f'{var2}', secondary_y=True)

    return fig

# Update bar graph 2
@app.callback(
    Output('bar-graph-2', 'figure'),
    [Input('province-dropdown', 'value'),
     Input('city-dropdown', 'value'),
     Input('variable3-dropdown', 'value')]
)
def update_bar_chart(province, cities, var3):
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
    df_count = df_filtered.groupby('City')[[var3]].value_counts().reset_index()
    top_5_per_city = (df_count.sort_values(['City', 'count'], ascending=[True, False])
                                 .groupby('City')
                                 .head(5))

    color_seq = ['#98BDFF','#F3797E','#7DA0FA', '#7978E9', '#4B49AC']

    fig = px.bar(
        y=top_5_per_city[var3], 
        x=top_5_per_city['count'],
        orientation='h',
        color=top_5_per_city['City'],
        text=top_5_per_city['count'],
        color_discrete_sequence=color_seq)

    # Update the layout of the bar chart
    fig.update_layout(title_text=f'Top 5 {var3} Counts Across Cities',
                      xaxis_title='Count',
                      yaxis_title=f'{var3}',
                      barmode='group')
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
    city_avg_prices = city_avg_prices.merge(province_df[['City', 'Latitude', 'Longitude','Median Family Income']].drop_duplicates(),
                                            on='City', 
                                            how='left')
    city_avg_prices.rename(columns={'Price': 'Avg_Price', "Median Family Income":"Median_Income"}, inplace=True)
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

@app.callback(
    [Output('output-histogram', 'figure'),
     Output('card-avg-price', 'children'),
     Output('card-min-price', 'children'),
     Output('card-max-price', 'children')],
    [Input('province-dropdown', 'value')]
)
def update_histogram_and_price_cards(province):
    filtered_df = df[df['Province'] == province]
    
    # Histogram
    histogram_fig = px.histogram(filtered_df, x='Price',
                                 title=f'Price Distribution in {province}',
                                 labels={'Price': 'Real Estate Price (CAD)'},
                                 nbins=50)
    histogram_fig.update_layout(yaxis_title='Count of Listings', bargap=0.2)
    
    # Statistics
    avg_price = filtered_df['Price'].mean() if not filtered_df.empty else 0
    min_price = filtered_df['Price'].min() if not filtered_df.empty else 0
    max_price = filtered_df['Price'].max() if not filtered_df.empty else 0
    
    # Update card contents
    avg_card_content = [dbc.CardHeader("Average Price"), dbc.CardBody(f"${avg_price:,.2f}")]
    min_card_content = [dbc.CardHeader("Minimum Price"), dbc.CardBody(f"${min_price:,.2f}")]
    max_card_content = [dbc.CardHeader("Maximum Price"), dbc.CardBody(f"${max_price:,.2f}")]
    
    return histogram_fig, avg_card_content, min_card_content, max_card_content


# Run the Dash application
if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1')
