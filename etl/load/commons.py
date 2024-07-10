from src.utils.convert_dtypes import get_sql_dtype
from etl.load.load_to_db import load_data
from etl.load.prep_landing import prep_landing_table
from etl.load.clear_staging import clear_staging_table


def execute_common_ops(conn, df, table):


    # step 2: Convert dtypes to SQL types
    df = get_sql_dtype(df)

    # step 3: insert data to staging table
    load_data(df, conn, f'dbo.stage{table}')

    # step 4: Prepare landing table
    prep_landing_table(conn, table)

    # step 5: Insert data to landing table
    load_data(df, conn, f'dbo.{table}')

    # step 6: Truncate staging table
    clear_staging_table(conn, table)

