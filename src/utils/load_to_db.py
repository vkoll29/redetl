from src.utils.count_columns import count_columns
from sqlalchemy import event
import time
import pyodbc
import logging

logging.basicConfig(filename='etl_log.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def load_data(df, conn, table):
    """
    Loads the provided dataframe to the database
    :param df: this is the dataframe to be loaded
    :param conn: connection object to the database
    :param table: the table to load the data into
    :return: None
    """
    print(f"Loading {len(df)} rows to {table}")
    start = time.time()
    cursor = conn.cursor()
    cursor.fast_executemany = True
    vals = count_columns(df)
    insert_stmt = f'INSERT INTO {table} VALUES ({vals})'

    # data_to_insert = df.values.tolist()
    # # # data_to_insert = [tuple(x) for x in data_to_insert]
    # for row in data_to_insert:
    #     try:
    #         cursor.execute(insert_stmt, row)
    #         logging.debug(f'Successfully inserted row: {row}')
    #     except Exception as e:
    #         logging.debug(f"Error inserting row: {row}. Exception: {e}")
    #         # conn.rollback()
    #
    # cursor.commit()
    # cursor.close()
    # conn.close()
    # print(f"Operation took {time.time() - start} seconds")

    try:

        # Try batch insert with executemany
        cursor.executemany(insert_stmt, df.values.tolist())
        cursor.commit()
        print(f"{cursor.rowcount} rows inserted")
        print(f"Time taken to write to db: {time.time() - start}")

    except Exception as ex:
        print(f'Batch insert failed. Time taken is {time.time() - start}.\n  Exception: {ex}')

    finally:
        cursor.close()
        conn.close()


def load_data_sa(df, engine, conn, table):
    @event.listens_for(engine, "before_cursor_execute")
    def receive_before_cursor_execute(
            conn, cursor, statement, params, context, executemany
    ):
        print("FUNC CALL")
        if executemany:
            cursor.fast_executemany = True

    S = time.time()
    df.to_sql(table, engine, if_exists='append', chunksize=None)


