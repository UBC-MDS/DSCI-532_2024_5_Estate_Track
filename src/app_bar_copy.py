from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import pandas as pd
import plotly.express as px
import altair as alt
import plotly.graph_objects as go
alt.data_transformers.enable("vegafusion")
from plotly.subplots import make_subplots


# Initialize the Dash app with Bootstrap CSS
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Read the CSV file
df = pd.read_csv('data/raw/HouseListings.csv', encoding='latin-1')

# Components
province_dropdown = dcc.Dropdown(
    id='province-dropdown',
    options=[{'label': province, 'value': province} for province in sorted(df['Province'].unique())],
    value='British Columbia'  # Changed from sorted(df['Province'].unique())[0]
)

city_dropdown = dcc.Dropdown(
    id='city-dropdown',
    multi = True
) 

variable1_dropdown = dcc.Dropdown(
    id='variable1-dropdown',
    options=[var for var in df[['Price','Number_Beds', 'Number_Baths','Population','Median_Family_Income' ]]],
    value='Price' 
)
variable2_dropdown = dcc.Dropdown(
    id='variable2-dropdown',
    options=[var for var in df[['Price','Number_Beds', 'Number_Baths','Population','Median_Family_Income' ]]],
    value='Median_Family_Income' 
)

bar_graph = dcc.Graph(id='bar-graph')

global_widgets = [
    dbc.Label("Province"),
    province_dropdown,
    html.Br(),
    dbc.Label("City"),
    city_dropdown,
    html.Br(),
    dbc.Label("Attribute 1"),
    variable1_dropdown,
    html.Br(),
    dbc.Label("Attribute 2"),
    variable2_dropdown,
    html.Br()]

# Layout
app.layout = dbc.Container([
    # dbc.Row(dbc.Col(title)),
    dbc.Row([
        dbc.Col(global_widgets, md=4),
        dbc.Col(bar_graph, md=8),
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
    if selected_province == 'British Columbia':
        city_value = ['Vancouver']
    else:
        city_value = []  # No cities are pre-selected if not British Columbia

    return city_options, city_value


# Callback to update output graph based on selected filters
@app.callback(
    Output('bar-graph', 'figure'),
    [Input('province-dropdown', 'value'),
     Input('city-dropdown', 'value'),
     Input('variable1-dropdown', 'value'),
     Input('variable2-dropdown', 'value')]
)
def grouped_bar_chart(province, cities, var1, var2):
    if not cities:  # This checks both for None and for an empty list
        return go.Bar(title="Please select at least one city.")
    
    if isinstance(cities, str):
        cities = [cities]  # Wrap string in list if it's not a list already

    df_province = df[(df['Province'] == province)]
    df_city = df_province[df_province['City'].isin(cities)]
    df_var = df_city.groupby('City')[[var1,var2]].mean()

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add bar 1 for var 1
    fig.add_trace(go.Bar(
        x=df_var.index,
        y=df_var[var1],
        text=df_var[var1],                # Add the income values as text
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

    fig.update_layout(title_text=f'Comparison of {var1} and {var2}',
                     barmode='group')
    fig.update_yaxes(title_text=f'{var1}', secondary_y=False)
    fig.update_yaxes(title_text=f'{var2}', secondary_y=True)
    
    # Show the figure
    # fig.show()
    return fig

# grouped_bar_chart(df_var, var1, var2)
# app.run_server(host='127.0.0.1', port=8050, debug=True)
# Run the Dash application
if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1')
