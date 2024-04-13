from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import dash_daq as daq
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from components import province_dropdown, city_dropdown, variable1_dropdown, variable2_dropdown, variable3_dropdown, card_avg_price, card_min_price, card_max_price,output_histogram
import callbacks
import altair as alt
import dash_vega_components as dvc
import altair as alt
from vega_datasets import data

# Initialize the Dash app with Bootstrap CSS
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Components with added labels using dbc.Row and dbc.Col
title = html.H1('HomeScope', style={'color': '#2AAA8A', 'font-size': '3em', 'font-family': 'Arial', 'text-align': 'center'})

# Assemble the widget layout
widget_layout = dbc.Row([
    dbc.Col(province_dropdown, width=3),
    dbc.Col(city_dropdown, width=3),
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
            
            # Row for Bar Graph and Histogram
            dbc.Row([
                dbc.Col(dcc.Graph(id='bar-graph-1'), md=6),
                dbc.Col(output_histogram, md=6)
            ], className="mb-3"),
            dbc.Row(dcc.Graph(id='bar-graph-2'))
        ], md=8),  # Adjust the width as per your design
    ], className="mb-5"),  # Add margin at the bottom of the row
], className="mt-5")  # Add margin at the top of the container


# Run the Dash application
if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1')
