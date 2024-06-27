from etl.transform._add_bottler_column import add_bottler_column
from src.utils.convert_dtypes import get_sql_dtype
from etl.load.commons import execute_common_ops


def mq_insert_staging(conn, df, container_name):

    table = 'IRManualQuestions'
    # step 1: Drop unnecessary columns
    columns_to_drop = [
        'ID',
        'QuestionType',
        'Text',
        'Tags',
        'ProductDetail',
        'ReExportStatus',
        'ReExportTime',
        'ExpiryDate'
    ]
    df = df.drop(columns_to_drop, axis=1)

    # step 2: Truncate options column to 200 characters
    df['Options'] = df['Options'].str[:200]

    # step 2: Add Bottler column
    df = add_bottler_column(df, container_name)

    # step 3: reorder columns
    new_order = [
        'SessionUID',
        'SceneUID',
        'SceneType',
        'SubSceneType',
        'ProgramID',
        'ProgramName',
        'ProgramItemID',
        'ProgramItemName',
        'QuestionID',
        'QuestionCategory',
        'QuestionText',
        'LocalQuestionText',
        'ParentQuestionID',
        'Options',
        'AnswerValue',
        'CreatedOnTime',
        'LastModifiedTime',
        'FileCreatedTime',
        'SliceStartTime',
        'SliceEndTime',
        'SceneLevel',
        'SessionLevel',
        'Description',
        'ReProcessedTime',
        'ReProcessedStatus',
        'Bottler',
        'EvidenceImageName',
        'EvidenceImageURL'
    ]
    df = df.loc[:, new_order]

    # Execute common operations
    execute_common_ops(conn, df, table)

        # step 4: Convert dtypes to SQL types
        # df_tf = get_sql_dtype(df)

        # step 4: Insert data to staging table
        # load_data(df_tf, conn, 'stg.StageIRManualQuestions')
