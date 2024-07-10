from etl.transform._add_bottler_column import add_bottler_column
from src.utils.extract_target_value import get_target_value
from src.utils.extract_target_score import get_target_score
from etl.load.commons import execute_common_ops


def metrics_insert_staging(conn, df, container_name):
    if df is None:
        print(f"container {container_name} is empty")
        return
    table = 'IRMetricsV2'
    # step 1: Drop unnecessary columns
    columns_to_drop = [
        'ID',
        'ReExportStatus',
        'ReExportTime',
        'PeriodStartDate',
        'PeriodEndDate',
        'SubPeriodStartDate',
        'SubPeriodEndDate',
        'MetricGroupId',
        'MetricGroupName',
        'Expression',
        'ProgramItemReferenceId'
    ]
    df = df.drop(columns_to_drop, axis=1)

    # step 2: Add Bottler column
    df = add_bottler_column(df, container_name)

    # step 3: Rename  columns
    # a) Maxpoints to Maxpoint
    df = df.rename(columns={'MaxPoints': 'MaxPoint'})

    # b) SessionUID to SessionUid
    df = df.rename(columns={'SessionUID': 'SessionUid'})

    # c) ProgramID to ProgramId
    df = df.rename(columns={'ProgramID': 'ProgramId'})

    # d) ProgramItemID to ProgramItemId
    df = df.rename(columns={'ProgramItemID': 'ProgramItemId'})

    # d) Calculation to TargetScore
    df = df.rename(columns={'Calculation': 'Target Score'})

    # step 4: Filter out zero values
    condition1 = (df['Value'] != "0") & (df['Value'] != "00") & (df['Value'] != "000")
    condition2 = df['Score'] != "0"
    condition3 = df['Target Score'].str.split(",", expand=True)[1] != "0"
    df = df[condition1 | condition2 | condition3]


    # Step 5: Derive Columns
    # a) TargetValue
    # REPLACE(TOKEN([Target Score], " > = >= <= < = ,", 2), "''YES''", "YES")
    df['Target Value'] = df['Target Score'].apply(get_target_value)

    # b) Metrics column
    df['Metrics'] = df['Target Score']

    # c) TargetScore
    df['Target Score'] = df['Target Score'].apply(get_target_score)

    # step 5: Remove 0 targets

    # step 6: reorder columns
    new_order = [
        'SessionUid',
        'SceneUID',
        'ProgramId',
        'ProgramName',
        'ProgramArea',
        'ProgramItemId',
        'ProgramItemName',
        'ItemID',
        'ItemType',
        'Template',
        'Description',
        'ConsideredForScoring',
        'Domain',
        'DomainValue',
        'Value',
        'MaxPoint',
        'MaxTarget',
        'Score',
        'Metrics',
        'CreatedOnTime',
        'LastModifiedTime',
        'FileCreatedTime',
        'SliceStartTime',
        'Bottler',
        'SliceEndTime',
        'Target Score',
        'Target Value',
        'ReProcessedStatus',
        'ReProcessedTime'

    ]
    df = df.loc[:, new_order]

    # Execute common operations
    execute_common_ops(conn, df, table)

