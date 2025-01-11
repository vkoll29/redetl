def clear_staging_table(conn, schema, base_table_name):
    """
    This function truncates the staging table.
    :param schema: specifies the schema in which the table resides
    :param conn: connection object to the database
    :param base_table_name: the base name of the table to truncate
    :return:
    """
    cursor = conn.cursor()
    try:
        cursor.execute(f"TRUNCATE TABLE {schema}.stage{base_table_name}")
        conn.commit()
        print(f"{schema}.stage{base_table_name} truncated")
    except Exception as e:
        print(f"ERROR TRUNCATING {schema}.stage{base_table_name}: {e}")
