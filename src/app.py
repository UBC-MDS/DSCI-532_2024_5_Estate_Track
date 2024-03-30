from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Initialize the Dash app with Bootstrap CSS
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Read the CSV file
df = pd.read_csv('data/raw/HouseListings.csv', encoding='latin-1')

# Define layout
app.layout = html.Div([
    html.Div([
        html.H1('HomeScope', style={'color': '#2AAA8A', 'font-size': '3em', 'font-family': 'Arial', 'text-align': 'center'})
    ]),
    dbc.Row([
        dbc.Col([
            html.Label("Province"),
            dcc.Dropdown(
                id='province-dropdown',
                options=[{'label': province, 'value': province} for province in df['Province'].unique()],
                value=df['Province'].unique()[0]
            ),
            html.Label("City"),
            dcc.Dropdown(
                id='city-dropdown',
                options=[{'label': city, 'value': city} for city in df[df['Province'] == df['Province'].unique()[0]]['City'].unique()],
                value=df[df['Province'] == df['Province'].unique()[0]]['City'].unique()[0]
            ),
            html.Label("Price Range"),
            dcc.RangeSlider(
                id='price-range-slider',
                min=int(df['Price'].quantile(0.05)),
                max=int(df['Price'].quantile(0.95)),
                step=10000,
                value=[int(df['Price'].quantile(0.05)), int(df['Price'].quantile(0.95))],
            ),
            html.Label("Number of Beds"),
            dcc.Slider(
                id='beds-slider',
                min=1,
                max=10,
                step=1,
                value=1,
            ),
            html.Label("Number of Baths"),
            dcc.Slider(
                id='baths-slider',
                min=1,
                max=10,
                step=1,
                value=1,
            )
        ], md=3),
        dbc.Col([
            dcc.Graph(id='output-graph')
        ])
    ])
])

# Define callback to update output graph
@app.callback(
    Output('output-graph', 'figure'),
    [
        Input('province-dropdown', 'value'),
        Input('city-dropdown', 'value'),
        Input('price-range-slider', 'value'),
        Input('beds-slider', 'value'),
        Input('baths-slider', 'value')
    ]
)
def update_output_graph(province, city, price_range, beds, baths):
    filtered_df = df[
        (df['Province'] == province) &
        (df['City'] == city) &
        (df['Price'] >= price_range[0]) &
        (df['Price'] <= price_range[1]) &
        (df['Number_Beds'] >= beds) &
        (df['Number_Baths'] >= baths)
    ]
    fig = px.scatter(filtered_df, x='Price', y='Number_Beds', color='City', hover_data=['Address'])
    return fig

# Run the Dash application
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
