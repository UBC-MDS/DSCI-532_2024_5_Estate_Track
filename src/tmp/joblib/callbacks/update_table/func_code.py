# first line: 319
@callback(
    Output('table', 'data'),
    [Input('price-range-slider', 'value')],
    State('table', 'data')  # Use State to keep the current table data intact unless the slider is adjusted
)
@memory.cache()
def update_table(price_range, existing_data):
    import time
    time.sleep(1)
    if price_range is None:
        # If the price range is not set, don't filter the data
        return existing_data
    # Filter the DataFrame based on the slider range
    filtered_df = df[(df['Price'] >= price_range[0]) & (df['Price'] <= price_range[1])]
    return filtered_df.to_dict('records')