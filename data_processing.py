import pandas as pd
import glob
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, "data", "*.csv")
file_paths = glob.glob(data_path)

processed_dfs = []

for file in file_paths:
    df = pd.read_csv(file)
    
    df = df[df['product'].str.strip() == 'Pink Morsel']
    
    df['price'] = df['price'].astype(str).str.replace('$', '', regex=False).astype(float)
    
    df['sales'] = df['quantity'] * df['price']
    
    df = df[['sales', 'date', 'region']]
    
    processed_dfs.append(df)

if len(processed_dfs) > 0:
    final_df = pd.concat(processed_dfs, ignore_index=True)
    output_path = os.path.join(current_dir, "formatted_output.csv")
    final_df.to_csv(output_path, index=False)
    print("Success! formatted_output.csv has been created.")
else:
    print("Error: No CSV files found in the data folder. Please check the folder location.")