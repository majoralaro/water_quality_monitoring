import pandas as pd
def clean_sensor_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean sensor data by handling missing or invalid values.

    Returns:
        pd.DataFrame: Cleaned data.
    """
    # Create a copy to avoid modifying the original DataFrame
    df_clean = df.copy()
    
    # Handle missing values
    # For numeric columns, fill with median
    numeric_cols = df_clean.select_dtypes(include=['float64', 'int64']).columns
    for col in numeric_cols:
        # Check for NaN or inf values
        df_clean[col] = df_clean[col].replace([float('inf'), -float('inf')], pd.NA)
        # Fill missing values with median
        df_clean[col] = df_clean[col].fillna(df_clean[col].median())
    
    # Handle non-numeric columns (if any)
    non_numeric_cols = df_clean.select_dtypes(exclude=['float64', 'int64']).columns
    for col in non_numeric_cols:
        # Fill missing categorical values with mode
        df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0])
    
    # Remove outliers using IQR method for numeric columns
    for col in numeric_cols:
        Q1 = df_clean[col].quantile(0.25)
        Q3 = df_clean[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Replace outliers with median
        df_clean[col] = df_clean[col].where(
            (df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound),
            df_clean[col].median()
        )
    
    # Handle negative values in columns where they don't make sense
    # Assuming sensor readings like temperature, pressure, etc. shouldn't be negative
    for col in numeric_cols:
        if df_clean[col].min() < 0:
            # Replace negative values with median
            df_clean[col] = df_clean[col].where(df_clean[col] >= 0, df_clean[col].median())
    
    # Remove duplicate rows
    df_clean = df_clean.drop_duplicates()
    
    # Ensure correct data types
    for col in numeric_cols:
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
    
    return df_clean