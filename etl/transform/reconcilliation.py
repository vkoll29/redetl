from etl.transform._add_bottler_column import add_bottler_column
from src.utils.get_conn import sa_engine
from sqlalchemy import create_engine
from src.utils.count_columns import count_columns
from etl.load.load_to_db import load_data
from src.utils.convert_dtypes import get_sql_dtype
from src.utils.insert_sa import insert_sa
from etl.load.prep_landing import prep_landing_table
from etl.load.clear_staging import clear_staging_table
from etl.load.commons import execute_common_ops


def recon_insert_staging(conn, df, container_name):
    """
    This function takes in a dataframe and a container name, then inserts the dataframe into the staging table.
    :param conn: connection object to the database
    :param df: df to insert into staging table
    :param container_name: the container name of the dataframe which determines the bottler name
    :return:
    """

    # Check if df is Nonetype
    if df is None:
        print(f"container {container_name} is empty")
        return

    # step 1: Drop unnecessary columns
    table = 'IRReconciliation'
    # df.to_csv(r'./df.csv', index=False)
    columns_to_drop = ['PrimaryEmail', 'UserProfile', 'SurveyId', 'IsMetricCalculated', 'UserName',
                       'SurveyFinishReceivedOn', 'ReconSummary']
    df = df.drop(columns_to_drop, axis=1)

    # step 2: Add Bottler column
    df = add_bottler_column(df, container_name)

    # step 3: reorder columns
    new_order = [
        'SessionUid',
        'SessionStartDateTime',
        'SessionEndDateTime',
        'ClientCode',
        'SubClientCode',
        'OutletCode',
        'OutletName',
        'CountryCode',
        'UserId',
        'SessionStatusCode',
        'SessionStatus',
        'Latitude',
        'Longitude',
        'TotalSceneActualReceived',
        'TotalSceneSummaryReceived',
        'TotalSceneProcessed',
        'TotalQuestionActualReceived',
        'TotalQuestionSummaryReceived',
        'IsQuestionSetup',
        'IsMetricSetup',
        'IsCMASetup',
        'IsPrioritySetup',
        'ParquetExportedStatus',
        'SessionProcessingStatus',
        'CreatedOnTime',
        'LastModifiedTime',
        'FileCreatedTime',
        'SliceStartTime',
        'SliceEndTime',
        'Bottler'
    ]
    df = df[new_order]

    # Execute common operations
    execute_common_ops(conn, df, table)



