from etl.transform._add_bottler_column import add_bottler_column
from etl.load.commons import execute_common_ops


def mq_insert_staging(conn, df, container_name):
    if df is None:
        print(f"container {container_name} is empty")
        return

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
        'SubClientCode',
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
        'EvidenceImageURL',
        'QuestionGroup'
    ]
    df = df.loc[:, new_order]

    # Execute common operations
    execute_common_ops(conn, df, table)
