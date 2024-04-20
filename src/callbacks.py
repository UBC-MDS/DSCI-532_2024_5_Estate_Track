from dash import Input, Output,callback, dcc, html, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from components import create_table
import numpy as np
import joblib
from data import df

memory = joblib.Memory("tmp", verbose=0)

# Callback to update city-dropdown options and values based on selected province
@callback(
    [Output('city-dropdown', 'options'),
     Output('city-dropdown', 'value')],
    [Input('province-dropdown', 'value')]
)
def update_city_dropdown(selected_province):
    unique_cities = sorted(df[df['Province'] == selected_province]['City'].unique())
    city_options = [{'label': city, 'value': city} for city in unique_cities]
    
    # Pre-select Vancouver if British Columbia is selected
    if unique_cities:
        city_value = [unique_cities[0], unique_cities[1]]
    else:
        city_value = []  # No cities are pre-selected if not British Columbia

    return city_options, city_value

# Update bar graph
@callback(
    Output('bar-graph-1', 'figure'),
    [Input('province-dropdown', 'value'),
     Input('city-dropdown', 'value'),
     Input('variable1-dropdown', 'value'),
     Input('variable2-dropdown', 'value')]
)
@memory.cache()
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
    df_grouped_samevar = df_filtered.groupby('City').agg({var1: 'mean'})

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    if var1 == var2:
        # If the two variables are the same, plot only one set of bars
        fig.add_trace(go.Bar(
            x=df_grouped_samevar.index,
            y=df_grouped_samevar[var1],
            text=df_grouped_samevar[var1],                # Add the income values as text
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
@callback(
    Output('bar-graph-2', 'figure'),
    [Input('province-dropdown', 'value'),
     Input('city-dropdown', 'value'),
     Input('variable3-dropdown', 'value')]
)
@memory.cache()
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

    color_seq = ['#98BDFF', '#F3797E', '#8B1FB6', '#1FB69F' , '#D0116D', '#601FB6']

    fig = px.bar(
        top_5_per_city,
        y=var3, 
        x='count',
        orientation='h',
        color='City',
        text=f"count",
        color_discrete_sequence=color_seq)

    # Update the layout of the bar chart
    fig.update_layout(title_text=f'Most Common Types {var3} in Selected Cities',
                      xaxis_title='Count',
                      yaxis_title=f'{var3}',
                      barmode='group')
    fig.update_traces(textposition='outside')

    return fig

# Update map graph
@callback(
    Output('map-graph', 'figure'),
    [Input('province-dropdown', 'value'),
     Input('city-dropdown', 'value')]
)

def update_map(province, selected_cities):
    # Selecting the province
    province_df = df[df['Province'] == province]

    # Ensure selected_cities is always a list
    if not isinstance(selected_cities, list):
        selected_cities = [selected_cities]

    # Filter only selected cities within the province
    province_df = province_df[province_df['City'].isin(selected_cities)]

    # If no city is selected, return an empty map with a message
    if province_df.empty:
        fig = go.Figure()
        fig.update_layout(title="No data available for the selected city/cities.")
        return fig

    # Get the latitude and longitude for centering the map
    center_lat = province_df['Latitude'].mean()
    center_lon = province_df['Longitude'].mean()

    # Calculate the average price for each selected city within the province
    city_avg_prices = province_df.groupby('City').agg({'Price': 'mean'}).reset_index()

    # Merge the average prices with the city locations
    city_avg_prices = city_avg_prices.merge(province_df[['City', 'Latitude', 'Longitude', 'Median Family Income']].drop_duplicates(),
                                            on='City',
                                            how='left')

    city_avg_prices.rename(columns={'Price': 'Avg_Price', "Median Family Income": "Median_Income"}, inplace=True)

    map_fig = px.scatter_mapbox(city_avg_prices,
                                lat="Latitude",
                                lon="Longitude",
                                color="City",
                                hover_data={"City": True,
                                            "Avg_Price": ':.2f',
                                            "Latitude": False,
                                            "Longitude": False,
                                            "Median_Income": True},
                                zoom=5,
                                center={"lat": center_lat, "lon": center_lon},
                                color_continuous_scale="RdYlGn_r")

    # Manually update marker sizes to reflect selected status without including in hover
    map_fig.update_traces(marker=dict(size=[9 if city in selected_cities else 2 for city in city_avg_prices['City']],
                                      sizemode='diameter'))

    map_fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r": 0, "t": 70, "l": 40, "b": 0},
        title={
            'text': f'Geospatial view of {province} House Prices',
            'y': 0.9,
            'x': 0.05,
            'xanchor': 'left',
            'yanchor': 'top'
        }
    )
    
    return map_fig

@callback(
        [
            Output("output-histogram", "figure"), 
            Output("card-avg-price", "children"),
            Output("card-avg-pop", "children"),
            Output("card-avg-income", "children"),
        ],
        [Input("province-dropdown", "value"), Input("city-dropdown", "value")],
    )

def update_histogram_and_price_cards(province, cities):
    filtered_df = df[df["Province"] == province]

    if isinstance(cities, str):
        cities = [cities]  # Ensure cities is a list
    filtered_df = filtered_df[filtered_df["City"].isin(cities)]
    # Prepare the figure
    fig = go.Figure()

    for city in cities:
        city_data = filtered_df[filtered_df['City'] == city]['Price']
        # Create a histogram with very fine bins
        hist_data = np.histogram(city_data, bins=200)
        hist_y = hist_data[0] / np.max(hist_data[0])  # Normalize histogram
        hist_x = (hist_data[1][1:] + hist_data[1][:-1]) / 2  # Midpoints of bins
        
        # Smooth the histogram using a moving average
        window_size = 5  # Increase for more smoothing
        window = np.ones(window_size) / window_size
        hist_y_smooth = np.convolve(hist_y, window, mode='same')
        
        # Add the smoothed line to the figure with area fill
        fig.add_trace(go.Scatter(
            x=hist_x, 
            y=hist_y_smooth, 
            fill='tozeroy', 
            mode='lines', 
            line_shape='spline', 
            name=city, 
            legendgroup=city
            
        ))

    # Update layout
    fig.update_layout(
        xaxis_title_text='Price',    
        legend_title_text='City',
        barmode='overlay',
        showlegend=True 
    )

    fig.update_layout(title_text=f'Comparison of House Prices in {province}')


    # Calculate statistics for price cards
    pop_avg = int(filtered_df["Population"].mean()) if not filtered_df.empty else "N/A"
    avg_price = int(filtered_df["Price"].mean()) if not filtered_df.empty else "N/A"
    income_avg = int(filtered_df["Median Family Income"].mean()) if not filtered_df.empty else "N/A"

    # Update card contents
    pop_card_content = dbc.CardBody(f"Average Population in Selected Cities: {pop_avg:,}", className="card-text")
    price_card_content = dbc.CardBody(f"Average Price in Selected Cities: ${avg_price:,}", className="card-text")
    income_card_content = dbc.CardBody(f"Average Income in Selected Cities: ${income_avg:,}", className="card-text")

    return fig, pop_card_content, price_card_content, income_card_content

@callback(
    Output('table-container', 'children'),
    Input('expert-toggle', 'on')
)
def toggle_table(toggle_on):
    if toggle_on:
        price_range_slider = html.Div([
            html.Label('Adjust Price Range of Table:'),
            dcc.RangeSlider(
                id='price-range-slider',
                min=int(df['Price'].min()),
                max=int(df['Price'].max()),
                step=1000000,
                value=[int(df['Price'].min()), int(df['Price'].max())],
                updatemode='drag'
            )
        ])
        table = create_table(df)
        # Return both the slider and table as children of the container Div
        return html.Div([price_range_slider, table])
    return None


@callback(
    Output('table', 'data'),
    [Input('price-range-slider', 'value')],
    State('table', 'data')  # Use State to keep the current table data intact unless the slider is adjusted
)

def update_table(price_range, existing_data):
    if price_range is None:
        # If the price range is not set, don't filter the data
        return existing_data
    # Filter the DataFrame based on the slider range
    filtered_df = df[(df['Price'] >= price_range[0]) & (df['Price'] <= price_range[1])]
    return filtered_df.to_dict('records')