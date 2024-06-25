import pandas as pd
import numpy as np
import time
from sqlalchemy import create_engine, event
from urllib.parse import quote_plus
from src.utils.get_config import __load_config

config = __load_config('config/config.yml')


def insert_sa():
    conn = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={config['db']['server']};"
        f"DATABASE={config['db']['instance']};"
        f"UID={config['db']['username']};"
        f"PWD={config['db']['pw']}"
    )
    quoted = quote_plus(conn)
    new_con = 'mssql+pyodbc:///?odbc_connect={}'.format(quoted)
    engine = create_engine(new_con)

    @event.listens_for(engine, 'before_cursor_execute')
    def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
        print("FUNC call")
        if executemany:
            cursor.fast_executemany = True

    table_name = 'fast_executemany_test'
    df = pd.DataFrame(np.random.random((10 ** 4, 100)))

    s = time.time()
    df.to_sql(table_name, engine, if_exists='replace', chunksize=None)
    print(time.time() - s)
