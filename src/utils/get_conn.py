import pyodbc
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
    conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={config['db']['server']};DATABASE={config['db']['instance']};UID={config['db']['username']};PWD={config['db']['pw']}"

    try:
        conn = pyodbc.connect(conn_str)
        print("DB Connection Successful!")
        return conn
    except Exception as e:
        print(f"Error: {e}")
        return e

establish_conn()