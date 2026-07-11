import pandas as pd
import numpy as np

# Load the dataset
phones_df = pd.read_csv('phones.csv')

# Find 5 phones whose price is closest to 500
def find_closest_to_500(df, target_price=500, n=5):
    # Calculate the absolute difference between each phone's price and the target price
    df['Price_Difference'] = np.abs(df['Price'] - target_price)
    
    # Sort by the price difference and select the top n rows
    closest_phones = df.sort_values(by='Price_Difference').head(n)
    
    # Drop the helper column before returning
    closest_phones = closest_phones.drop(columns=['Price_Difference'])
    return closest_phones

# Get the 5 phones closest to $500
closest_phones = find_closest_to_500(phones_df)

# Print the result
print("5 Phones Closest to $500:")
print(closest_phones)
