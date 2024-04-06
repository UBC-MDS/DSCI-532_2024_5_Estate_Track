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
output_histogram = dcc.Graph(id='output-histogram')


# Card for displaying the average price dynamically
card_avg_price = dbc.Card(id='card-avg-price', children=[
    dbc.CardBody([
        html.P("Select a province to see the average price", className="card-text")
    ])
], style={"marginTop": "20px"})
# Additional card components for Min and Max Prices
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
        dbc.Col(card_avg_price, md=4, style={"marginBottom": "10px"}),
        dbc.Col(card_min_price, md=4, style={"marginBottom": "10px"}),
        dbc.Col(card_max_price, md=4, style={"marginBottom": "10px"})
    ]),
    dbc.Row([
        dbc.Col(output_histogram, md=12),
    ]),
    dbc.Row([
        dbc.Col(global_widgets, md=4),
        dbc.Col(output_graph, md=8)
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
    if selected_province == 'British Columbia':
        city_value = ['Vancouver']
    else:
        city_value = []  # No cities are pre-selected if not British Columbia

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

def run_real_estate_dash_app(df, title='Real Estate Price Distribution'):
    """
    Initializes and runs a Dash app to display the count of real estate listings per price range, split by province.

    Parameters:
    - df: pandas.DataFrame, the data frame containing 'Province' and 'Price' columns.
    - title: str, the title of the graph.
    """
    # Visualization
    fig = px.histogram(df, x='Price', color='Province', barmode='group',
                    histfunc='count', title=title)
    fig.update_layout(xaxis_title='Real Estate Price (CAD)',
                    yaxis_title='Count of Listings',
                    bargap=0.2)
    return (fig)

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
    app.run_server(debug=False, host='127.0.0.1')
