from dash import Dash
import dash_bootstrap_components as dbc
from components import sidebar, card_avg_price, card_min_price, card_max_price,output_histogram, bar_plot_card_1, bar_plot_card_2, map_plot
import callbacks

# Initialize the Dash app with Bootstrap CSS
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
           title='HomeScope',
           suppress_callback_exceptions=True)

server = app.server

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
