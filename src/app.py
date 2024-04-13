from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import dash_daq as daq
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from components import province_dropdown, city_dropdown, variable3_dropdown, card_avg_price, card_min_price, card_max_price,output_histogram, bar_plot_card_1, bar_plot_card_2, map_plot
import callbacks
import altair as alt
import dash_vega_components as dvc
import altair as alt
from vega_datasets import data

# Initialize the Dash app with Bootstrap CSS
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Define the layout with a cleaner structure
app.layout = dbc.Container(fluid=True, children=[
    # Two-column layout
    dbc.Row([
        # Left Column for filters and map with added spacing
        dbc.Col([
            # Province and City dropdowns with additional vertical space

            dbc.Col(province_dropdown, md=12, className="mb-4"),  # Increase bottom margin for spacing
            dbc.Col(city_dropdown, md=12, className="mb-4"),  # Increase bottom margin for spacing
        ], md=3),  
        
        # Right Column for cards and graphs
        dbc.Col([
            # Row for Cards
            dbc.Row([
                dbc.Col(card_avg_price, md=4),
                dbc.Col(card_min_price, md=4),
                dbc.Col(card_max_price, md=4)
            ], className="mb-3"),  # Add margin at the bottom of the row
            
            # Row for Bar Graph and Histogram
            dbc.Row([
                dbc.Col(bar_plot_card_1, md=6),
                dbc.Col(output_histogram, md=6)
            ], className="mb-3"),

            dbc.Row([
                dbc.Col(map_plot, md=6),
                dbc.Col(bar_plot_card_2, md=6)
            ], className="mb-3"),


        ], md=9),  # Adjust the width as per your design
    ], className="mb-5"),  # Add margin at the bottom of the row
], className="mt-5")  # Add margin at the top of the container


# Run the Dash application
if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1')
