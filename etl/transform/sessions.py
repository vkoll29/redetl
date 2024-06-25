from etl.transform._add_bottler_column import add_bottler_column
from src.utils.load_to_db import load_data
from src.utils.convert_dtypes import get_sql_dtype


def sessions_insert_staging(conn, df, container_name):

    # step 1: Drop unnecessary columns
    columns_to_drop = ['ID',
                       'ProgramId',
                       'ProgramName',
                       'ProgramItemId',
                       'ProgramItemName',
                       'PrimaryEmail',
                       'UserProfile',
                       'CancelEvidenceImageUrl',
                       'CancelEvidenceImageName',
                       'ReExportStatus',
                       'ReExportTime',
                       'ReProcessedStatus',
                       'ReProcessedTime',
                       'UserName',
                       'SessionSource',
                       'SessionEndLatitude',
                       'SessionEndLongitude',
                       'LastCorrectedOn',
                       'LastCorrectedBy',
                       'ClientReferenceID',
                       'ManuallyCompletedOn',
                       'ManuallyCompletedBy',
                       'ProgramItemReferenceId',
                       'IsRouteCompliance',
                       ]
    df = df.drop(columns_to_drop, axis=1)

    # step 2: Add Bottler column
    df = add_bottler_column(df, container_name)


    # step 3: convert dtypes
    df = get_sql_dtype(df)

    # step 4: Insert data to staging table
    load_data(df, conn, 'stg.stageSessions')
