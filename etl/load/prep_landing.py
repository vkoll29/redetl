def prep_landing_table(conn, base_table_name):
    """
    This function deletes rows from the landing table that have a corresponding row in the staging table.
    It is used to avoid duplicate rows in the landing table. The assumption is there are rows in the landing table that may have been updated from source
    :param conn: connection object to the database
    :param base_table_name: name of the table to delete rows from
    :return:
    """
    cursor = conn.cursor()
    try:
        cursor.execute(f"""
            DELETE T      
            FROM  
                dbo.{base_table_name} T 
            INNER JOIN
                dbo.Stage{base_table_name} S ON T.SessionUid = S.SessionUid 
          
        """)
        conn.commit()
        print(f"Successfully deleted {cursor.rowcount} rows from {base_table_name}")
    except Exception as e:
        print(f"ERROR PREPPING LANDING TABLE: {e}")
    finally:
        if conn:
            cursor.close()


