# first line: 110
@callback(
    Output('bar-graph-2', 'figure'),
    [Input('province-dropdown', 'value'),
     Input('city-dropdown', 'value'),
     Input('variable3-dropdown', 'value')]
)
@memory.cache()
def update_bar_chart(province, cities, var3):
    import time
    time.sleep(2)
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

    color_seq = ['#98BDFF', '#F3797E', '#8B1FB6', '#1FB69F' , '#D0116D', '#601FB6']

    fig = px.bar(
        top_5_per_city,
        y=var3, 
        x='count',
        orientation='h',
        color='City',
        text=f"count",
        color_discrete_sequence=color_seq)

    # Update the layout of the bar chart
    fig.update_layout(title_text=f'Most Common Types {var3} in Selected Cities',
                      xaxis_title='Count',
                      yaxis_title=f'{var3}',
                      barmode='group')
    fig.update_traces(textposition='outside')

    return fig
