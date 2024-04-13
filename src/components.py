from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import dash_daq as daq
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data import df
import altair as alt
import dash_vega_components as dvc
import altair as alt
from vega_datasets import data



#Dropdowns for province, cities and variable 
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

output_histogram = dvc.Vega(id='output-histogram', spec={})

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