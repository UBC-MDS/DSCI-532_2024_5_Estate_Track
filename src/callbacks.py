from dash import Dash, html, dcc, Input, Output,callback
import dash_bootstrap_components as dbc
import plotly.express as px
import dash_daq as daq
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import altair as alt
import dash_vega_components as dvc
import altair as alt
from vega_datasets import data
import numpy as np


from data import df

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
        city_value = unique_cities[0]
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
@callback(
    Output('map-graph', 'figure'),
    [Input('province-dropdown', 'value'),
     Input('city-dropdown', 'value')]
)

def update_map(province, cities):
    # Selecting the province and setting up latitude and longitudes

    province_df = df[df['Province'] == province]
    first_city = province_df['City'].dropna().sort_values().iloc[0]

    # Get the latitude and longitude of the first city
    first_city_data = province_df[province_df['City'] == first_city]
    avg_lat = first_city_data['Latitude'].iloc[0]
    avg_lon = first_city_data['Longitude'].iloc[0]

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
                                zoom=5,
                                center={"lat": avg_lat, "lon": avg_lon},
                                color_continuous_scale="RdYlGn_r")
    map_fig.update_layout(
    mapbox_style="open-street-map",
    margin={"r": 0, "t": 70, "l": 40, "b": 0},
    title={
         'text': f'Geospatial view of {province} House Prices',
         'y':0.9,
         'x':0.05,
         'xanchor': 'left',
         'yanchor': 'top'
     },
    barmode='group'
)
    
    return map_fig

@callback(
        [
            Output("output-histogram", "figure"), 
            Output("card-min-price", "children"),
            Output("card-avg-price", "children"),
            Output("card-max-price", "children"),
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
            name=f'{city}', 
            legendgroup=city
        ))

    # Update layout
    fig.update_layout(
        xaxis_title_text='Price',  # X-axis label
        yaxis_title_text='Relative Frequency / Density',  # Y-axis label
        legend_title_text='City',
        barmode='overlay'  # Overlay the histograms
    )

    fig.update_layout(title_text=f'Comparison of House Prices in {province}')


    # Calculate statistics for price cards
    min_price = filtered_df["Price"].min() if not filtered_df.empty else "N/A"
    avg_price = filtered_df["Price"].mean() if not filtered_df.empty else "N/A"
    max_price = filtered_df["Price"].max() if not filtered_df.empty else "N/A"

    # Update card contents
    min_card_content = dbc.CardBody(f"Minimum Price: ${min_price:,.2f}", className="card-text")
    avg_card_content = dbc.CardBody(f"Average Price: ${avg_price:,.2f}", className="card-text")
    max_card_content = dbc.CardBody(f"Maximum Price: ${max_price:,.2f}", className="card-text")

    return fig, avg_card_content, min_card_content, max_card_content
