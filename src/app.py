from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import dash_daq as daq
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from components import province_dropdown, city_dropdown, card_avg_price, card_min_price, card_max_price,output_histogram, bar_plot_card_1, bar_plot_card_2, map_plot
import callbacks
import dash_vega_components as dvc
import altair as alt


# Initialize the Dash app with Bootstrap CSS
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
           title='HomeScope',
           suppress_callback_exceptions=True)

server = app.server

sidebar = dbc.Col([
    html.Img(src='/assets/logos/logo_main.png', className='img-fluid'),
    html.Br(),
    html.P(
        "HomeScope is a data analysis project aimed at providing stakeholders "
        "in the real estate industry with actionable insights derived from comprehensive "
        "analysis of key variables.",  # Description text
        className='text-muted'
    ),
    html.Br(),
    html.H3('Global controls'),  # Heading for the sidebar
    html.Br(),
    html.H5('Select Province'),  # Title for the province dropdown
    province_dropdown,
    html.Br(),
    html.H5('Select City'),  # Title for the city dropdown
    city_dropdown,
    html.Br() ,
    html.Br(),
    html.Br(),
    html.Div([
        html.P("Last Updated: 2024-04-15"),
        html.P("Made by: @Iris, @Aishwarya, @Carrie,  @Nasim"),
        html.P(html.A("Repo: HomeScope", href="https://github.com/UBC-MDS/DSCI-532_2024_5_HomeScope")),
    ], className="sidebar-footer"),
 
], className="sidebar")


# Define the layout with a cleaner structure
app.layout = dbc.Container(fluid=True, children=[
    # Two-column layout
    dbc.Row([
        # Left Column for filters and map with added spacing
        dbc.Col([
                sidebar
        ], md=3, style={'display': 'flex', 'flexDirection': 'column'}),  
        
        # Right Column for cards and graphs
        dbc.Col([
            # Row for Cards
            dbc.Row([
                dbc.Col(card_avg_price, md=4),
                dbc.Col(card_min_price, md=4),
                dbc.Col(card_max_price, md=4)
            ], className="mb-3"), 
            
            # Row for Bar Graph and Histogram
            dbc.Row([
                dbc.Col(output_histogram, md=6),
                dbc.Col(bar_plot_card_1, md=6)
            ], className="mb-3"),

            dbc.Row([
                dbc.Col(map_plot, md=6),
                dbc.Col(bar_plot_card_2, md=6)
            ], className="mb-3"),


        ], md=9),  
    ], align="stretch"),  
])  


# Run the Dash application
if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1')
