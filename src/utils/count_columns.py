def count_columns(df):
    """
    Create a string that contains ? to be used to insert values into a sql db table
    :param df: the dataframe whose number of columns should be counted
    :return: the parameterized string
    :example: a df with 4 columns should return '?,?,?,?'
    """
    n = len(df.columns)
    values_string_list = list('?' * n)
    values_param = ','.join(values_string_list)
    return values_param
