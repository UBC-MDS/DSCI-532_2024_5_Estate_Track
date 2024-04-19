from dash import html, dcc
import dash_bootstrap_components as dbc
from dash import dash_table
import dash_daq as daq
from data import df



#Dropdowns for province, cities and variable 
province_dropdown = dcc.Dropdown(
        id='province-dropdown',
        options=[{'label': province, 'value': province} for province in sorted(df['Province'].unique())],
        value='British Columbia'
    )

city_dropdown = dcc.Dropdown(
        id='city-dropdown',
        multi=True
    )

variable1_dropdown = dcc.Dropdown(
        id='variable1-dropdown',
        options=[feature for feature in df[['Price','Bedrooms', 'Bathrooms','Population','Median Family Income' ]]],
        value='Price',
        style={'width': '95%', 'margin-left': '20px'}
    )

variable2_dropdown = dcc.Dropdown(
        id='variable2-dropdown',
        options=[feature for feature in df[['Price','Bedrooms', 'Bathrooms','Population','Median Family Income'  ]]],
        value='Median Family Income',
        style={'width': '95%','margin-left': '20px'}
    )

variable3_dropdown = dcc.Dropdown(
        id='variable3-dropdown',
        options=[feature for feature in df[['Bedrooms', 'Bathrooms']]],
        value='Bedrooms',
        style={'width': '83%', 'margin-left': '38px'}
    )

# Card for displaying the minimum price dynamically
card_avg_price = dbc.Card(
    id='card-avg-price', 
    children=[
        dbc.CardBody([
            html.P("Select a province to see the average price", className="card-text")
        ])
    ],
    className="card-avg-price"  
)

# Card for displaying the average price dynamically
card_avg_pop = dbc.Card(
    id='card-avg-pop',
    children=[
        dbc.CardBody([
            html.P("Select a province to see the average population", className="card-text")
        ])
    ],
    className="card-avg-pop"  
)

# Card for displaying the maximum price dynamically
card_avg_income = dbc.Card(
    id='card-avg-income', 
    children=[
        dbc.CardBody([
            html.P("Select a province to see the median income", className="card-text")
        ])
    ],
    className="card-avg-income"  
)

#bar plot of numeric column
bar_plot_1 = dcc.Graph(id='bar-graph-1')

#bar plot1 add two dropdown
bar_plot_card_1 = dbc.Card(
    dbc.CardBody([
        dbc.Row([
            dbc.Col(variable1_dropdown, md=6), 
            dbc.Col(variable2_dropdown, md=6)  
        ]),
        bar_plot_1  
    ]),
    style={"border": "none", "boxShadow": "none"}
)

# Expert mode toggle switch
expert_toggle = daq.BooleanSwitch(
    id='expert-toggle',
    on=False,
    label={'label': 'Expert Mode', 'style': {'color': 'white', 'font-weight': 'bold'}},
    color='#72b7b2'
)

sidebar = dbc.Col([
    html.Div([
        html.Img(src='/assets/logos/logo_main.png', className='img-fluid'),
        html.P(
            "Welcome to HomeScope, the gateway to actionable insights in real estate. Dive deep into key data and empower your decisions with our comprehensive analysis tool.",
            className='text-muted', style={'margin-bottom': '0px', 'padding-bottom': '0px'}
        ),
        html.Br(),
        html.Br(),
        html.H3('Global controls'),
        html.Br(),
        html.H5('Select Province'),
        province_dropdown,
        html.Br(),
        html.H5('Select City'),
        city_dropdown,
        html.Br(),
        html.Br(),
        expert_toggle,
    ], style={'flex': '1'}),  # This makes the div grow to take available space, pushing the footer down
    
    html.Div([
        html.P("Last Updated: 2024-04-20"),
        html.P("Made by: @Iris, @Aishwarya, @Carrie,  @Nasim"),
        html.P(html.A("Repo: HomeScope", href="https://github.com/UBC-MDS/DSCI-532_2024_5_HomeScope")),
    ], className="sidebar-footer"),
], style={'display': 'flex', 'flex-direction': 'column', 'height': '100vh'}, className="sidebar")


#histogram plot of price
output_histogram = dcc.Graph(id='output-histogram')

#map plot
map_plot = dcc.Graph(id='map-graph')

#bar plot of bedrooms and bathrooms
bar_plot_2 = dcc.Graph(id='bar-graph-2')

#bar plot2 add one dropdown
bar_plot_card_2 = dbc.Card([
    dbc.CardBody([
        variable3_dropdown,
        bar_plot_2
    ])
],
style={"border": "none", "boxShadow": "none"} 
)

#a table to show data in detail
def create_table(df):
    return dash_table.DataTable(
        id='table',
        data=df.to_dict('records'),
        columns=[{"name": col.replace('_', ' '), "id": col} for col in df.columns],
        page_size=10,
        sort_action='native',
        filter_action='native'
    )