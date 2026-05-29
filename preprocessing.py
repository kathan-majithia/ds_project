import pandas as pd
from datetime import datetime

def clean_data(df):
    df = df.drop_duplicates()
    print(f"After dup removal: {len(df)} rows")

    df = df.fillna(0)

    df = df[(df['Value_IN(ETH)'] > 0) | (df['Value_OUT(ETH)'] > 0)]
    print(f"After filtering zeros: {len(df)} rows")
    
    df['DateTime'] = pd.to_datetime(df['DateTime (UTC)'], format='%Y-%m-%d %H:%M:%S')
    
    df['TxnFee(ETH)'] = pd.to_numeric(df['TxnFee(ETH)'], errors='coerce').fillna(0)
    df['Value_IN(ETH)'] = pd.to_numeric(df['Value_IN(ETH)'], errors='coerce').fillna(0)
    df['Value_OUT(ETH)'] = pd.to_numeric(df['Value_OUT(ETH)'], errors='coerce').fillna(0)
    
    return df

def engineer_features(df):

    df['hour'] = df['DateTime'].dt.hour
    df['day_of_week'] = df['DateTime'].dt.dayofweek
    df['month'] = df['DateTime'].dt.month
    
    df['total_value'] = df['Value_IN(ETH)'] + df['Value_OUT(ETH)']
    df['is_large_tx'] = (df['total_value'] > df['total_value'].quantile(0.9)).astype(int)
    df['fee_ratio'] = df['TxnFee(ETH)'] / (df['total_value'] + 0.001)  # Avoid division by 0
    
    whale_threshold = df['total_value'].quantile(0.90)
    df['is_whale'] = (df['total_value'] > whale_threshold).astype(int)
    
    return df