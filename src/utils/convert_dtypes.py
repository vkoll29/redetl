import pandas as pd


def get_sql_dtype(df):
    """
    Converts DataFrame columns to appropriate types for SQL insertion.
    - Non-datetime columns are converted to string (equivalent to SQL's nvarchar).
    - Datetime columns are converted to date format.
    :param df: Input DataFrame.
    :return: Modified DataFrame.
    """
    # Print initial data types
    print("Initial data types:\n", df.dtypes)
    for col in df.select_dtypes(exclude=['datetime64[ns]']).columns:
        if col != 'Target Score':  # target score is a float, if converted to str the ingestion will fail
            df[col] = df[col].astype(str)

    # Convert datetime columns to date
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):

            # the lambda function below ensures that NaT values are replaced with None which SQL will handle as NULL

            df[col] = df[col].apply(lambda x: x.date() if pd.notna(x) else None)

    return df
