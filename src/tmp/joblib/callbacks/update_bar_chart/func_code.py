# first line: 31
@callback(
    Output('bar-graph-1', 'figure'),
    [Input('province-dropdown', 'value'),
     Input('city-dropdown', 'value'),
     Input('variable1-dropdown', 'value'),
     Input('variable2-dropdown', 'value')]
)
@memory.cache()
def update_bar_chart(province, cities, var1, var2):
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
    df_grouped = df_filtered.groupby('City')[[var1,var2]].mean()
    df_grouped_samevar = df_filtered.groupby('City').agg({var1: 'mean'})

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    if var1 == var2:
        # If the two variables are the same, plot only one set of bars
        fig.add_trace(go.Bar(
            x=df_grouped_samevar.index,
            y=df_grouped_samevar[var1],
            text=df_grouped_samevar[var1],                # Add the income values as text
            textposition='auto',              # Position the text automatically
            texttemplate='%{text:.2s}',
            name=f'{var1}',
            marker_color='#F3797E'))
    else:
        # If the two variables are different, plot two sets of bars
        fig.add_trace(go.Bar(
            x=df_grouped.index,
            y=df_grouped[var1],
            text=df_grouped[var1],                # Add the income values as text
            textposition='auto',              # Position the text automatically
            texttemplate='%{text:.2s}',
            name=f'{var1}',
            marker_color='#F3797E',
            offsetgroup=1),
            secondary_y=False
        )
    
        # Add bar 2 for var 2
        fig.add_trace(go.Bar(
            x=df_grouped.index,
            y=df_grouped[var2],
            text=df_grouped[var2],  
            textposition='auto',             
            texttemplate='%{text:.2s}',
            name=f'{var2}',
            marker_color='#7978E9',
            offsetgroup=2),
            secondary_y=True,
        )

    # Update the layout of the bar chart
    fig.update_layout(title_text=f'Comparison of {var1} and {var2}',
                     barmode='group')
    fig.update_yaxes(title_text=f'{var1}', secondary_y=False)
    fig.update_yaxes(title_text=f'{var2}', secondary_y=True)

    return fig
