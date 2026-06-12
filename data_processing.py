import os
import glob
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
data_folder = os.path.join(current_dir, "data")
file_paths = glob.glob(os.path.join(data_folder, "*.csv"))

processed_dfs = []

for file in file_paths:
    df = pd.read_csv(file)
    
    # تصحیح حروف بزرگ و کوچک در ستون محصول
    df['product'] = df['product'].str.strip()
    df = df[df['product'].str.lower() == 'pink morsel']
    
    # محاسبه فروش
    df['price'] = df['price'].astype(str).str.replace('$', '', regex=False).astype(float)
    df['sales'] = df['quantity'] * df['price']
    
    # انتخاب ستون‌های نهایی
    df = df[['sales', 'date', 'region']]
    processed_dfs.append(df)

if len(processed_dfs) > 0:
    final_df = pd.concat(processed_dfs, ignore_index=True)
    output_path = os.path.join(current_dir, "formatted_output.csv")
    final_df.to_csv(output_path, index=False)
    print("FINISHED_SUCCESSFULLY")
else:
    print("NO_DATA_FOUND")