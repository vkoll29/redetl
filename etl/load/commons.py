from src.utils.convert_dtypes import get_sql_dtype
from src.utils.truncate_str_cols import truncate_str
from etl.load.load_to_db import load_data
from etl.load.prep_landing import prep_landing_table
from etl.load.clear_staging import clear_staging_table


def execute_common_ops(conn, df, table, **kwargs):
    schema = 'staging'

    # step 1: truncate strings
    df = truncate_str(df)
    # step 2: Convert dtypes to SQL types
    if 'date_columns_to_ignore' in kwargs:
        df = get_sql_dtype(df, date_columns_to_ignore=kwargs['date_columns_to_ignore'])
    else:
        df = get_sql_dtype(df)

    # step 3: insert data to staging table
    load_data(df, conn, f'{schema}.stage{table}')

    # step 4: Prepare landing table
    prep_landing_table(conn, schema, table)

    # step 5: Insert data to landing table
    load_data(df, conn, f'{schema}.{table}')

    # step 6: Truncate staging table
    clear_staging_table(conn, schema, table)

