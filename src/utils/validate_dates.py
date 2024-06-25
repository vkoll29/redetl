import pandas as pd


def validate_and_format_dates(date_series):
    min_date = pd.to_datetime('1753-01-01')
    max_date = pd.to_datetime('9999-12-31')
    valid_dates = date_series.apply(pd.to_datetime, errors='coerce')
    valid_dates = valid_dates[(valid_dates >= min_date) & (valid_dates <= max_date)]
    valid_dates = valid_dates.fillna(pd.Timestamp('1900-01-01'))
    return valid_dates.dt.strftime('%Y-%m-%d %H:%M:%S')
