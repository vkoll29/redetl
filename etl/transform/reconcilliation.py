from etl.transform._add_bottler_column import add_bottler_column
from src.utils.get_conn import sa_engine
from sqlalchemy import create_engine
from src.utils.count_columns import count_columns
from src.utils.load_to_db import load_data
from src.utils.convert_dtypes import get_sql_dtype
from src.utils.insert_sa import insert_sa


def recon_insert_staging(conn, df, container_name):
    """
    This function takes in a dataframe and a container name, then inserts the dataframe into the staging table.
    :param conn: connection object to the database
    :param df: df to insert into staging table
    :param container_name: the container name of the dataframe which determines the bottler name
    :return:
    """
    # step 1: Drop unnecessary columns
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
    df_tf = df[new_order]
    df_tf = get_sql_dtype(df_tf)
    # df_tf.to_csv(r'./df_tf.csv', index=False)

    # step 3: Insert data to staging table
    load_data(df_tf, conn, 'stg.stageIRReconciliation')
    # insert_sa()
    # cursor = conn.cursor()
    # column_names = df.columns.tolist()
    # from pprint import pprint
    # pprint(column_names)
