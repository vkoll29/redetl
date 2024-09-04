import pandas as pd


def get_sql_dtype(df, **kwargs):
    """
    Converts DataFrame columns to appropriate types for SQL insertion.
    - Non-datetime columns are converted to string (equivalent to SQL's nvarchar).
    - Datetime columns are converted to date format.
    :param df: Input DataFrame.
    :return: Modified DataFrame.
    """
    # print("Initial data types:\n", df.dtypes)
    for col in df.select_dtypes(exclude=['datetime64[ns]']).columns:
        if col != 'Target Score':  # target score is a float, if converted to str the ingestion will fail
            df[col] = df[col].astype(str)

    # Convert datetime columns to date
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            # this will only be applicable to sessions_wt_timestamp table
            # this if block basically means the columns are not converted to date type and instead they keep their datetime value
            if 'date_columns_to_ignore' in kwargs:
                if col not in kwargs['date_columns_to_ignore']:
                    # the lambda function below ensures that NaT values are replaced with None which SQL will handle as NULL
                    df[col] = df[col].apply(lambda x: x.date() if pd.notna(x) else None)

                else:
                    df[col] = df[col]

            # this applies to every other table
            else:
                df[col] = df[col].apply(lambda x: x.date() if pd.notna(x) else None)

    return df
