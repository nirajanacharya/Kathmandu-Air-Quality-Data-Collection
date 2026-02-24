import pandas as pd

def clean_and_pivot(df):
    if df.empty:
        print("WARNING: Empty DataFrame received")
        return pd.DataFrame()
    
    print(f"Raw data: {df.shape[0]:,} rows × {df.shape[1]} columns")
    
    datetime_cols = [col for col in df.columns if 'datetime' in col.lower() or 'date' in col.lower()]
    
    if not datetime_cols:
        print("ERROR: No datetime column found!")
        return pd.DataFrame()
    
    datetime_col = datetime_cols[0]
    
    required_cols = [datetime_col, "parameter", "value"]
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        print(f"ERROR: Missing columns: {missing_cols}")
        return pd.DataFrame()
    
    df_clean = df[required_cols].copy()
    df_clean.rename(columns={datetime_col: "datetime"}, inplace=True)
    df_clean["datetime"] = pd.to_datetime(df_clean["datetime"])
    df_clean = df_clean.dropna()
    
    params = sorted(df_clean['parameter'].unique())
    print(f"Parameters: {', '.join(params)}")
    print(f"Date range: {df_clean['datetime'].min()} to {df_clean['datetime'].max()}")
    
    df_pivot = df_clean.pivot_table(
        index="datetime",
        columns="parameter",
        values="value",
        aggfunc="mean"
    )
    
    df_pivot = df_pivot.sort_index()
    
    print(f"Final data: {df_pivot.shape[0]:,} timestamps × {df_pivot.shape[1]} parameters")
    
    return df_pivot