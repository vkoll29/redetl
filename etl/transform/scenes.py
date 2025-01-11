from etl.transform._add_bottler_column import add_bottler_column
from etl.load.commons import execute_common_ops


def scenes_insert_staging(conn, df, container_name):
    if df is None:
        print(f"container {container_name} is empty")
        return

    table = 'IRScenes'
    # step 1: Drop unnecessary columns
    columns_to_drop = [
        'ImageQuality',
        'ReExportStatus',
        'ReExportTime',
        'AssetSerialNumber',
        'AssetEquipmentNumber',
        'SceneCollectionMode',
        'IsSelfValidated',
        'IsClientValidated',
        'IrImageUsable'
    ]
    df = df.drop(columns_to_drop, axis=1)

    # step 2: Add Bottler column
    df = add_bottler_column(df, container_name)

    # step 3: reorder columns
    new_order = [
        'SessionUID',
        'SceneUID',
        'SceneDateTime',
        'VerifiedOn',
        'Source',
        'SceneType',
        'SubSceneType',
        'CreatedOnTime',
        'LastModifiedTime',
        'FileCreatedTime',
        'SliceStartTime',
        'SliceEndTime',
        'Bottler',
        'ReProcessedTime',
        'ReProcessedStatus',
        'StitchedImageURL',
        'RawImagePath',
        'RawImageNames',
        'ParentSceneUid',
        'ImageCount',
        'IsFacingAvailable',
        'SubClientCode'
    ]

    df = df.loc[:, new_order]

    # Execute common operations
    execute_common_ops(conn, df, table)
