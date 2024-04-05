from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import pandas as pd
import plotly.express as px
import altair as alt
import plotly.graph_objects as go
alt.data_transformers.enable("vegafusion")

# Initialize the Dash app with Bootstrap CSS
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Read the CSV file
df = pd.read_csv('../data/raw/HouseListings.csv', encoding='latin-1')

City1 = "Toronto"
City2 = "Vancouver"
city_list = [City1, City2]
city_list

# df_city = df.query('City == "Toronto" | City == "Vancouver"')
df_city = df[df['City'].isin(city_list)]
var1 = 'Price'
var2 = 'Population'
df_var = df_city.groupby('City')[[var1,var2]].mean()
df_var

# +
from plotly.subplots import make_subplots

def grouped_bar_chart(df_var, var1, var2):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add bar 1 for var 1
    fig.add_trace(go.Bar(
        x=df_var.index,
        y=df_var[var1],
        text=df_var[var1],  # Add the income values as text
        textposition='auto',              # Position the text automatically
        texttemplate='%{text:.2s}',
        name=f'{var1}',
        marker_color='indianred',
        offsetgroup=1),
        secondary_y=False
    )
    
    # Add bar 2 for var 2
    fig.add_trace(go.Bar(
        x=df_var.index,
        y=df_var[var2],
        text=df_var[var2],  
        textposition='auto',             
        texttemplate='%{text:.2s}',
        name=f'{var2}',
        marker_color='lightsalmon',
        offsetgroup=2),
        secondary_y=True,
    )

    fig.update_layout(title_text=f'Bar Chart Comparison of {var1} and {var2}',
                     barmode='group')
    fig.update_yaxes(title_text=f'{var1}', secondary_y=False)
    fig.update_yaxes(title_text=f'{var2}', secondary_y=True)
    
    # Show the figure
    fig.show()

grouped_bar_chart(df_var, var1, var2)
# -



# Components
title = [html.H1('HomeScope', style={'color': '#2AAA8A', 'font-size': '3em', 'font-family': 'Arial', 'text-align': 'center'}), html.Br()]
province_dropdown = dcc.Dropdown(
    id='province-dropdown',
    options=[{'label': province, 'value': province} for province in sorted(df['Province'].unique())],
    value='British Columbia'  # Changed from sorted(df['Province'].unique())[0]
)

# Layout
app.layout = dbc.Container([
    dbc.Row(dbc.Col(title)),
    dbc.Row([dvc.Vega(id='bar', spec={}),
            dcc.Dropdown(id='y-col', options=df.columns, value='Population'),
            dcc.Dropdown(id='city-dropdown', options=df['City'].unique(), value='City')])
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
    if selected_province == 'British Columbia':
        city_value = ['Vancouver']
    else:
        city_value = []  # No cities are pre-selected if not British Columbia

    return city_options, city_value


@app.callback(
    Output('output-graph', 'figure'),
    [Input('province-dropdown', 'value'),
     Input('city-dropdown', 'value'),
     Input('y-col', 'value')])

def chart(city-dropdown, y_col):
    fig = px.bar(df, x=city-dropdown, y = y_col)
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    return fig

# def chart(city, y_col):
#     return(alt.Chart(df).mark_bar().encode(
#         x = city,
#         y = y_col,
#         tooltip = city
#     ).interactive().todict()
#     )

# Run the Dash application
if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1')
