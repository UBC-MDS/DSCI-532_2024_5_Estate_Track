import pandas as pd

df = pd.read_csv('data/raw/HouseListings.csv', encoding='latin-1')
df.rename(columns={'Number_Beds': 'Bedrooms', 
                    'Number_Baths': 'Bathrooms',
                    'Median_Family_Income': 'Median Family Income'}, inplace=True)