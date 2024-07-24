import pandas as pd


def truncate_str(df):
    # Step 6: truncate all str columns
    for col in df.columns:

        if pd.api.types.is_string_dtype(df[col]):
            df[col] = df[col].str.slice(0, 500)
    return df
