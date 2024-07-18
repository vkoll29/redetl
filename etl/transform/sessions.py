from etl.transform._add_bottler_column import add_bottler_column
from src.utils.convert_dtypes import get_sql_dtype
from etl.load.commons import execute_common_ops


def sessions_insert_staging(conn, df, container_name):
    if df is None:
        print(f"container {container_name} is empty")
        return
    table = 'Sessions'
    table_ts = 'SessionsWtTimestamp'
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

    # Sessions with timestamp take a different approach
    # insert into sessions wt ts first because you need the original datetime values. the df is held in memory and
    # any transformations on it will be kept for subsequent operations
    execute_common_ops(conn, df, table_ts, date_columns_to_ignore=['SessionStartDateTime', 'SessionEndDateTime'])

    # Execute common operations
    execute_common_ops(conn, df, table)
