def clear_staging_table(conn, base_table_name):
    """
    This function truncates the staging table.
    :param conn: connection object to the database
    :param base_table_name: the base name of the table to truncate
    :return:
    """
    cursor = conn.cursor()
    try:
        cursor.execute(f"TRUNCATE TABLE stg.stage{base_table_name}")
        conn.commit()
        print(f"stg.stage{base_table_name} truncated")
    except Exception as e:
        print(f"ERROR TRUNCATING stg.stage{base_table_name}: {e}")
