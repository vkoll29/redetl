import pyodbc
from sqlalchemy import create_engine, event
from urllib.parse import quote_plus

from src.utils.get_config import __load_config

config = __load_config('config/config.yml')


def establish_conn():
    """
    Establishes a connection to the database.
    :return: returns a connection object if successful, otherwise returns an error message

    TODO:
        - Add exception handling for connection errors.
        - Add exception handling for config file errors.
        - declare config as a variable in the function. then pass the file name as a parameter.
    """
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={config['db']['server']};"
        f"DATABASE={config['db']['instance']};"
        f"UID={config['db']['username']};"
        f"PWD={config['db']['pw']}"
    )

    try:
        conn = pyodbc.connect(conn_str)
        print("DB Connection Successful!")
        return conn
    except Exception as e:
        print(f"Error: {e}")
        return e


def sa_engine():
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={config['db']['server']};"
        f"DATABASE={config['db']['instance']};"
        f"UID={config['db']['username']};"
        f"PWD={config['db']['pw']}"
    )
    quoted = quote_plus(conn_str)
    sa_conn = f"mssql+pyodbc:///?odbc_connect={quoted}"
    engine = create_engine(sa_conn)

    return engine
