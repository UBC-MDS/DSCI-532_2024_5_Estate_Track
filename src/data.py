import pandas as pd

df = pd.read_parquet('../data/processed/HouseListings.parquet')
df.rename(columns={'Number_Beds': 'Bedrooms', 
                    'Number_Baths': 'Bathrooms',
                    'Median_Family_Income': 'Median Family Income'}, inplace=True)