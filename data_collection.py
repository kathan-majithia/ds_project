import pandas as pd

def load_data():
    df = pd.read_csv('ethereum.csv')
    
    # Rename messy columns
    df.columns = df.columns.str.strip()
    
    print(f"Shape: {df.shape}")
    print(f"Dtypes:\n{df.dtypes}")
    
    return df